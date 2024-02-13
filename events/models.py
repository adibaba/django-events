# https://docs.djangoproject.com/en/4.2/ref/models/
from django.db import models

from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import django.db.models.deletion
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.db.models import Q


class Country(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Level(models.Model):
    class Meta:
        ordering = ["order"]

    title = models.CharField(max_length=100)
    order = models.SmallIntegerField(default=10_000)

    def __str__(self):
        return self.title


class Unit(models.Model):
    class Meta:
        ordering = ["order"]

    title = models.CharField(max_length=100)
    order = models.SmallIntegerField(default=10_000)

    def __str__(self):
        return self.title


class Person(models.Model):
    class Meta:
        ordering = ["user__last_name", "user__first_name"]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    country = models.ForeignKey(Country, on_delete=django.db.models.deletion.CASCADE, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=django.db.models.deletion.CASCADE, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=django.db.models.deletion.CASCADE, null=True, blank=True)

    supervisor = models.ForeignKey("self", on_delete=django.db.models.deletion.CASCADE, null=True, blank=True)
    representatives = models.ManyToManyField("self", blank=True)
    is_supervisor = models.BooleanField(default=False, verbose_name="Person is a supervisor")

    def __str__(self):
        """Returns full name of related user"""
        return f"{self.user.first_name} {self.user.last_name}"

    def get_absolute_url(self):
        return reverse("person_detail", kwargs={"pk": self.pk})


@receiver(post_save, sender=User)
def create_user_person(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_person(sender, instance, **kwargs):
    instance.person.save()


class Event(models.Model):
    def get_default_date():
        """Method prevents the creation of a new migrations file every time makemigrations is executed."""
        return datetime.today() + timedelta(days=7)

    class Meta:
        ordering = ["-id"]

    title = models.CharField(max_length=100)
    description = models.TextField(
        help_text='To provide links, you can use Markdown. Example: "[Django](https://www.example.org/)".'
    )

    date = models.DateField(default=get_default_date, verbose_name="Date")
    time_begin = models.TimeField(verbose_name="Start time", default="9:00")
    duration = models.PositiveSmallIntegerField(
        default=60,
        verbose_name="Duration (minutes)",
        validators=[MinValueValidator(10), MaxValueValidator(60 * 10)],
    )
    maximum_participants = models.IntegerField(default=20, validators=[MinValueValidator(1)])
    presenters = models.ManyToManyField(Person, blank=True)
    project_numbers = models.TextField(
        blank=True,
        help_text="Project numbers are required for events which are not in free time. "
        + "They are used to assign the participation in events to projects. "
        + "Different company entities (e.g. in different countries) may require different projet numbers.",
    )
    leisure = models.BooleanField(
        default=True,
        verbose_name="Event is in free time",
        help_text="If an event is considered to take place in free time,"
        + "no approvement from supervisors is required to participate.",
    )
    published = models.BooleanField(
        default=False,
        verbose_name="Publish Event",
        help_text="The event will be publicly listed and the registration is opened.",
    )
    canceled = models.BooleanField(
        default=False,
        verbose_name="Cancel Event",
        help_text="The event will no longer be listed and the registration is closed.",
    )

    def __str__(self):
        return f"{self.id} - {self.title}"

    def get_absolute_url(self):
        return reverse("event_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("event_update", kwargs={"pk": self.pk})

    def get_end_time(self):
        return datetime.combine(self.date, self.time_begin) + timedelta(minutes=self.duration)

    def is_in_past(self):
        return datetime.now() > datetime.combine(self.date, self.time_begin)

    def get_free_slots(self):
        """
        Returns the maxumim number of participants,
        excluding the number of registrations which have been canceled or rejected.
        """
        if self.leisure:
            return self.maximum_participants - Registration.objects.filter(event=self).filter(canceled=False).count()
        else:
            return (
                self.maximum_participants
                - Registration.objects.filter(event=self)
                .filter(canceled=False)
                .filter(~Q(approvement_state__exact=False))
                .count()
            )


class Registration(models.Model):
    """
    A registration is created by one "person" for one "event".

    - "approvement_state" value meanings: "null/None" means not set yet, "True" means approved, "False" means refused.
    - "cancelded": If a user canceles a registration, this flag is set. The registration itself is not deleted.
    """

    class Meta:
        ordering = ["-event__id", "pk"]

    person = models.ForeignKey(Person, on_delete=django.db.models.deletion.CASCADE)
    event = models.ForeignKey(
        Event,
        on_delete=django.db.models.deletion.CASCADE,
    )
    approvement_state = models.BooleanField(null=True, default=None, verbose_name="Approvement state")
    canceled = models.BooleanField(default=False, verbose_name="Registration is canceled")

    def __str__(self):
        return f"{self.pk}"
