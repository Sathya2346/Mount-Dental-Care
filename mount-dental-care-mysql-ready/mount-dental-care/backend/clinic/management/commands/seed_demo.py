from django.core.management.base import BaseCommand

from clinic.seeding import install_media, seed_content, sync_sample_media


class Command(BaseCommand):
    help = (
        "Install the full Mount Dental Care default content (CMS text, doctors, "
        "gallery, footer, hero carousel) and copy the bundled media into "
        "MEDIA_ROOT. Safe to run repeatedly."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Overwrite existing records and media with the bundled defaults.",
        )

    def handle(self, *args, **options):
        reset = options["reset"]

        refreshed = sync_sample_media()
        if refreshed:
            self.stdout.write(
                "Sample folder: refreshed "
                + ", ".join(refreshed)
                + " in seed_media/doctors/."
            )

        copied, kept = install_media(force=reset)
        self.stdout.write(f"Media: {copied} file(s) installed into MEDIA_ROOT, {kept} kept.")
        if refreshed and not reset:
            self.stdout.write(
                "Note: existing photos in MEDIA_ROOT were kept. Run "
                "`python manage.py update_doctor_images` to publish the refreshed "
                "doctor photos, or re-run with --reset."
            )

        counts, log = seed_content(reset=reset)
        for line in log:
            self.stdout.write(f"  {line}")

        self.stdout.write(self.style.SUCCESS(
            f"Seed complete — {counts['created']} created, {counts['updated']} updated, "
            f"{counts['kept']} already up to date."
        ))
        if not reset:
            self.stdout.write(
                "Tip: add --reset to force the bundled defaults over existing records."
            )
