from django.contrib.auth import authenticate
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
import random
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .notifications import record_notification, send_and_log, send_admin_appointment_email
from .serializers import *

def tokens(user):
    refresh=RefreshToken.for_user(user)
    return {'refresh':str(refresh),'access':str(refresh.access_token)}

@api_view(['GET'])
@permission_classes([AllowAny])
def site_data(request):
    s=SiteSettings.objects.first()
    data={'site':SiteSerializer(s,context={'request':request}).data if s else None,
          'hero_banners':HeroBannerSerializer(HeroBanner.objects.filter(active=True),many=True,context={'request':request}).data,
          'nav':list(NavItem.objects.filter(active=True).values('label')),
          'offer':(lambda o:{'eyebrow':o.eyebrow,'title':o.title,'description':o.description,'button_text':o.button_text})(OfferBanner.objects.filter(active=True).first()) if OfferBanner.objects.filter(active=True).exists() else None,
          'services':ServiceSerializer(Service.objects.filter(active=True),many=True).data,
          'trust':TrustSerializer(TrustFeature.objects.filter(active=True),many=True).data,
          'doctors':DoctorSerializer(Doctor.objects.filter(active=True),many=True,context={'request':request}).data,
          'gallery':GallerySerializer(GalleryItem.objects.filter(active=True),many=True,context={'request':request}).data,
          'addresses':AddressSerializer(ClinicAddress.objects.filter(active=True),many=True).data,
          'hours':HourSerializer(ClinicHour.objects.all(),many=True).data,
          'footer':FooterSerializer(FooterLink.objects.filter(active=True),many=True).data,
          'pages':PageContentSerializer(PageContent.objects.filter(active=True),many=True,context={'request':request}).data,
          'texts':SiteTextSerializer(SiteText.objects.all(),many=True).data,
          'branches':BranchSerializer(Branch.objects.filter(active=True),many=True).data,
          'clinic_images':ClinicImageSerializer(ClinicImage.objects.filter(active=True),many=True,context={'request':request}).data,
          'youtube':YoutubeVideoSerializer(YoutubeVideo.objects.filter(active=True),many=True).data,
          'awards':AwardSerializer(Award.objects.filter(active=True),many=True,context={'request':request}).data}
    response = Response(data)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    return response

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    ser=RegisterSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    if User.objects.filter(username=ser.validated_data['username']).exists(): return Response({'detail':'Username already exists.'},status=400)
    user=ser.save()
    Appointment.objects.filter(user__isnull=True,email__iexact=user.email).update(user=user)
    # Claim the guest notifications that were held against this email address.
    Notification.objects.filter(user__isnull=True,email__iexact=user.email).exclude(email='').update(user=user,email='')
    return Response({'user':UserSerializer(user).data,**tokens(user)},status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    user=authenticate(username=request.data.get('username'),password=request.data.get('password'))
    if not user: return Response({'detail':'Invalid username or password.'},status=401)
    return Response({'user':UserSerializer(user).data,**tokens(user)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request): return Response(UserSerializer(request.user).data)

def _mask_email(email):
    local, _, domain = email.partition('@')
    return f"{local[:2]}***@{domain}" if domain else email


def _format_wait(seconds):
    seconds = max(1, int(seconds))
    return f"{seconds // 60}:{seconds % 60:02d}"


@api_view(['POST'])
@permission_classes([AllowAny])
def request_appointment_otp(request):
    ser=AppointmentSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    data=ser.validated_data
    email=data['email'].strip().lower()
    masked=_mask_email(email)

    now=timezone.now()
    cooldown=timedelta(seconds=getattr(settings,'OTP_RESEND_COOLDOWN_SECONDS',120))

    # Send at most ONE email per cooldown window per address. If a code is still
    # pending, refresh it with the latest form values and hand back the same
    # reference instead of mailing a second code (a double click, a retry or an
    # impatient resend must not spam the patient's inbox).
    pending=(EmailOTP.objects
             .filter(email__iexact=email,verified=False,expires_at__gt=now)
             .order_by('-created_at')
             .first())
    if pending and pending.created_at > now-cooldown:
        for field in ('full_name','mobile_number','preferred_date','treatment_type','message'):
            setattr(pending,field,data.get(field,''))
        if request.user.is_authenticated and pending.user_id is None:
            pending.user=request.user
        pending.save()
        wait=max(1,int((cooldown-(now-pending.created_at)).total_seconds()))
        return Response({
            'ok':True,
            'otp_id':pending.id,
            'masked_email':masked,
            'expires_in':max(1,int((pending.expires_at-now).total_seconds())),
            'resend_in':wait,
            'email_sent':False,
            'notice':f'A verification code was already emailed to {masked}. You can ask for a new code in {_format_wait(wait)}.',
        })

    code=f"{random.randint(0,9999):04d}"
    EmailOTP.objects.filter(email__iexact=email,verified=False).update(verified=True)
    otp=EmailOTP.objects.create(
        email=email,
        full_name=data['full_name'],
        mobile_number=data['mobile_number'],
        preferred_date=data['preferred_date'],
        treatment_type=data['treatment_type'],
        message=data.get('message',''),
        otp_hash=make_password(code),
        expires_at=now+timedelta(minutes=settings.OTP_EXPIRY_MINUTES),
        user=request.user if request.user.is_authenticated else None,
    )
    pref_date_str = otp.preferred_date.strftime('%d/%m/%Y') if hasattr(otp.preferred_date, 'strftime') else str(otp.preferred_date)
    log = send_and_log('appointment_otp', otp.email, {
        'otp':code,'expiry_minutes':settings.OTP_EXPIRY_MINUTES,'full_name':otp.full_name,
        'mobile_number':otp.mobile_number,'email':otp.email,'preferred_date':pref_date_str,
        'treatment_type':otp.treatment_type,'message':otp.message
    }, user=otp.user)
    email_sent = bool(log and log.status == 'sent')
    error_note = log.error if log else ''
    if not email_sent:
        print(f"[OTP DEV NOTICE] Could not send email via Gmail SMTP: {error_note}")
        print(f"[OTP CODE] Verification code for {otp.email} is: {code}")
        if not getattr(settings, 'DEBUG', False):
            otp.delete()
            return Response({'detail':f'Unable to send Gmail OTP. Check your Gmail SMTP configuration in backend/.env. ({error_note})'},status=503)

    resp = {
        'ok': True,
        'otp_id': otp.id,
        'masked_email': masked,
        'expires_in': settings.OTP_EXPIRY_MINUTES*60,
        'resend_in': int(cooldown.total_seconds()),
        'email_sent': email_sent,
    }
    if not email_sent:
        resp['dev_otp'] = code
        resp['notice'] = f"Local dev fallback: SMTP delivery failed ({error_note}). Your verification code is {code}."
    return Response(resp)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_appointment_otp(request):
    otp=EmailOTP.objects.filter(pk=request.data.get('otp_id'),verified=False).first()
    if not otp: return Response({'detail':'This verification request is no longer valid. Please request a new OTP.'},status=400)
    if timezone.now()>otp.expires_at: return Response({'detail':'OTP expired. Please request a new OTP.'},status=400)
    if otp.attempts>=5: return Response({'detail':'Too many incorrect attempts. Please request a new OTP.'},status=429)
    code=str(request.data.get('otp','')).strip()
    if len(code)!=4 or not code.isdigit() or not check_password(code,otp.otp_hash):
        otp.attempts += 1; otp.save(update_fields=['attempts'])
        return Response({'detail':'Incorrect verification code.'},status=400)
    otp.verified=True; otp.save(update_fields=['verified'])
    user=request.user if request.user.is_authenticated else otp.user
    appointment=Appointment.objects.create(user=user,full_name=otp.full_name,mobile_number=otp.mobile_number,email=otp.email,preferred_date=otp.preferred_date,treatment_type=otp.treatment_type,message=otp.message,status='pending')
    # Panel record only — the OTP email has already been sent and no further
    # Gmail message goes out. The notification is linked to the account when the
    # patient is signed in, otherwise held against their email address until
    # they register.
    appt_date_str = appointment.preferred_date.strftime('%d/%m/%Y') if hasattr(appointment.preferred_date, 'strftime') else str(appointment.preferred_date)
    record_notification(
        recipient=appointment.email,
        title='Appointment Request Received',
        message=f'Your {appointment.treatment_type} appointment request for {appt_date_str} has been received. Our coordinator will contact you soon.',
        user=user,
        appointment=appointment,
    )
    # Immediately notify admin/clinic staff via email with full appointment details
    send_admin_appointment_email(appointment)
    return Response({'ok':True,'appointment':AppointmentSerializer(appointment).data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    appointments=Appointment.objects.filter(user=request.user)
    notifications=Notification.objects.filter(user=request.user)
    return Response({'user':UserSerializer(request.user).data,'appointments':AppointmentSerializer(appointments,many=True).data,'notifications':NotificationSerializer(notifications,many=True).data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request,pk):
    n=Notification.objects.filter(pk=pk,user=request.user).first()
    if not n: return Response({'detail':'Not found'},status=404)
    n.is_read=True; n.save(update_fields=['is_read']); return Response({'ok':True})
