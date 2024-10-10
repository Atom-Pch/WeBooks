# Generated by Django 5.1.1 on 2024-10-10 08:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("webooks", "0002_remove_book_author_remove_book_genre_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
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
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Genre",
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
                ("name", models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name="Shelf",
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
                ("name", models.CharField(default="My Shelf", max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Book",
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
                ("title", models.CharField(max_length=255)),
                (
                    "cover",
                    models.ImageField(blank=True, null=True, upload_to="covers/"),
                ),
                ("publication_date", models.DateField(blank=True, null=True)),
                ("add_date", models.DateField(auto_now_add=True)),
                ("synopsis", models.TextField(blank=True, null=True)),
                ("link", models.URLField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("pending", "Pending"), ("approved", "Approved")],
                        default="pending",
                        max_length=10,
                    ),
                ),
                (
                    "author",
                    models.ManyToManyField(related_name="books", to="webooks.author"),
                ),
                (
                    "genre",
                    models.ManyToManyField(
                        blank=True, related_name="books", to="webooks.genre"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ShelfBook",
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
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("want", "Want to read"),
                            ("reading", "Currently reading"),
                            ("read", "Already read"),
                        ],
                        max_length=25,
                    ),
                ),
                (
                    "book",
                    models.ManyToManyField(related_name="shelfbook", to="webooks.book"),
                ),
                (
                    "shelf",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="webooks.shelf"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
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
                ("bio", models.CharField(default="I love reading!", max_length=255)),
                ("pfp", models.ImageField(blank=True, null=True, upload_to="pfps/")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="shelf",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="webooks.userprofile"
            ),
        ),
        migrations.CreateModel(
            name="Review",
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
                ("rating", models.PositiveSmallIntegerField()),
                ("comment", models.TextField(blank=True, null=True)),
                ("reviewed_at", models.DateTimeField(auto_now_add=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="webooks.book",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="webooks.userprofile",
                    ),
                ),
            ],
        ),
    ]
