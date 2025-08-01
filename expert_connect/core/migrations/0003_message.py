# Generated by Django 5.2.4 on 2025-08-01 13:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_expertprofile_featured_podcastprofile_featured"),
    ]

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subject", models.CharField(max_length=255)),
                ("body", models.TextField()),
                ("sent_at", models.DateTimeField(auto_now_add=True)),
                ("read_at", models.DateTimeField(blank=True, null=True)),
                (
                    "receiver",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="received_messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
