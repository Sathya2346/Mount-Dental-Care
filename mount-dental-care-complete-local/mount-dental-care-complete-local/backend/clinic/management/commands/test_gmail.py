from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Send a test email using the configured Gmail SMTP settings.'
    def add_arguments(self, parser):
        parser.add_argument('recipient')
    def handle(self, *args, **opts):
        recipient = opts['recipient']
        user = (getattr(settings,'EMAIL_HOST_USER','') or '').strip()
        password = (getattr(settings,'EMAIL_HOST_PASSWORD','') or '').replace(' ','').strip()
        if not user or user.lower().startswith('your'):
            raise CommandError('EMAIL_HOST_USER is not configured in backend/.env')
        if not password or password.lower().startswith('your'):
            raise CommandError('EMAIL_HOST_PASSWORD is not configured in backend/.env')
        try:
            sent = send_mail('Mount Dental Care Gmail test', 'Gmail SMTP is configured correctly. OTP delivery can now use this account.', user, [recipient], fail_silently=False)
        except Exception as exc:
            raise CommandError(f'Gmail SMTP test failed: {exc}')
        self.stdout.write(self.style.SUCCESS(f'Test email sent to {recipient} ({sent} message).'))
