# Generated by Django 4.0.2 on 2022-03-26 02:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reuse", "0002_post_search_token"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="search_token",
            new_name="search_vector",
        ),
    ]
