from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from .models import *
from .notifications import record_notification, resend_email_log

admin.site.site_header = 'Mount Dental Care — Administration'
admin.site.site_title = 'Mount Dental Care Admin'
admin.site.index_title = 'Website & Appointment Management'

def preview_file(obj, field, width=140):
    f = getattr(obj, field, None)
    if not f:
        return '—'
    try:
        return format_html('<a href="{}" target="_blank"><img src="{}" style="max-width:{}px;max-height:90px;object-fit:contain;border:1px solid #ddd;border-radius:8px;padding:3px;background:#fff" /></a>', f.url, f.url, width)
    except Exception:
        return 'Uploaded'

@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display=("title","media_type","media_thumb","sort_order","active")
    list_editable=("sort_order","active")
    list_filter=("media_type","active")
    search_fields=("title",)
    readonly_fields=("media_preview",)
    fields=("title","media_type","media","media_preview","sort_order","active")
    def media_thumb(self,obj):
        if not obj.media: return "—"
        if obj.media_type == "image": return preview_file(obj,"media",90)
        return format_html('<a href="{}" target="_blank">Open video</a>',obj.media.url)
    def media_preview(self,obj):
        if not obj.media: return "—"
        if obj.media_type == "image": return preview_file(obj,"media",420)
        return format_html('<video src="{}" controls style="max-width:520px;max-height:280px"></video>',obj.media.url)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    # Branch phone numbers are edited under Branches (they fill the top bar, the
    # call popup and the footer), so this form only carries the brand, hero,
    # metrics and top-bar/footer copy the page actually renders.
    fieldsets = (
        ('Brand & Contact', {
            'fields': ('clinic_name','logo','logo_preview','email'),
            'description': 'Branch phone numbers are edited under Branches, which fills the top bar, the call popup and the footer.',
        }),
        ('Hero', {'fields': ('hero_background_image','hero_background_preview','hero_title','hero_description')}),
        ('Metrics', {'fields': ('metric_dentists','metric_equipment','metric_emi','metric_patients')}),
        ('Top Bar & Footer', {'fields': ('topbar_hours','whatsapp_number','footer_about','footer_copyright')}),
    )
    readonly_fields = ('logo_preview','hero_background_preview')
    def has_add_permission(self, request): return not SiteSettings.objects.exists()
    def logo_preview(self, obj): return preview_file(obj, 'logo')
    def hero_background_preview(self, obj): return preview_file(obj, 'hero_background_image')

class OrderedAdmin(admin.ModelAdmin):
    list_display = ('__str__','sort_order','active')
    list_editable = ('sort_order','active')
    list_per_page = 50

@admin.register(NavItem)
class NavItemAdmin(OrderedAdmin):
    search_fields=('label',)
@admin.register(OfferBanner)
class OfferBannerAdmin(admin.ModelAdmin): list_display=('title','active'); list_editable=('active',)
@admin.register(Service)
class ServiceAdmin(OrderedAdmin):
    search_fields=('title','description')
    list_display=('__str__','icon','sort_order','active')
    fieldsets=(
        ('Card', {'fields': ('icon','title','description')}),
        ('"Learn More" popup', {'fields': ('badge','full_description','highlights'),
                                 'description': 'These fields fill the popup opened by a service card. Leave them blank to fall back to sensible defaults.'}),
        ('Display', {'fields': ('sort_order','active')}),
    )
@admin.register(TrustFeature)
class TrustFeatureAdmin(OrderedAdmin): search_fields=('title','description')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display=('name','role','image_thumb','is_lead','sort_order','active')
    list_editable=('is_lead','sort_order','active')
    search_fields=('name','role')
    readonly_fields=('image_preview',)
    fields=('name','role','image','image_preview','bio','education','expertise','tenure','memberships','is_lead','sort_order','active')
    def image_thumb(self,obj): return preview_file(obj,'image',80)
    def image_preview(self,obj): return preview_file(obj,'image',220)

@admin.register(GalleryItem)
class GalleryAdmin(admin.ModelAdmin):
    list_display=('title','media_thumb','has_video','sort_order','active')
    list_editable=('sort_order','active')
    search_fields=('title','description')
    readonly_fields=('image_preview','video_preview')
    fields=('title','description','image','image_preview','video','video_preview','sort_order','active')
    def media_thumb(self,obj): return preview_file(obj,'image',90) if obj.image else ('Video uploaded' if obj.video else '—')
    def has_video(self,obj): return bool(obj.video)
    has_video.boolean=True
    def image_preview(self,obj): return preview_file(obj,'image',220)
    def video_preview(self,obj):
        return format_html('<a href="{}" target="_blank">Open uploaded video</a>', obj.video.url) if obj.video else '—'

admin.site.register(ClinicAddress,OrderedAdmin)
admin.site.register(ClinicHour)
admin.site.register(FooterLink,OrderedAdmin)

@admin.register(SiteText)
class SiteTextAdmin(admin.ModelAdmin):
    list_display=('label','key','group','preview','sort_order')
    list_filter=('group',)
    list_editable=('sort_order',)
    search_fields=('key','label','value')
    ordering=('group','sort_order')
    fields=('key','label','group','value','sort_order')
    def preview(self,obj):
        text=(obj.value or '').strip().replace('\n',' ')
        return (text[:70]+'…') if len(text)>70 else (text or '—')

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display=('name','phone_display','is_primary','sort_order','active')
    list_editable=('is_primary','sort_order','active')
    search_fields=('name','phone_display','address')
    fields=('name','phone_display','phone_dial','address','is_primary','sort_order','active',
            'map_embed_url','map_directions_url')

@admin.register(ClinicImage)
class ClinicImageAdmin(admin.ModelAdmin):
    list_display=('title','caption','thumb','sort_order','active')
    list_editable=('sort_order','active')
    search_fields=('title','caption')
    readonly_fields=('image_preview',)
    fields=('title','caption','image','image_preview','sort_order','active')
    def thumb(self,obj): return preview_file(obj,'image',90)
    def image_preview(self,obj): return preview_file(obj,'image',260)

@admin.register(YoutubeVideo)
class YoutubeVideoAdmin(admin.ModelAdmin):
    list_display=('title','url','sort_order','active')
    list_editable=('sort_order','active')
    search_fields=('title','url')

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display=('title','category','event_date','thumb','sort_order','active')
    list_editable=('sort_order','active')
    search_fields=('title','category','venue','description')
    readonly_fields=('image_preview',)
    fields=('title','category','description','venue','event_date','image','image_preview','sort_order','active')
    def thumb(self,obj): return preview_file(obj,'image',90)
    def image_preview(self,obj): return preview_file(obj,'image',260)

@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display=('key','title','active')
    list_editable=('active',)
    search_fields=('key','title','description')
    fields=('key','eyebrow','title','description','active')


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display=('kind','template_type','subject','active','updated_at')
    list_filter=('template_type','active')
    search_fields=('template_type','subject','body')
    ordering=('template_type',)
    fieldsets=(
        ('Template', {'fields':('template_type','active','subject','body'),
                      'description':'Add as many templates as you like. The two built-in names are the ones the website sends automatically.'}),
        ('Available placeholders', {'fields':('placeholder_help',)}),
    )
    readonly_fields=('placeholder_help',)
    @admin.display(description='Kind', ordering='template_type')
    def kind(self,obj):
        return dict(EmailTemplate.BUILTIN_TYPES).get(obj.template_type,'Custom template')
    def placeholder_help(self,obj):
        return mark_safe(
            '<p style="margin:0 0 8px">Type <code>{{name}}</code> in the subject or body and it is replaced when the message is sent.</p>'
            '<b>appointment_otp</b> — emailed to the patient:<br>'
            '{{otp}}, {{expiry_minutes}}, {{full_name}}, {{mobile_number}}, {{email}}, {{preferred_date}}, {{treatment_type}}, {{message}}<br><br>'
            '<b>admin_appointment_notify</b> — emailed to clinic staff:<br>'
            '{{appointment_id}}, {{full_name}}, {{mobile_number}}, {{email}}, {{preferred_date}}, {{treatment_type}}, {{message}}, {{booked_at}}'
        )

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display=('full_name','mobile_number','email','preferred_date_fmt','treatment_type','status','created_at_fmt')
    list_filter=('status','treatment_type','created_at')
    search_fields=('full_name','mobile_number','email','message','admin_note')
    readonly_fields=('created_at','updated_at')
    fieldsets=(('Patient',{'fields':('user','full_name','mobile_number','email')}),('Appointment',{'fields':('preferred_date','treatment_type','message','status','admin_note')}),('Timestamps',{'fields':('created_at','updated_at')}))

    @admin.display(description='Preferred Date', ordering='preferred_date')
    def preferred_date_fmt(self, obj):
        return obj.preferred_date.strftime('%d/%m/%Y') if obj.preferred_date else '-'

    @admin.display(description='Booked At', ordering='created_at')
    def created_at_fmt(self, obj):
        return obj.created_at.strftime('%d/%m/%Y, %I:%M %p') if obj.created_at else '-'

    def save_model(self,request,obj,form,change):
        old_status=None
        old_note=None
        if obj.pk:
            old=Appointment.objects.get(pk=obj.pk); old_status=old.status; old_note=old.admin_note
        super().save_model(request,obj,form,change)
        changed = (not change) or old_status != obj.status or old_note != obj.admin_note
        if not changed:
            return
        label=dict(Appointment.STATUS_CHOICES).get(obj.status,obj.status.title())
        message=obj.admin_note or f'Your appointment request is now {label.lower()}.'
        # Panel notification only. Gmail is reserved for the OTP, so a status
        # change never emails the patient.
        record_notification(
            recipient=obj.email,
            title=f'Appointment {label}',
            message=message,
            user=obj.user,
            appointment=obj,
        )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display=('user','email','title','notification_type','is_read','created_at')
    list_filter=('notification_type','is_read','created_at')
    search_fields=('user__username','user__email','email','title','message')
    autocomplete_fields=('user','appointment')
    fieldsets=(
        ('Recipient',{'fields':('user','email'),'description':'Set a user for registered patients, or an email address for guest bookings.'}),
        ('Notification',{'fields':('title','message','notification_type','appointment','is_read')}),
    )

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    # NOTE: no date_hierarchy — MySQL/MariaDB without the time zone tables
    # loaded raises "Database returned an invalid datetime value".
    list_display=('recipient','template_type','subject','status','attempts','user','appointment','created_at')
    list_filter=('status','template_type','created_at')
    search_fields=('recipient','subject','body','error','user__username','user__email')
    readonly_fields=('template_type','recipient','subject','body','status','error','attempts','user','appointment','created_at','last_attempt_at')
    actions=('resend_selected',)
    def has_add_permission(self,request): return False
    @admin.action(description='Resend selected OTP emails via Gmail')
    def resend_selected(self,request,queryset):
        sent=failed=0
        for log in queryset:
            resend_email_log(log)
            if log.status=='sent': sent+=1
            else: failed+=1
        self.message_user(request, f'Resent {sent} OTP email(s) via Gmail; {failed} still failing.', level=messages.SUCCESS if not failed else messages.WARNING)


admin.site.unregister(User)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('username','email','first_name','last_name','is_active','date_joined')
    search_fields=('username','email','first_name','last_name')
