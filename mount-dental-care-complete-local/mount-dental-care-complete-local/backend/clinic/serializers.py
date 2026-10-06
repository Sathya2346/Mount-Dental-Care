from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

def _versioned_url(serializer, file_field):
    """Absolute media URL with a ``?v=<mtime>`` cache-buster, or ``None``."""
    if not file_field:
        return None
    req = serializer.context.get('request')
    url = req.build_absolute_uri(file_field.url) if req else file_field.url
    try:
        stamp = int(file_field.storage.get_modified_time(file_field.name).timestamp())
        return f"{url}?v={stamp}"
    except Exception:
        return url


class UserSerializer(serializers.ModelSerializer):
    class Meta: model=User; fields=['id','username','first_name','last_name','email']

class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=150)
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True,min_length=6)
    first_name=serializers.CharField(max_length=80,required=False,allow_blank=True)
    last_name=serializers.CharField(max_length=80,required=False,allow_blank=True)
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class PageContentSerializer(serializers.ModelSerializer):
    class Meta: model=PageContent; fields=['key','eyebrow','title','description']

class AppointmentSerializer(serializers.ModelSerializer):
    preferred_date = serializers.DateField(format='%d/%m/%Y', input_formats=['%Y-%m-%d', '%d/%m/%Y'])
    created_at = serializers.DateTimeField(format='%d/%m/%Y, %I:%M %p', read_only=True)
    updated_at = serializers.DateTimeField(format='%d/%m/%Y, %I:%M %p', read_only=True)
    class Meta:
        model=Appointment
        fields=['id','full_name','mobile_number','email','preferred_date','treatment_type','message','status','admin_note','created_at','updated_at']
        read_only_fields=['id','status','admin_note','created_at','updated_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields=['id','title','message','notification_type','appointment','is_read','created_at']

class HeroBannerSerializer(serializers.ModelSerializer):
    media=serializers.SerializerMethodField()
    def get_media(self,o):
        if not o.media: return None
        req = self.context.get('request')
        url = req.build_absolute_uri(o.media.url) if req else o.media.url
        try:
            stamp=int(o.media.storage.get_modified_time(o.media.name).timestamp())
            return f"{url}?v={stamp}"
        except Exception:
            return url
    class Meta:
        model=HeroBanner
        fields=["id","title","media_type","media","sort_order"]


class SiteSerializer(serializers.ModelSerializer):
    logo=serializers.SerializerMethodField(); hero_background_image=serializers.SerializerMethodField()
    def img(self,obj,field):
        f=getattr(obj,field)
        if not f: return None
        req = self.context.get('request')
        url = req.build_absolute_uri(f.url) if req else f.url
        try:
            stamp=int(f.storage.get_modified_time(f.name).timestamp())
            return f"{url}?v={stamp}"
        except Exception:
            return url
    def get_logo(self,o): return self.img(o,'logo')
    def get_hero_background_image(self,o): return self.img(o,'hero_background_image')
    class Meta: model=SiteSettings; fields='__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta: model=Service; fields=['id','icon','title','description','badge','full_description','highlights','sort_order']
class SiteTextSerializer(serializers.ModelSerializer):
    class Meta: model=SiteText; fields=['key','label','group','value','sort_order']
class BranchSerializer(serializers.ModelSerializer):
    class Meta: model=Branch; fields=['id','name','phone_display','phone_dial','address','map_embed_url','map_directions_url','is_primary','sort_order']
class ClinicImageSerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()
    def get_image(self,o): return _versioned_url(self,o.image)
    class Meta: model=ClinicImage; fields=['id','title','caption','image','sort_order']
class YoutubeVideoSerializer(serializers.ModelSerializer):
    class Meta: model=YoutubeVideo; fields=['id','title','url','sort_order']
class AwardSerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()
    def get_image(self,o): return _versioned_url(self,o.image)
    class Meta: model=Award; fields=['id','title','category','description','venue','event_date','image','sort_order']
class TrustSerializer(serializers.ModelSerializer):
    class Meta: model=TrustFeature; fields=['icon','title','description','sort_order']
class DoctorSerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()
    def get_image(self,o):
        if not o.image: return None
        req = self.context.get('request')
        url = req.build_absolute_uri(o.image.url) if req else o.image.url
        try:
            stamp=int(o.image.storage.get_modified_time(o.image.name).timestamp())
            return f"{url}?v={stamp}"
        except Exception:
            return url
    class Meta: model=Doctor; fields=['id','name','role','image','bio','education','expertise','tenure','memberships','is_lead','sort_order']
class GallerySerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField(); video=serializers.SerializerMethodField()
    def get_file(self,o,field):
        f=getattr(o,field)
        if not f: return None
        req = self.context.get('request')
        url = req.build_absolute_uri(f.url) if req else f.url
        try:
            stamp=int(f.storage.get_modified_time(f.name).timestamp())
            return f"{url}?v={stamp}"
        except Exception:
            return url
    def get_image(self,o): return self.get_file(o,'image')
    def get_video(self,o): return self.get_file(o,'video')
    class Meta: model=GalleryItem; fields=['id','title','description','image','video','sort_order']
class AddressSerializer(serializers.ModelSerializer):
    class Meta: model=ClinicAddress; fields=['label','address','sort_order']
class HourSerializer(serializers.ModelSerializer):
    class Meta: model=ClinicHour; fields=['day','hours','emergency','sort_order']
class FooterSerializer(serializers.ModelSerializer):
    class Meta: model=FooterLink; fields=['group','label','url','sort_order']
