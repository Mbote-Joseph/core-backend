# Generated by Django 4.1 on 2023-08-24 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="admin",
            name="role",
            field=models.CharField(default="admin", max_length=50),
        ),
        migrations.AddField(
            model_name="superadmin",
            name="role",
            field=models.CharField(default="superadmin", max_length=50),
        ),
    ]
