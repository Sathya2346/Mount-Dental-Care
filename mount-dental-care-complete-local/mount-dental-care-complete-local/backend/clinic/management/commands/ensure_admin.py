import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Create (or repair) the admin account from environment variables.

    A hosting platform cannot prompt for a password, so the superuser that
    opens Django Admin is created here instead of with the interactive
    ``createsuperuser`` command. The command is idempotent: run it on every
    deploy and it only touches what is missing, so a password changed in the
    admin panel is never overwritten unless ADMIN_RESET_PASSWORD=true.

    Required env vars:
        DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD
    Optional:
        DJANGO_SUPERUSER_EMAIL, ADMIN_RESET_PASSWORD
    """

    help = "Create or repair the Django Admin superuser from environment variables."

    def add_arguments(self, parser):
        parser.add_argument(
            "--username", default=os.getenv("DJANGO_SUPERUSER_USERNAME", ""),
            help="Defaults to the DJANGO_SUPERUSER_USERNAME environment variable.",
        )
        parser.add_argument(
            "--email", default=os.getenv("DJANGO_SUPERUSER_EMAIL", ""),
            help="Defaults to the DJANGO_SUPERUSER_EMAIL environment variable.",
        )
        parser.add_argument(
            "--password", default=os.getenv("DJANGO_SUPERUSER_PASSWORD", ""),
            help="Defaults to the DJANGO_SUPERUSER_PASSWORD environment variable.",
        )

    def handle(self, *args, **options):
        username = (options.get("username") or "").strip()
        email = (options.get("email") or "").strip()
        password = options.get("password") or ""
        reset = os.getenv("ADMIN_RESET_PASSWORD", "").lower() == "true"

        if not username:
            self.stdout.write(
                "Skipped: set DJANGO_SUPERUSER_USERNAME (and "
                "DJANGO_SUPERUSER_PASSWORD) to create the admin account."
            )
            return

        user = User.objects.filter(username__iexact=username).first()
        if user is None:
            if not password:
                self.stderr.write(
                    f"Cannot create \"{username}\": DJANGO_SUPERUSER_PASSWORD is empty."
                )
                return
            user = User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Created superuser "{user.username}".'))
            return

        changed = []
        if not user.is_superuser:
            user.is_superuser = True
            changed.append("is_superuser")
        if not user.is_staff:
            user.is_staff = True
            changed.append("is_staff")
        if email and user.email != email:
            user.email = email
            changed.append("email")
        if reset and password:
            user.set_password(password)
            changed.append("password")
        if changed:
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Updated superuser "{user.username}" ({", ".join(changed)}).'
                )
            )
        else:
            self.stdout.write(f'Superuser "{user.username}" already exists — left unchanged.')
