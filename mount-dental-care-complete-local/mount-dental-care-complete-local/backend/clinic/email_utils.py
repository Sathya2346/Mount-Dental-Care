from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .models import EmailTemplate

# Gmail is used for exactly one message: the appointment verification code.
# Nothing else is emailed to patients.
DEFAULTS = {
    'appointment_otp': {
        'subject': 'Your Mount Dental Care verification code is {{otp}}',
        'body': '''Hello {{full_name}},\n\nYour Mount Dental Care appointment verification code is: {{otp}}\n\nThis code expires in {{expiry_minutes}} minutes. Do not share this code with anyone.\n\nAppointment date: {{preferred_date}}\nTreatment: {{treatment_type}}\n\nMount Dental Care'''
    },
    'admin_appointment_notify': {
        'subject': 'New Appointment Booking - {{full_name}} ({{treatment_type}})',
        'body': '''A new appointment has been booked on Mount Dental Care.\n\n--- Patient Details ---\nName: {{full_name}}\nMobile: {{mobile_number}}\nEmail: {{email}}\nPreferred Date: {{preferred_date}}\nTreatment: {{treatment_type}}\nMessage: {{message}}\n\nBooked at: {{booked_at}}\nAppointment ID: {{appointment_id}}\n\nPlease log in to the admin panel to review and confirm this appointment.\n\n-- Mount Dental Care System'''
    },
}


def render_template(template_type, context):
    """Return the subject/body for a template with placeholders replaced."""
    obj = EmailTemplate.objects.filter(template_type=template_type, active=True).first()
    default = DEFAULTS.get(template_type, {'subject': '', 'body': ''})
    subject = obj.subject if obj else default['subject']
    body = obj.body if obj else default['body']
    for key, value in context.items():
        subject = subject.replace('{{'+key+'}}', str(value if value is not None else ''))
        body = body.replace('{{'+key+'}}', str(value if value is not None else ''))
    return subject, body


def gmail_credentials():
    """Validate and return the Gmail SMTP settings, or raise a readable error.

    The OTP is the only way a patient can confirm an appointment, so a missing
    mailbox is a configuration error rather than a silent no-op.
    """
    from_email = (getattr(settings, 'DEFAULT_FROM_EMAIL', '') or getattr(settings, 'EMAIL_HOST_USER', '')).strip()
    username = (getattr(settings, 'EMAIL_HOST_USER', '') or '').strip()
    password = (getattr(settings, 'EMAIL_HOST_PASSWORD', '') or '').replace(' ', '').strip()
    if not username or username.lower().startswith('your'):
        raise RuntimeError('EMAIL_HOST_USER is not configured. Edit backend/.env and set it to the Gmail address that will send OTPs.')
    if not password or password.lower().startswith('your'):
        raise RuntimeError('EMAIL_HOST_PASSWORD is not configured. Generate a Gmail App Password and put the 16-character value in backend/.env.')
    if not from_email:
        raise RuntimeError('DEFAULT_FROM_EMAIL is not configured in backend/.env.')
    return from_email


def send_raw_email(subject, body, to_email):
    """Send a fully rendered Gmail message. Returns the subject."""
    if not to_email:
        raise RuntimeError('No recipient email address was provided.')
    msg = EmailMultiAlternatives(subject, body, gmail_credentials(), [to_email])
    msg.send(fail_silently=False)
    return subject
