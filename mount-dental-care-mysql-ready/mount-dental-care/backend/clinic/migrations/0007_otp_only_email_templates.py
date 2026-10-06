from django.db import migrations, models

# Gmail now sends the appointment verification code and nothing else, so the
# other templates are removed. They are recreated by reverse() if needed.
REMOVED_TYPES = ('appointment_received', 'appointment_status', 'patient_message')

RESTORE = {
    'appointment_received': (
        'Appointment request received — Mount Dental Care',
        'Hello {{full_name}},\n\nWe received your appointment request.\n\nDate: {{preferred_date}}\nTreatment: {{treatment_type}}\n\nOur patient coordinator will contact you shortly.\n\nMount Dental Care',
    ),
    'appointment_status': (
        'Appointment {{status}} — Mount Dental Care',
        'Hello {{full_name}},\n\nYour appointment status is now: {{status}}.\n\nDate: {{preferred_date}}\nTreatment: {{treatment_type}}\n\n{{admin_note}}\n\nMount Dental Care',
    ),
    'patient_message': (
        'Message from Mount Dental Care — {{title}}',
        'Hello {{full_name}},\n\n{{message}}\n\nIf you have any questions, simply reply to this email.\n\nMount Dental Care',
    ),
}


def remove_unused_templates(apps, schema_editor):
    EmailTemplate = apps.get_model('clinic', 'EmailTemplate')
    EmailTemplate.objects.filter(template_type__in=REMOVED_TYPES).delete()


def restore_templates(apps, schema_editor):
    EmailTemplate = apps.get_model('clinic', 'EmailTemplate')
    for template_type, (subject, body) in RESTORE.items():
        EmailTemplate.objects.get_or_create(
            template_type=template_type,
            defaults={'subject': subject, 'body': body, 'active': True},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0006_email_log_and_patient_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='template_type',
            field=models.CharField(
                choices=[('appointment_otp', 'Appointment OTP')],
                max_length=40,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='body',
            field=models.TextField(
                help_text='Use placeholders such as {{otp}}, {{expiry_minutes}}, {{full_name}}, {{mobile_number}}, {{email}}, {{preferred_date}}, {{treatment_type}}, {{message}}.'
            ),
        ),
        migrations.RunPython(remove_unused_templates, restore_templates),
    ]
