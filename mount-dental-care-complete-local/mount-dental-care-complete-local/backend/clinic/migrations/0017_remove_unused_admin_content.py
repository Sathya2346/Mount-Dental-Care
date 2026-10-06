"""Remove admin content that the website never rendered.

Several CMS entries looked editable but drove nothing on the page, so an editor
could change them and see no effect. They are removed here, data included:

* ``Review`` — there is no reviews/testimonials section on the site anymore.
* ``PageContent`` ``extra_text`` / ``button_text`` / ``image`` / ``video`` — the
  page only reads the eyebrow, title and description. The ``seo`` and
  ``reviews`` rows are dropped too (the app never reads them; the document
  title is hardcoded in ``index.html``).
* ``SiteSettings`` ``phone`` / ``alternate_phone`` / ``emergency_phone`` and the
  ``hero_family_image`` / ``why_technology_image`` / ``why_technology_video`` /
  ``why_dental_image`` / ``hero_rating`` / ``hero_rating_text`` /
  ``smiles_restored`` / ``experience`` fields — branch phones now live on
  Branches, the Hero band uses Hero Banners, the Why section uses Clinic tour
  images, and the rating strip/counters were dropped from the page.
* The stale duplicate footer link ``Painless Root Canal Treatment`` (the seed
  keeps ``Comfortable Root Canal Treatment``), left behind by an earlier seed.
"""

from django.db import migrations, models

REMOVED_SITE_FIELDS = [
    "emergency_phone",
    "phone",
    "alternate_phone",
    "hero_family_image",
    "why_technology_image",
    "why_technology_video",
    "why_dental_image",
    "hero_rating",
    "hero_rating_text",
    "smiles_restored",
    "experience",
]

REMOVED_PAGE_FIELDS = ["extra_text", "button_text", "video", "image"]

UNUSED_PAGE_KEYS = ["seo", "reviews"]
DUPLICATE_FOOTER_LINK = "Painless Root Canal Treatment"


def purge_unused_content(apps, schema_editor):
    PageContent = apps.get_model("clinic", "PageContent")
    FooterLink = apps.get_model("clinic", "FooterLink")
    PageContent.objects.filter(key__in=UNUSED_PAGE_KEYS).delete()
    FooterLink.objects.filter(label__iexact=DUPLICATE_FOOTER_LINK).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("clinic", "0016_remove_vamsi_lavu_and_kamalakannan_doctors"),
    ]

    operations = [
        migrations.RunPython(purge_unused_content, migrations.RunPython.noop),
        *[
            migrations.RemoveField(model_name="sitesettings", name=field)
            for field in REMOVED_SITE_FIELDS
        ],
        *[
            migrations.RemoveField(model_name="pagecontent", name=field)
            for field in REMOVED_PAGE_FIELDS
        ],
        migrations.DeleteModel(name="Review"),
        migrations.AlterField(
            model_name="emailtemplate",
            name="body",
            field=models.TextField(
                help_text=(
                    "Placeholders: {{otp}}, {{expiry_minutes}}, {{appointment_id}}, "
                    "{{full_name}}, {{mobile_number}}, {{email}}, {{preferred_date}}, "
                    "{{treatment_type}}, {{message}}, {{booked_at}}."
                )
            ),
        ),
    ]
