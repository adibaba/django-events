from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from events.models import Event, Registration


class PresenterUnpublishesEventTestCase(TestCase):
    """
    Setting: A presenter created and published an event.
    Now, she wants to withdraw the publication, but users already registered.
    """

    def setUp(self):
        self.u1 = User.objects.create(username="u1", first_name="u1")
        self.u2 = User.objects.create(username="u2", first_name="u2")
        self.e1 = Event.objects.create(title="e1", published=True)
        self.e1.presenters.set([self.u1.person])
        self.e1.save()
        self.e2 = Event.objects.create(title="e2", published=True)
        self.e2.presenters.set([self.u1.person])
        self.e2.save()
        self.r1 = Registration.objects.create(person=self.u2.person, event=self.e1)

    def test(self):
        self.client.force_login(self.u1)
        response = self.client.post(reverse("event_update", kwargs={"pk": self.e1.pk}), follow=True)
        self.assertNotContains(response, "Publish Event")
        self.assertContains(response, "Cancel Event")

        # Also check if an event without registration differs
        response = self.client.post(reverse("event_update", kwargs={"pk": self.e2.pk}), follow=True)
        self.assertContains(response, "Publish Event")
        self.assertNotContains(response, "Cancel Event")


class UserWithdrawsCancelationTestCase(TestCase):
    """
    Setting : A person canceled her registration in the past.
    Now, the person wants to withdraw a previous cancelation of a registration.
    But there are no free slots.
    """

    def setUp(self):
        self.u1 = User.objects.create(username="u1", first_name="u1")
        self.u2 = User.objects.create(username="u2", first_name="u2")
        self.e1 = Event.objects.create(title="e1", published=True, maximum_participants=1)
        self.e2 = Event.objects.create(title="e2", published=True, maximum_participants=1)
        self.r1 = Registration.objects.create(person=self.u1.person, event=self.e1, canceled=True)
        self.r2 = Registration.objects.create(person=self.u2.person, event=self.e1)

    def test(self):
        # Note: The HTML of the website contained (2023-11-08):
        # <a href="/events/1/register" class="btn btn-primary disabled">Attend Event</a>
        self.client.force_login(self.u1)
        response = self.client.get(reverse("event_detail", kwargs={"pk": self.e1.pk}), follow=True)
        self.assertContains(response, 'disabled">Attend Event')

        # Also check if an event with free slots differs
        response = self.client.get(reverse("event_detail", kwargs={"pk": self.e2.pk}), follow=True)
        self.assertNotContains(response, 'disabled">Attend Event')
