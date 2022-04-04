# Generated by Django 4.0.2 on 2022-03-21 06:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recycle", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("title", models.CharField(max_length=250)),
                ("category", models.CharField(max_length=200)),
                ("phone_number", models.CharField(max_length=17, null=True)),
                ("email", models.EmailField(max_length=254, null=True)),
                ("description", models.TextField()),
                ("approved", models.BooleanField(default=False, null=True)),
                (
                    "still_available",
                    models.BooleanField(default=True, null=True),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "zip_code",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="recycle.zipcode",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("url", models.URLField(max_length=2000)),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reuse.post",
                    ),
                ),
            ],
        ),
    ]
