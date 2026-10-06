"""Patient records, and the single Gmail message the clinic sends.

Gmail is used for **one thing only**: the 4-digit appointment verification code.

Everything else a patient sees — appointment status changes, clinic messages
written in Django Admin — is stored as a ``Notification`` row in the panel.
Nothing else is emailed to them.
"""

from .email_utils import render_template, send_raw_email
from .models import EmailLog, Notification


def send_and_log(template_type, recipient, context, user=None, appointment=None):
    """Send one templated Gmail message and record the outcome in EmailLog."""
    recipient = (recipient or '').strip()
    if not recipient:
        return None
    subject, body = render_template(template_type, context)
    log = EmailLog.objects.create(
        template_type=template_type,
        recipient=recipient,
        subject=subject,
        body=body,
        user=user,
        appointment=appointment,
    )
    try:
        send_raw_email(subject, body, recipient)
    except Exception as exc:
        log.status = 'failed'
        log.error = str(exc)
        log.save(update_fields=['status', 'error'])
        print(f"[EMAIL] {template_type} to {recipient} failed: {exc}")
    return log


def record_notification(*, recipient, title, message, user=None, appointment=None,
                        notification_type='appointment'):
    """Store a patient notification for the panel. No email is sent.

    It is linked to the account when the patient has one, and otherwise held
    against their email address until they register.
    """
    return Notification.objects.create(
        user=user,
        email='' if user else recipient,
        title=title,
        message=message,
        notification_type=notification_type,
        appointment=appointment,
    )


def send_admin_appointment_email(appointment):
    """Email every admin/staff member the full details of a new appointment.

    Admin email addresses are collected from:
    1. The ``SiteSettings.email`` field (the clinic's main contact email).
    2. All Django superusers who have an email address on file.

    Duplicate addresses are de-duplicated so no one gets the same mail twice.
    The email uses the ``admin_appointment_notify`` template which can be
    customised from the Admin panel (Email Templates section).
    """
    from django.contrib.auth.models import User as AuthUser
    from .models import SiteSettings

    from django.conf import settings as django_settings

    # Collect admin emails ─────────────────────────────────────────────────────
    admin_emails = set()

    # 1) Notification / Host email configured in settings / environment
    admin_env_email = getattr(django_settings, 'ADMIN_NOTIFICATION_EMAIL', '') or getattr(django_settings, 'EMAIL_HOST_USER', '')
    if admin_env_email and admin_env_email.strip():
        admin_emails.add(admin_env_email.strip().lower())

    # 2) Clinic email from SiteSettings (skip demo dummy addresses if unreachable)
    site = SiteSettings.objects.first()
    if site and site.email:
        email_clean = site.email.strip().lower()
        # Avoid sending to demo / placeholder domain if not real
        if not email_clean.endswith('@mountdentalcare.com'):
            admin_emails.add(email_clean)

    # 3) Superusers with a valid real email address
    for email in (AuthUser.objects
                  .filter(is_superuser=True, is_active=True)
                  .exclude(email='')
                  .values_list('email', flat=True)):
        clean = email.strip().lower()
        if clean not in ('admin@example.com', 'admin@gmail.com', 'root@localhost'):
            admin_emails.add(clean)

    # Fallback to EMAIL_HOST_USER if all collected were filtered out
    if not admin_emails and getattr(django_settings, 'EMAIL_HOST_USER', None):
        admin_emails.add(django_settings.EMAIL_HOST_USER.strip().lower())

    if not admin_emails:
        print("[ADMIN EMAIL] No valid admin email addresses found. Skipping admin notification.")
        return

    # Build context ─────────────────────────────────────────────────────────────
    pref_date = appointment.preferred_date
    pref_date_str = pref_date.strftime('%d/%m/%Y') if hasattr(pref_date, 'strftime') else str(pref_date)
    booked_at_str = appointment.created_at.strftime('%d/%m/%Y, %I:%M %p') if appointment.created_at else ''

    context = {
        'full_name': appointment.full_name,
        'mobile_number': appointment.mobile_number,
        'email': appointment.email,
        'preferred_date': pref_date_str,
        'treatment_type': appointment.treatment_type,
        'message': appointment.message or '(none)',
        'booked_at': booked_at_str,
        'appointment_id': str(appointment.pk),
    }

    # Send to each admin ────────────────────────────────────────────────────────
    for admin_email in admin_emails:
        try:
            send_and_log(
                'admin_appointment_notify',
                admin_email,
                context,
                appointment=appointment,
            )
            print(f"[ADMIN EMAIL] Appointment #{appointment.pk} notification sent to {admin_email}")
        except Exception as exc:
            print(f"[ADMIN EMAIL] Failed to notify {admin_email}: {exc}")


def resend_email_log(log):
    """Retry a stored message — used for a failed OTP send. Returns the log."""
    log.attempts += 1
    try:
        send_raw_email(log.subject, log.body, log.recipient)
        log.status = 'sent'
        log.error = ''
    except Exception as exc:
        log.status = 'failed'
        log.error = str(exc)
    log.save(update_fields=['status', 'error', 'attempts', 'last_attempt_at'])
    return log
