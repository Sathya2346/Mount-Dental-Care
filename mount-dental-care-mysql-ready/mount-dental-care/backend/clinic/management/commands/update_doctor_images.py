import os
from pathlib import Path
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand

from clinic.models import Doctor
from clinic.seeding import sync_sample_media


class Command(BaseCommand):
    help = (
        "Replace the seeded doctor photos from the project's sample/ folder "
        "(natesh.jpg, padmini.jpg) without "
        "resetting any other CMS content."
    )

    # Doctor name -> bundled photo file name. Photos are dropped into sample/
    # using these names, then published to MEDIA_ROOT and linked to the row.
    IMAGE_MAP = {
        "Dr. S. NATESH M.D.S.": "natesh.jpg",
        "Dr. N. PADMINI M.D.S.": "padmini.jpg",
    }

    def handle(self, *args, **options):
        seed_dir = Path(settings.BASE_DIR) / "seed_media" / "doctors"
        media_dir = Path(settings.MEDIA_ROOT) / "doctors"
        media_dir.mkdir(parents=True, exist_ok=True)

        for filename in sync_sample_media():
            self.stdout.write(f"Refreshed bundled seed image from sample/: {filename}")

        for doctor_name, filename in self.IMAGE_MAP.items():
            source = seed_dir / filename
            target = media_dir / filename

            if not source.exists():
                self.stderr.write(self.style.ERROR(f"Missing seed image: {source}"))
                continue

            shutil.copy2(source, target)
            # copy2 preserves the source mtime and the API advertises images as
            # ``?v=<mtime>``, so stamp the publish time: without it a replaced
            # photo keeps its old URL and browsers serve the cached image.
            os.utime(target, None)

            doctor = Doctor.objects.filter(name=doctor_name).first()
            if not doctor:
                self.stdout.write(self.style.WARNING(
                    f"Doctor not found; image copied only: {doctor_name}"
                ))
                continue

            doctor.image.name = f"doctors/{filename}"
            doctor.save(update_fields=["image"])
            self.stdout.write(self.style.SUCCESS(
                f"Updated image: {doctor_name} -> doctors/{filename}"
            ))

        self.stdout.write(self.style.SUCCESS(
            "Doctor image replacement completed. Other CMS data was not reset."
        ))
