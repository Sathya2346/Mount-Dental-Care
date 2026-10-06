from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("clinic", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="HeroBanner",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(blank=True, max_length=150)),
                ("media_type", models.CharField(choices=[("image", "Image"), ("video", "Video")], default="image", max_length=10)),
                ("media", models.FileField(upload_to="hero-banners/")),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["sort_order", "id"], "verbose_name": "Hero Banner", "verbose_name_plural": "Hero Banners"},
        ),
    ]
