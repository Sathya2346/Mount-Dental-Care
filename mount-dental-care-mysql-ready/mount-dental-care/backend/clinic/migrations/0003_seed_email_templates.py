from django.db import migrations

DEFAULTS=[
 ('appointment_otp','Your Mount Dental Care verification code is {{otp}}','Hello {{full_name}},\n\nYour Mount Dental Care appointment verification code is: {{otp}}\n\nThis code expires in {{expiry_minutes}} minutes. Do not share this code with anyone.\n\nAppointment date: {{preferred_date}}\nTreatment: {{treatment_type}}\n\nMount Dental Care'),
 ('appointment_received','Appointment request received — Mount Dental Care','Hello {{full_name}},\n\nWe received your appointment request.\n\nDate: {{preferred_date}}\nTreatment: {{treatment_type}}\n\nOur patient coordinator will contact you shortly.\n\nMount Dental Care'),
 ('appointment_status','Appointment {{status}} — Mount Dental Care','Hello {{full_name}},\n\nYour appointment status is now: {{status}}.\n\nDate: {{preferred_date}}\nTreatment: {{treatment_type}}\n\n{{admin_note}}\n\nMount Dental Care'),
]

def seed(apps,schema_editor):
    EmailTemplate=apps.get_model('clinic','EmailTemplate')
    for template_type,subject,body in DEFAULTS:
        EmailTemplate.objects.get_or_create(template_type=template_type,defaults={'subject':subject,'body':body,'active':True})

def unseed(apps,schema_editor):
    apps.get_model('clinic','EmailTemplate').objects.all().delete()

class Migration(migrations.Migration):
    dependencies=[('clinic','0002_herobanner')]
    operations=[migrations.RunPython(seed,unseed)]
