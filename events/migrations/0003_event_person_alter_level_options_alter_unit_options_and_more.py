# Generated by Django 4.2.5 on 2023-11-17 11:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import events.models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("events", "0002_group_moderators_fixtures"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
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
                (
                    "description",
                    models.TextField(
                        help_text='To provide links, you can use Markdown. Example: "[Django](https://www.example.org/)".'
                    ),
                ),
                (
                    "date",
                    models.DateField(
                        default=events.models.Event.get_default_date,
                        verbose_name="Date",
                    ),
                ),
                (
                    "time_begin",
                    models.TimeField(default="9:00", verbose_name="Start time"),
                ),
                (
                    "duration",
                    models.PositiveSmallIntegerField(
                        default=60,
                        validators=[
                            django.core.validators.MinValueValidator(10),
                            django.core.validators.MaxValueValidator(600),
                        ],
                        verbose_name="Duration (minutes)",
                    ),
                ),
                (
                    "maximum_participants",
                    models.IntegerField(
                        default=20,
                        validators=[django.core.validators.MinValueValidator(1)],
                    ),
                ),
                (
                    "project_numbers",
                    models.TextField(
                        blank=True,
                        help_text="Project numbers are required for events which are not in free time. They are used to assign the participation in events to projects. Different company entities (e.g. in different countries) may require different projet numbers.",
                    ),
                ),
                (
                    "leisure",
                    models.BooleanField(
                        default=True,
                        help_text="If an event is considered to take place in free time,no approvement from supervisors is required to participate.",
                        verbose_name="Event is in free time",
                    ),
                ),
                (
                    "published",
                    models.BooleanField(
                        default=False,
                        help_text="The event will be publicly listed and the registration is opened.",
                        verbose_name="Publish Event",
                    ),
                ),
                (
                    "canceled",
                    models.BooleanField(
                        default=False,
                        help_text="The event will no longer be listed and the registration is closed.",
                        verbose_name="Cancel Event",
                    ),
                ),
            ],
            options={
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="Person",
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
                    "is_supervisor",
                    models.BooleanField(default=False, verbose_name="Person is a supervisor"),
                ),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.country",
                    ),
                ),
            ],
            options={
                "ordering": ["user__last_name", "user__first_name"],
            },
        ),
        migrations.AlterModelOptions(
            name="level",
            options={"ordering": ["order"]},
        ),
        migrations.AlterModelOptions(
            name="unit",
            options={"ordering": ["order"]},
        ),
        migrations.AlterField(
            model_name="level",
            name="order",
            field=models.SmallIntegerField(default=10000),
        ),
        migrations.AlterField(
            model_name="unit",
            name="order",
            field=models.SmallIntegerField(default=10000),
        ),
        migrations.CreateModel(
            name="Registration",
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
                    "approvement_state",
                    models.BooleanField(default=None, null=True, verbose_name="Approvement state"),
                ),
                (
                    "canceled",
                    models.BooleanField(default=False, verbose_name="Registration is canceled"),
                ),
                (
                    "event",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="events.event"),
                ),
                (
                    "person",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="events.person"),
                ),
            ],
            options={
                "ordering": ["-event__id", "pk"],
            },
        ),
        migrations.AddField(
            model_name="person",
            name="level",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="events.level",
            ),
        ),
        migrations.AddField(
            model_name="person",
            name="representatives",
            field=models.ManyToManyField(blank=True, to="events.person"),
        ),
        migrations.AddField(
            model_name="person",
            name="supervisor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="events.person",
            ),
        ),
        migrations.AddField(
            model_name="person",
            name="unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="events.unit",
            ),
        ),
        migrations.AddField(
            model_name="person",
            name="user",
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="event",
            name="presenters",
            field=models.ManyToManyField(blank=True, to="events.person"),
        ),
    ]
