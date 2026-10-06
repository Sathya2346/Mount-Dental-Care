# Generated for the footer accreditation / copyright update.

from django.db import migrations, models


def clean_footer_text(apps, schema_editor):
    """Drop the US accreditation badges and move the saved copyright year on.

    The React app never renders ADA / HIPAA labels whatever the database holds,
    so this only keeps the values shown in Admin in step with the website.
    """
    SiteSettings = apps.get_model("clinic", "SiteSettings")
    blocked = ("accredited", "hipaa")
    for settings in SiteSettings.objects.all():
        badges = [b.strip() for b in (settings.footer_badges or "").split(",")]
        cleaned = ", ".join(b for b in badges if b and not any(w in b.lower() for w in blocked))
        copyright_text = (settings.footer_copyright or "").replace("2025", "2026")
        if cleaned != (settings.footer_badges or "") or copyright_text != (settings.footer_copyright or ""):
            settings.footer_badges = cleaned
            settings.footer_copyright = copyright_text
            settings.save(update_fields=["footer_badges", "footer_copyright"])


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0013_remove_navitem_anchor_alter_navitem_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='footer_badges',
            field=models.CharField(blank=True, default='', help_text='Optional comma separated pills shown under the footer blurb. American accreditation labels (ADA / HIPAA) are never shown on this site.', max_length=200),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='footer_copyright',
            field=models.CharField(blank=True, default='© 2026 Mount Dental Care & Clinic. All rights reserved.', max_length=200),
        ),
        migrations.RunPython(clean_footer_text, migrations.RunPython.noop),
    ]
