# Creates Country, Level, Unit
# Imports related fixtures

from django.db import migrations, models
from django.core import serializers


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    def import_fixures(apps, schema_editor):
        for file in ["country.xml", "level.xml", "unit.xml"]:
            f = open("events/fixtures/" + file, "r")
            data = f.read()
            f.close()
            for obj in serializers.deserialize("xml", data):
                obj.save()

    operations = [
        migrations.CreateModel(
            name="Country",
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
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Level",
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
                ("title", models.CharField(max_length=100)),
                ("order", models.SmallIntegerField(default=0)),
            ],
            options={
                "ordering": ["pk"],
            },
        ),
        migrations.CreateModel(
            name="Unit",
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
                ("title", models.CharField(max_length=100)),
                ("order", models.SmallIntegerField(default=0)),
            ],
            options={
                "ordering": ["pk"],
            },
        ),
        migrations.RunPython(import_fixures),
    ]
