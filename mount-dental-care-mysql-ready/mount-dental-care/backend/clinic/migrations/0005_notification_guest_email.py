import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def backfill(apps, schema_editor):
    """Give appointments booked before this change their notification back."""
    Appointment = apps.get_model('clinic', 'Appointment')
    Notification = apps.get_model('clinic', 'Notification')
    for appointment in Appointment.objects.filter(notifications__isnull=True):
        Notification.objects.create(
            user_id=appointment.user_id,
            email='' if appointment.user_id else appointment.email,
            title='Appointment Request Received',
            message=(
                f'Your {appointment.treatment_type} appointment request for '
                f'{appointment.preferred_date} has been received. '
                'Our coordinator will contact you soon.'
            ),
            notification_type='appointment',
            appointment=appointment,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0004_alter_emailtemplate_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='email',
            field=models.EmailField(
                blank=True,
                db_index=True,
                default='',
                help_text='Set for guest bookings that are not linked to an account yet.',
                max_length=254,
            ),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='notifications',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(backfill, migrations.RunPython.noop),
    ]
