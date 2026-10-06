"""The default content is published correctly and the API never changes shape.

These tests pin the contract between Django Admin / ``seed_demo`` and the React
app: after a fresh install every section the page renders has content, the
media files exist, and the payload keys are the ones ``src/App.jsx`` reads.
"""

import tempfile
from pathlib import Path

from django.core.management import call_command
from django.test import TestCase, override_settings

from ..models import (
    Award, Branch, ClinicAddress, ClinicHour, ClinicImage, Doctor, EmailTemplate,
    FooterLink, GalleryItem, HeroBanner, NavItem, OfferBanner, PageContent,
    Service, SiteSettings, SiteText, TrustFeature, YoutubeVideo,
)

# Every model that holds website content, i.e. everything the clinic edits.
CONTENT_MODELS = [
    SiteSettings, NavItem, OfferBanner, Service, TrustFeature, Doctor,
    GalleryItem, ClinicAddress, ClinicHour, FooterLink, SiteText,
    Branch, ClinicImage, YoutubeVideo, Award, PageContent, HeroBanner,
    EmailTemplate,
]

# Section -> keys the React app reads from each record (src/App.jsx,
# hydrateFromBackend). A missing key silently blanks part of the page, so it is
# asserted here rather than discovered in the browser.
API_CONTRACT = {
    "site": [
        "clinic_name", "email",
        "logo", "hero_background_image",
        "hero_title", "hero_description",
        "metric_dentists", "metric_equipment",
        "metric_emi", "metric_patients", "topbar_hours", "whatsapp_number",
        "footer_about", "footer_copyright",
    ],
    "hero_banners": ["id", "media_type", "media", "title"],
    "nav": ["label"],
    "services": ["id", "icon", "title", "description", "badge", "full_description", "highlights"],
    "trust": ["icon", "title", "description"],
    "doctors": ["id", "image", "name", "role", "bio", "education", "expertise", "tenure", "memberships", "is_lead"],
    "gallery": ["id", "image", "title", "description", "video"],
    "addresses": ["label", "address"],
    "hours": ["day", "hours", "emergency"],
    "footer": ["group", "label", "url", "sort_order"],
    "pages": ["key", "eyebrow", "title", "description"],
    "texts": ["key", "label", "group", "value"],
    "branches": ["id", "name", "phone_display", "phone_dial", "address",
                 "map_embed_url", "map_directions_url", "is_primary"],
    "clinic_images": ["id", "image", "title", "caption"],
    "youtube": ["id", "title", "url"],
    "awards": ["id", "image", "title", "category", "description", "venue", "event_date"],
}


class SeedContentTests(TestCase):
    """A fresh install publishes the whole website."""

    @classmethod
    def setUpClass(cls):
        cls._media_dir = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls._media_dir.cleanup)
        super().setUpClass()

    def setUp(self):
        self.enterContext(override_settings(MEDIA_ROOT=Path(self._media_dir.name)))

    def seeded_payload(self):
        call_command("seed_demo", verbosity=0)
        response = self.client.get("/api/site/")
        self.assertEqual(response.status_code, 200)
        return response.json()

    def test_every_registered_admin_model_has_seed_data(self):
        self.seeded_payload()
        empty = [model._meta.object_name for model in CONTENT_MODELS if not model.objects.exists()]
        self.assertEqual(empty, [], f"seed_demo left these empty: {', '.join(empty)}")

    def test_api_payload_matches_what_the_react_app_reads(self):
        data = self.seeded_payload()
        for section, keys in API_CONTRACT.items():
            value = data[section]
            self.assertIsNotNone(value, f"{section} is missing from the API payload")
            record = value[0] if isinstance(value, list) and value else value
            self.assertIsInstance(record, dict, f"{section} should contain records")
            for key in keys:
                self.assertIn(key, record, f"{section} is missing the \"{key}\" key the frontend reads")

    def test_sections_the_page_renders_are_not_empty(self):
        data = self.seeded_payload()
        for section in ("nav", "services", "trust", "doctors", "gallery",
                        "addresses", "hours", "footer", "pages", "texts", "branches",
                        "clinic_images", "youtube", "awards", "hero_banners"):
            self.assertTrue(data[section], f"{section} has no content after seeding")
        self.assertTrue(data["site"], "site settings are empty after seeding")
        self.assertTrue(data["offer"], "the offer banner is empty after seeding")

    def test_seeded_media_files_and_urls_exist(self):
        data = self.seeded_payload()

        # Every uploaded asset the page shows must resolve to a real file and a
        # versioned URL (the ?v= token is what busts the browser cache).
        def check(url, label):
            self.assertTrue(url, f"{label} has no image after seeding")
            self.assertIn("/media/", url, f"{label} image URL is not served from /media/")
            self.assertIn("?v=", url, f"{label} image URL is missing its cache-busting token")
            relative = url.split("/media/", 1)[1].split("?", 1)[0]
            self.assertTrue((Path(self._media_dir.name) / relative).exists(), f"{label}: media/{relative} is missing on disk")

        check(data["site"]["logo"], "logo")
        check(data["site"]["hero_background_image"], "hero background")
        for doctor in data["doctors"]:
            check(doctor["image"], f'doctor "{doctor["name"]}"')
        for award in data["awards"]:
            check(award["image"], f'award "{award["title"]}"')

    def test_seeding_twice_creates_no_duplicates(self):
        self.seeded_payload()
        counts = {model.__name__: model.objects.count() for model in CONTENT_MODELS}
        call_command("seed_demo", verbosity=0)
        after = {model.__name__: model.objects.count() for model in CONTENT_MODELS}
        self.assertEqual(counts, after, "re-running the seed must not duplicate records")

    def test_text_blocks_allow_editing_every_section_of_copy(self):
        data = self.seeded_payload()
        keys = {row["key"] for row in data["texts"]}
        # A sample of the copy the clinic is expected to be able to reword.
        for key in ("hero.book_button", "header.book_button", "services.heading.title",
                    "footer.quick_links_title", "appointment.submit", "awards.heading.title",
                    "contact.email_label", "experts.founder_tag"):
            self.assertIn(key, keys, f"text block {key} is not editable in Admin")


class EmptyContentTests(TestCase):
    """Before any content exists (worst case: someone deleted everything)."""

    def test_api_answers_with_empty_sections(self):
        response = self.client.get("/api/site/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsNone(data["site"])
        for key, keys in API_CONTRACT.items():
            self.assertIn(key, data, f"{key} must still be part of the payload")
        for section in ("nav", "services", "trust", "doctors", "gallery",
                        "clinic_images", "youtube", "awards", "hero_banners"):
            self.assertEqual(data[section], [])
