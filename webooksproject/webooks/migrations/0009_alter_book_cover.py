# Generated by Django 5.1.1 on 2024-10-16 09:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("webooks", "0008_alter_book_cover"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="cover",
            field=models.TextField(
                blank=True, default="https://shorturl.at/HIdup", null=True
            ),
        ),
    ]
