# Generated by Django 4.0.1 on 2022-04-25 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("moderation", "0002_alter_volunteerlogs_reason"),
    ]

    operations = [
        migrations.AddField(
            model_name="volunteerlogs",
            name="approved",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="volunteerlogs",
            name="approved_by",
            field=models.CharField(default="nyc.greencan@gmail.com", max_length=100),
        ),
    ]
