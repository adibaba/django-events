# Imports group 'moderators'
# Imports required contenttypes and permissions before

from django.conf import settings
from django.db import migrations
from django.core import serializers


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0001_country_level_unit_fixtures"),
    ]

    def import_fixures(apps, schema_editor):
        for file in ["contenttype.xml", "permission.xml", "group.xml"]:
            f = open("events/fixtures/" + file, "r")
            data = f.read()
            f.close()
            for obj in serializers.deserialize("xml", data):
                obj.save()

    operations = [
        migrations.RunPython(import_fixures),
    ]
