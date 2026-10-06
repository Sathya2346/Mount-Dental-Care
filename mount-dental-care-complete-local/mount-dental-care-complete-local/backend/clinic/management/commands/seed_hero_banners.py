from django.core.management.base import BaseCommand

from clinic.models import HeroBanner
from clinic.seeding import HERO_BANNERS, install_media


class Command(BaseCommand):
    help = "Create/update the bundled Mount Dental Care hero carousel banners."

    def handle(self, *args, **options):
        copied, kept = install_media()
        self.stdout.write(f"Media: {copied} file(s) installed, {kept} kept.")

        # Older seed versions created untitled banners pointing at gallery photos.
        HeroBanner.objects.filter(title="").delete()

        for title, media_type, media, order in HERO_BANNERS:
            HeroBanner.objects.update_or_create(
                title=title,
                defaults={
                    "media_type": media_type,
                    "media": media,
                    "sort_order": order,
                    "active": True,
                },
            )
            self.stdout.write(self.style.SUCCESS(f"Ready: {title}"))

        self.stdout.write(self.style.SUCCESS(
            f"Hero carousel is ready with {len(HERO_BANNERS)} bundled media items."
        ))
