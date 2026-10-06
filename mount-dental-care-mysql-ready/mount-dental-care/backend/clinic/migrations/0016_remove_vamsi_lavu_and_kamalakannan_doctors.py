"""Remove the Dr. Vamsi Lavu and Dr. Kamalakannan doctor profiles.

The clinic no longer lists these two specialists, so their profiles and photos
were dropped from the seed data. An already-seeded database still holds the
rows, and the seeder only upserts (it never prunes), so delete them here to
make sure a saved database cannot bring them back.
"""

from django.db import migrations

REMOVED_DOCTOR_NAMES = ["VAMSI LAVU", "KAMALAKANNAN"]


def delete_removed_doctors(apps, schema_editor):
    Doctor = apps.get_model("clinic", "Doctor")
    for name in REMOVED_DOCTOR_NAMES:
        Doctor.objects.filter(name__icontains=name).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("clinic", "0015_remove_footer_badges_and_legal_links"),
    ]

    operations = [
        migrations.RunPython(delete_removed_doctors, migrations.RunPython.noop),
    ]
