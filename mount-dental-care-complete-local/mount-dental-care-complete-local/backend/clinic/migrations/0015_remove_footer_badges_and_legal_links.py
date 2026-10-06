"""Remove the footer accreditation pills and the footer legal links.

Both were content the clinic does not want on the site:

* ``SiteSettings.footer_badges`` held the "ADA Accredited" / "HIPAA Compliant"
  pills. Those are American accreditation labels, so the field is dropped
  entirely rather than merely hidden.
* The ``footer.legal_*`` text rows fed the "Privacy Policy / Terms &
  Conditions / Patient Rights" links in the bottom bar. They are deleted here
  so a saved database cannot bring them back.
"""

from django.db import migrations

LEGAL_KEYS = ["footer.legal_1", "footer.legal_2", "footer.legal_3"]


def delete_legal_text_rows(apps, schema_editor):
    SiteText = apps.get_model("clinic", "SiteText")
    SiteText.objects.filter(key__in=LEGAL_KEYS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("clinic", "0014_footer_accreditation_and_copyright"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sitesettings",
            name="footer_badges",
        ),
        migrations.RunPython(delete_legal_text_rows, migrations.RunPython.noop),
    ]
