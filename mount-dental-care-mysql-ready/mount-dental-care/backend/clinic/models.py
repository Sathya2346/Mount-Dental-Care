from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

# Text-block keys are dotted (e.g. "services.heading.title"), which SlugField
# rejects — so validate with a pattern that allows dots as well as dashes.
text_key_validator = RegexValidator(
    r'^[a-zA-Z0-9_.-]+$',
    'Use only letters, numbers, dots, dashes and underscores.',
)

class HeroBanner(models.Model):
    MEDIA_CHOICES=[("image","Image"),("video","Video")]
    title=models.CharField(max_length=150,blank=True)
    media_type=models.CharField(max_length=10,choices=MEDIA_CHOICES,default="image")
    media=models.FileField(upload_to="hero-banners/")
    sort_order=models.PositiveIntegerField(default=0)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=["sort_order","id"]
        verbose_name="Hero Banner"
        verbose_name_plural="Hero Banners"
    def __str__(self): return self.title or f"Hero Banner {self.pk}"


class SiteSettings(models.Model):
    clinic_name=models.CharField(max_length=150,default='Mount Dental Care')
    email=models.EmailField(default='mountdentalcare@gmail.com')
    logo=models.ImageField(upload_to='site/',blank=True,null=True)
    hero_background_image=models.ImageField(upload_to='hero/',blank=True,null=True)
    hero_title=models.CharField(max_length=255,default='Healthy Smiles, Lifelong Confidence')
    hero_description=models.TextField(default='Expert Dental Care with Advanced Technology and Personalized Treatment. Compassionate, gentle care designed for the whole family.')
    metric_dentists=models.CharField(max_length=80,default='15+')
    metric_equipment=models.CharField(max_length=80,default='3D CBCT')
    metric_emi=models.CharField(max_length=80,default='0% EMI')
    metric_patients=models.CharField(max_length=80,default='5,000+')
    # Top bar + footer copy that used to be hard-coded in the React bundle.
    topbar_hours=models.CharField(max_length=200,default='Mon-Sat : Morning - 10.00 AM - 01.00 PM | Evening 05.00 PM - 08.30 PM')
    whatsapp_number=models.CharField(max_length=30,blank=True,default='917010823417',help_text='Digits only, used to build the wa.me chat link.')
    footer_about=models.TextField(default='Providing exceptional, patient-first dental treatments with cutting-edge technology and genuine human warmth. Your smile is our lifelong masterpiece.')
    footer_copyright=models.CharField(max_length=200,blank=True,default='© 2026 Mount Dental Care & Clinic. All rights reserved.')
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return self.clinic_name
    class Meta: verbose_name='Site Settings'; verbose_name_plural='Site Settings'


class EmailTemplate(models.Model):
    """Editable subject/body for the messages the clinic sends.

    ``template_type`` is free text so any number of templates can be added,
    renamed or deleted from Admin. The two built-in types below are the ones
    the site sends automatically; every other name is kept as a reusable
    template. Deleting (or clearing) a built-in template is safe: the sender
    then falls back to the copy bundled with the code, so the appointment OTP
    always goes out (see ``clinic.email_utils.DEFAULTS``).
    """
    BUILTIN_TYPES=[
        ('appointment_otp','Appointment OTP'),
        ('admin_appointment_notify','Admin Appointment Notification'),
    ]
    BUILTIN_TYPE_HELP=(
        'Names the website sends automatically: "appointment_otp" (the patient '
        'verification code) and "admin_appointment_notify" (the new-booking '
        'alert to clinic staff). Any other name is kept as a reusable template.'
    )
    template_type=models.CharField(max_length=60,unique=True,help_text=BUILTIN_TYPE_HELP)
    subject=models.CharField(max_length=255)
    body=models.TextField(help_text='Placeholders: {{otp}}, {{expiry_minutes}}, {{appointment_id}}, {{full_name}}, {{mobile_number}}, {{email}}, {{preferred_date}}, {{treatment_type}}, {{message}}, {{booked_at}}.')
    active=models.BooleanField(default=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return dict(self.BUILTIN_TYPES).get(self.template_type,self.template_type)
    class Meta:
        ordering=['template_type']
        verbose_name='Email Template'
        verbose_name_plural='Email Templates'

class EmailOTP(models.Model):
    email=models.EmailField(db_index=True)
    full_name=models.CharField(max_length=150)
    mobile_number=models.CharField(max_length=50)
    preferred_date=models.DateField()
    treatment_type=models.CharField(max_length=150)
    message=models.TextField(blank=True)
    otp_hash=models.CharField(max_length=128)
    expires_at=models.DateTimeField()
    attempts=models.PositiveSmallIntegerField(default=0)
    verified=models.BooleanField(default=False)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='email_otps')
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.email} — {self.created_at:%Y-%m-%d %H:%M}'

class NavItem(models.Model):
    """A menu link.

    The page section it scrolls to is derived from the label, so there is no
    separate anchor to maintain: "Why Choose Us" opens ``#why-choose-us``.
    """
    label=models.CharField(max_length=80,help_text='Menu text. The link scrolls to the page section with the matching name, e.g. "Why Choose Us" opens #why-choose-us.')
    sort_order=models.PositiveIntegerField(default=0)
    active=models.BooleanField(default=True)
    class Meta: ordering=['sort_order']
    def __str__(self): return self.label

class OfferBanner(models.Model):
    eyebrow=models.CharField(max_length=100,default='LIMITED TIME OFFER')
    title=models.CharField(max_length=255)
    description=models.TextField()
    button_text=models.CharField(max_length=100,default='Claim Offer & Book Today')
    active=models.BooleanField(default=True)
    def __str__(self): return self.title

class Service(models.Model):
    ICON_CHOICES=[(x,x) for x in ['stethoscope','sparkles','sun','activity','shield','layers','smile','baby']]
    icon=models.CharField(max_length=40,choices=ICON_CHOICES,default='sparkles')
    title=models.CharField(max_length=150)
    description=models.TextField()
    # "Learn More" popup copy. Kept on the service itself so adding a new
    # service in Admin automatically gets a fully editable detail panel.
    badge=models.CharField(max_length=150,blank=True,default='')
    full_description=models.TextField(blank=True,default='')
    highlights=models.TextField(blank=True,default='',help_text='One treatment highlight per line.')
    sort_order=models.PositiveIntegerField(default=0)
    active=models.BooleanField(default=True)
    class Meta: ordering=['sort_order']
    def __str__(self): return self.title

class TrustFeature(models.Model):
    icon=models.CharField(max_length=40,default='award')
    title=models.CharField(max_length=150)
    description=models.TextField()
    sort_order=models.PositiveIntegerField(default=0)
    active=models.BooleanField(default=True)
    class Meta: ordering=['sort_order']
    def __str__(self): return self.title

class Doctor(models.Model):
    name=models.CharField(max_length=150)
    role=models.CharField(max_length=255)
    image=models.ImageField(upload_to='doctors/',blank=True,null=True)
    bio=models.TextField(blank=True)
    education=models.CharField(max_length=255,blank=True)
    expertise=models.CharField(max_length=255,blank=True)
    tenure=models.CharField(max_length=255,blank=True)
    memberships=models.CharField(max_length=255,blank=True)
    is_lead=models.BooleanField(default=False)
    sort_order=models.PositiveIntegerField(default=0)
    active=models.BooleanField(default=True)
    class Meta: ordering=['sort_order']
    def __str__(self): return self.name

class GalleryItem(models.Model):
    title=models.CharField(max_length=100,default='INTERVIEW')
    description=models.TextField(blank=True)
    image=models.ImageField(upload_to='gallery/',blank=True,null=True)
    video=models.FileField(upload_to='gallery/videos/',blank=True,null=True)
    sort_order=models.PositiveIntegerField(default=0)
    active=models.BooleanField(default=True)
    class Meta: ordering=['sort_order']
    def __str__(self): return self.title

class ClinicAddress(models.Model):
    label=models.CharField(max_length=80,default='Clinic Location')
    address=models.TextField()
    sort_order=models.PositiveIntegerField(default=0)
    active=models.BooleanField(default=True)
    class Meta: ordering=['sort_order']
    def __str__(self): return self.address

class ClinicHour(models.Model):
    day=models.CharField(max_length=50)
    hours=models.CharField(max_length=100)
    emergency=models.BooleanField(default=False)
    sort_order=models.PositiveIntegerField(default=0)
    class Meta: ordering=['sort_order']
    def __str__(self): return f'{self.day}: {self.hours}'

class FooterLink(models.Model):
    group=models.CharField(max_length=80,choices=[('quick','Quick Links'),('treatments','Key Treatments')])
    label=models.CharField(max_length=150)
    url=models.CharField(max_length=255,default='#home')
    sort_order=models.PositiveIntegerField(default=0)
    active=models.BooleanField(default=True)
    class Meta: ordering=['group','sort_order']
    def __str__(self): return self.label

class PageContent(models.Model):
    key=models.CharField(max_length=80,unique=True)
    eyebrow=models.CharField(max_length=150,blank=True)
    title=models.CharField(max_length=255,blank=True)
    description=models.TextField(blank=True)
    active=models.BooleanField(default=True)
    def __str__(self): return self.key

class Appointment(models.Model):
    STATUS_CHOICES=[('pending','Pending'),('confirmed','Confirmed'),('rescheduled','Rescheduled'),('completed','Completed'),('cancelled','Cancelled')]
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='appointments')
    full_name=models.CharField(max_length=150)
    mobile_number=models.CharField(max_length=50)
    email=models.EmailField()
    preferred_date=models.DateField()
    treatment_type=models.CharField(max_length=150)
    message=models.TextField(blank=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    admin_note=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return f'{self.full_name} — {self.preferred_date}'

class Notification(models.Model):
    TYPE_CHOICES=[('info','Info'),('success','Success'),('warning','Warning'),('appointment','Appointment')]
    # A notification always exists, even when the booking came from a visitor
    # who has not created an account yet. In that case it is held against the
    # email address and is claimed automatically if they register later.
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='notifications')
    email=models.EmailField(blank=True,db_index=True,default='',help_text='Set for guest bookings that are not linked to an account yet.')
    title=models.CharField(max_length=160)
    message=models.TextField()
    notification_type=models.CharField(max_length=30,choices=TYPE_CHOICES,default='info')
    appointment=models.ForeignKey(Appointment,on_delete=models.SET_NULL,null=True,blank=True,related_name='notifications')
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-created_at']
    def recipient(self): return self.user.username if self.user_id else (self.email or 'guest')
    def __str__(self): return f'{self.recipient()}: {self.title}'


class EmailLog(models.Model):
    """Delivery record for the Gmail messages the clinic sends.

    Only the appointment OTP is ever emailed, so this holds one row per OTP
    attempt: the full subject and body, the result, and a link back to the
    patient. Failed sends can be retried from Admin.
    """
    STATUS_CHOICES=[('sent','Sent'),('failed','Failed')]
    template_type=models.CharField(max_length=40)
    recipient=models.EmailField(db_index=True)
    subject=models.CharField(max_length=255,blank=True)
    body=models.TextField(blank=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='sent')
    error=models.TextField(blank=True)
    attempts=models.PositiveSmallIntegerField(default=1)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='email_logs')
    appointment=models.ForeignKey(Appointment,on_delete=models.SET_NULL,null=True,blank=True,related_name='email_logs')
    created_at=models.DateTimeField(auto_now_add=True)
    last_attempt_at=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['-created_at']
        verbose_name='Email log'
        verbose_name_plural='Email logs'
    def __str__(self): return f'{self.recipient} — {self.template_type} ({self.get_status_display()})'


class SiteText(models.Model):
    """A single editable line of website copy.

    Every string that used to be hard-coded in the React bundle (section
    taglines, button captions, contact labels, footer notes...) is seeded here
    as one row, so the clinic can reword any of it from Admin — no deployment
    needed. The frontend looks a block up by ``key`` and falls back to its
    bundled copy when the row is blank, so a section can never render empty.
    """
    GROUP_CHOICES=[
        ('general','General'),
        ('header','Header'),
        ('hero','Hero'),
        ('offer','Offer banner'),
        ('services','Services'),
        ('about','About & mission'),
        ('experts','Experts'),
        ('appointment','Appointment'),
        ('contact','Contact'),
        ('footer','Footer'),
        ('awards','Awards'),
        ('why','Why choose us'),
    ]
    key=models.CharField(max_length=140,unique=True,validators=[text_key_validator],help_text='Stable identifier the website reads. Edit with care — changing it detaches the text from its section.')
    label=models.CharField(max_length=200,blank=True,help_text='What this text is, shown only in Admin.')
    group=models.CharField(max_length=40,choices=GROUP_CHOICES,default='general')
    value=models.TextField(blank=True)
    sort_order=models.PositiveIntegerField(default=0)
    class Meta:
        ordering=['group','sort_order','id']
        verbose_name='Text block'
        verbose_name_plural='Text blocks'
    def __str__(self): return self.label or self.key


class Branch(models.Model):
    """A clinic location used by the top bar, call modal, contact and footer."""
    name=models.CharField(max_length=150)
    phone_display=models.CharField(max_length=80,blank=True,help_text='Shown to visitors, e.g. 044-2234 5000.')
    phone_dial=models.CharField(max_length=30,blank=True,help_text='Digits only, used for tel: links, e.g. 04422345000.')
    address=models.TextField(blank=True)
    map_embed_url=models.URLField(max_length=600,blank=True,help_text='Google Maps embed URL for the contact map.')
    map_directions_url=models.URLField(max_length=600,blank=True,help_text='Google Maps directions URL.')
    is_primary=models.BooleanField(default=False,help_text='The primary branch drives the default map and directions links.')
    sort_order=models.PositiveIntegerField(default=0)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=['sort_order','id']
        verbose_name='Branch'
        verbose_name_plural='Branches'
    def __str__(self): return self.name


class ClinicImage(models.Model):
    """A slide in the clinic tour carousel (Why Choose Us section)."""
    title=models.CharField(max_length=150)
    caption=models.CharField(max_length=200,blank=True)
    image=models.ImageField(upload_to='clinic/',blank=True,null=True)
    sort_order=models.PositiveIntegerField(default=0)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=['sort_order','id']
        verbose_name='Clinic tour image'
        verbose_name_plural='Clinic tour images'
    def __str__(self): return self.title


class YoutubeVideo(models.Model):
    """An embedded YouTube video shown beside the clinic tour carousel."""
    title=models.CharField(max_length=150)
    url=models.URLField(max_length=600,help_text='YouTube embed URL, e.g. https://www.youtube.com/embed/VIDEO_ID')
    sort_order=models.PositiveIntegerField(default=0)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=['sort_order','id']
        verbose_name='YouTube video'
        verbose_name_plural='YouTube videos'
    def __str__(self): return self.title


class Award(models.Model):
    """An academic honour shown in the Awards section."""
    title=models.CharField(max_length=200)
    category=models.CharField(max_length=150,blank=True)
    description=models.TextField(blank=True)
    venue=models.CharField(max_length=200,blank=True)
    event_date=models.CharField(max_length=120,blank=True,help_text='Free text, e.g. 20th January 2008.')
    image=models.ImageField(upload_to='awards/',blank=True,null=True)
    sort_order=models.PositiveIntegerField(default=0)
    active=models.BooleanField(default=True)
    class Meta:
        ordering=['sort_order','id']
        verbose_name='Award'
        verbose_name_plural='Awards'
    def __str__(self): return self.title
