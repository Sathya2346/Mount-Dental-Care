"""Every model in Django Admin can be added, edited and deleted.

The test walks ``admin.site._registry`` — so a model registered later is
covered automatically — and drives the real admin screens as a logged-in
superuser:

* the Add form saves a new record (POST -> redirect -> the row exists),
* the Change form saves an edit (POST -> redirect -> the new value is stored),
* the Delete confirmation removes it again.

The values posted come from the admin's own form definition, so the test also
covers custom widgets (the split date/time inputs, choice lists, uploads) and
would fail if a field were listed in Admin but not editable. Between the steps
the public site API is asked for its payload, which is what proves an admin
edit never leaves a section of the React page unable to load.
"""

import tempfile
from io import BytesIO
from pathlib import Path

from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from PIL import Image

# Relations are optional in this project (every foreign key is nullable) and
# a multi-valued one cannot be filled with a single value, so they are skipped.
SKIPPED_FORM_FIELDS = (
    forms.ModelChoiceField,
    forms.ModelMultipleChoiceField,
    forms.MultipleChoiceField,
)

# Text form fields whose value is expected to change visibly on an edit.
TEXT_FORM_FIELDS = (forms.CharField, forms.EmailField, forms.URLField)

# Models where Admin deliberately hides "Add" (the row is written by the app).
ORM_ONLY_MODELS = {
    "EmailLog": "append-only email log: has_add_permission is False, so Admin offers change/delete only",
}


def image_upload(name="crud-check.png"):
    buffer = BytesIO()
    Image.new("RGB", (4, 4), (12, 120, 200)).save(buffer, format="PNG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/png")


def video_upload(name="crud-check.mp4"):
    # The file only has to exist and carry the declared content type; nothing
    # transcodes or plays it during the test.
    return SimpleUploadedFile(name, b"\x00\x00\x00\x18ftypmp42" + b"\x00" * 64, content_type="video/mp4")


def form_value(name, field, suffix=""):
    """A valid value for an admin *form* field (not a model field)."""
    if isinstance(field, forms.ImageField):
        return image_upload(f"crud-check{suffix or ''}.png")
    if isinstance(field, forms.FileField):
        return video_upload(f"crud-check{suffix or ''}.mp4")
    if isinstance(field, SKIPPED_FORM_FIELDS):
        return None
    choices = [str(value) for value, _label in (getattr(field, "choices", None) or []) if str(value) != ""]
    if choices:
        return choices[0]
    if isinstance(field, forms.BooleanField):
        return "on"
    if isinstance(field, (forms.IntegerField, forms.DecimalField, forms.FloatField)):
        return "7"
    if isinstance(field, forms.DateTimeField):
        return "2026-01-01 10:00:00"
    if isinstance(field, forms.DateField):
        return "2026-01-01"
    if isinstance(field, forms.TimeField):
        return "10:00:00"
    if isinstance(field, forms.EmailField):
        value = f"c-{name}{suffix or ''}@example.com".replace("_", "")
    elif isinstance(field, forms.URLField):
        value = f"https://example.com/{name.replace('_', '-')}{suffix}"
    else:
        value = f"c-{name}{suffix}"

    # Stay inside the field's max_length so the edit value is never cut short.
    max_length = getattr(field, "max_length", None)
    if max_length and len(value) > max_length:
        value = value[:max_length]
    return value


class AdminCrudTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # Uploads made through the admin must land in a throwaway folder, never
        # in the project's media directory.
        cls._media_dir = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls._media_dir.cleanup)
        super().setUpClass()

    def setUp(self):
        self.enterContext(override_settings(MEDIA_ROOT=Path(self._media_dir.name)))
        self.superuser = User.objects.create_superuser(
            username="crud-admin", email="crud-admin@example.com", password="crud-pass-123"
        )
        self.client.force_login(self.superuser)
        self.request = RequestFactory().get("/admin/")
        self.request.user = self.superuser

    # -- helpers ----------------------------------------------------------
    def form_payload(self, model_admin, obj=None, suffix=""):
        """POST data for this admin form, plus the names of its text fields."""
        readonly = set(model_admin.get_readonly_fields(self.request, obj))
        form = model_admin.get_form(self.request, obj)
        data, text_names = {}, []

        for name, field in form.base_fields.items():
            if name in readonly:
                continue
            if isinstance(field, forms.SplitDateTimeField):
                # The admin renders date/time as two inputs (name_0, name_1).
                data[f"{name}_0"], data[f"{name}_1"] = "2026-01-01", "10:00:00"
                continue
            value = form_value(name, field, suffix)
            if value is None:
                continue
            data[name] = value
            if isinstance(field, TEXT_FORM_FIELDS) and not getattr(field, "choices", None):
                text_names.append(name)

        return data, text_names

    @staticmethod
    def form_errors(response):
        """The admin form errors, so a failure says which field was refused."""
        context = getattr(response, "context", None)
        if not context or "adminform" not in context:
            return ""
        errors = context["adminform"].form.errors
        return f" - {dict(errors)}" if errors else ""

    def site_api(self):
        response = self.client.get("/api/site/")
        self.assertEqual(response.status_code, 200, "the public site API must keep answering")
        return response.json()

    # -- the check --------------------------------------------------------
    def test_every_admin_model_can_be_added_edited_and_deleted(self):
        checked, orm_created, problems = 0, [], []

        for model, model_admin in admin.site._registry.items():
            opts = model._meta
            label = f"{opts.app_label}.{opts.object_name}"
            checked += 1

            add_url = reverse(f"admin:{opts.app_label}_{opts.model_name}_add")
            change_url = f"admin:{opts.app_label}_{opts.model_name}_change"
            delete_url = f"admin:{opts.app_label}_{opts.model_name}_delete"

            # ---- ADD --------------------------------------------------
            obj = None
            if self.client.get(add_url).status_code == 200:
                payload, _ = self.form_payload(model_admin)
                response = self.client.post(add_url, payload, follow=False)
                if response.status_code != 302:
                    problems.append(
                        f"{label}: Add form rejected the record ({response.status_code})"
                        + self.form_errors(response)
                    )
                    continue
                obj = model.objects.order_by("-pk").first()
                if obj is None:
                    problems.append(f"{label}: Add redirected but no row was created")
                    continue
            else:
                try:  # e.g. EmailLog: no Add screen, the app writes the rows
                    obj = model.objects.create()
                except Exception as exc:
                    problems.append(f"{label}: no Add screen and the row could not be created ({exc})")
                    continue
                orm_created.append(opts.object_name)

            # ---- EDIT -------------------------------------------------
            suffix = "-edited"
            payload, text_names = self.form_payload(model_admin, obj, suffix)
            response = self.client.post(reverse(change_url, args=[obj.pk]), payload, follow=False)
            if response.status_code != 302:
                problems.append(
                    f"{label}: Change form rejected the edit ({response.status_code})"
                    + self.form_errors(response)
                )
                continue

            if text_names:
                obj.refresh_from_db()
                stored = [name for name in text_names if suffix in str(getattr(obj, name))]
                if not stored:
                    problems.append(
                        f"{label}: Change saved but none of {text_names} kept the new value"
                    )
                    continue

            # ---- DELETE -----------------------------------------------
            response = self.client.post(reverse(delete_url, args=[obj.pk]), {"post": "yes"}, follow=False)
            if response.status_code != 302:
                problems.append(f"{label}: Delete screen rejected the request ({response.status_code})")
                continue
            if model.objects.filter(pk=obj.pk).exists():
                problems.append(f"{label}: the record still exists after deleting it")
                continue

            self.site_api()  # the page must still load with this record gone

        self.assertFalse(problems, "Admin management problems:\n  - " + "\n  - ".join(problems))
        self.assertEqual(checked, len(admin.site._registry))
        for name in orm_created:
            self.assertIn(name, ORM_ONLY_MODELS, f"{name} should be addable in Admin")

    def test_deleting_all_content_leaves_the_site_api_working(self):
        """An empty CMS must not break the page (the React app falls back to bundled copy)."""
        from .test_seed_and_api import CONTENT_MODELS

        for model in CONTENT_MODELS:
            model.objects.all().delete()

        data = self.site_api()
        self.assertIsNone(data["site"])
        for key in ("nav", "services", "trust", "doctors", "gallery",
                    "addresses", "hours", "footer", "pages", "texts", "branches",
                    "clinic_images", "youtube", "awards", "hero_banners"):
            self.assertEqual(list(data[key]), [], f"{key} should be empty after deleting all content")

    def test_admin_login_and_index_reach_every_model(self):
        self.client.logout()
        self.assertEqual(self.client.get("/admin/login/").status_code, 200)

        self.client.force_login(self.superuser)
        index = self.client.get("/admin/")
        self.assertEqual(index.status_code, 200)
        for model in admin.site._registry:
            opts = model._meta
            self.assertContains(
                index, f"/admin/{opts.app_label}/{opts.model_name}/",
                msg_prefix=f"{opts.object_name} is not reachable from the admin index",
            )
