import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

PATIENT_MESSAGE = {
    'template_type': 'patient_message',
    'subject': 'Message from Mount Dental Care — {{title}}',
    'body': (
        'Hello {{full_name}},\n\n'
        '{{message}}\n\n'
        'If you have any questions, simply reply to this email.\n\n'
        'Mount Dental Care'
    ),
}


def seed_patient_message(apps, schema_editor):
    EmailTemplate = apps.get_model('clinic', 'EmailTemplate')
    EmailTemplate.objects.get_or_create(
        template_type=PATIENT_MESSAGE['template_type'],
        defaults={
            'subject': PATIENT_MESSAGE['subject'],
            'body': PATIENT_MESSAGE['body'],
            'active': True,
        },
    )


def unseed_patient_message(apps, schema_editor):
    apps.get_model('clinic', 'EmailTemplate').objects.filter(
        template_type=PATIENT_MESSAGE['template_type']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0005_notification_guest_email'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='template_type',
            field=models.CharField(
                choices=[
                    ('appointment_otp', 'Appointment OTP'),
                    ('appointment_received', 'Appointment Received'),
                    ('appointment_status', 'Appointment Status Update'),
                    ('patient_message', 'Message to Patient'),
                ],
                max_length=40,
                unique=True,
            ),
        ),
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_type', models.CharField(max_length=40)),
                ('recipient', models.EmailField(db_index=True, max_length=254)),
                ('subject', models.CharField(blank=True, max_length=255)),
                ('body', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('sent', 'Sent'), ('failed', 'Failed')], default='sent', max_length=10)),
                ('error', models.TextField(blank=True)),
                ('attempts', models.PositiveSmallIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_attempt_at', models.DateTimeField(auto_now=True)),
                ('appointment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='email_logs', to='clinic.appointment')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='email_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Email log',
                'verbose_name_plural': 'Email logs',
                'ordering': ['-created_at'],
            },
        ),
        migrations.RunPython(seed_patient_message, unseed_patient_message),
    ]
