# See https://docs.djangoproject.com/en/4.2/topics/testing/overview/
# See https://docs.djangoproject.com/en/4.2/topics/testing/tools/#assertions
from django.contrib.auth.models import User
from django.test import Client, TestCase
from events.models import Person, Event, Registration
import unittest


class CreatePersonTestCase(TestCase):
    """Tests if Person objects are automatically created when User objects are created."""

    def setUp(self):
        User.objects.create(username="DevolaTeamson")
        User.objects.create(username="DevolaViktualiaTeamson")

    def test(self):
        self.assertEqual(len(User.objects.all()), len(Person.objects.all()))
        self.assertEqual(2, len(Person.objects.all()))


class NoFreeSlotsTestCase(TestCase):
    """Tests if an exception is thrown when maximum slots of an event are exceeded."""

    def setUp(self):
        User.objects.create(username="u1")
        User.objects.create(username="u2")
        Event.objects.create(title="e1", maximum_participants=1)

    @unittest.expectedFailure
    def test(self):
        Registration.objects.create(person=Person.objects.get(pk=1), event=Event.objects.get(title="e1"))
        Registration.objects.create(person=Person.objects.get(pk=1), event=Event.objects.get(title="e2"))


class NoFreeSlotsClientTestCase(TestCase):
    """Tests if an error message is displayed when maximum slots of an event are exceeded."""

    def setUp(self):
        self.user1 = User.objects.create(username="u1", first_name="u1")
        self.user2 = User.objects.create(username="u2", first_name="u2")
        self.event1 = Event.objects.create(title="e1", maximum_participants=1)
        self.client2 = Client()
        self.client.force_login(self.user1)
        self.client2.force_login(self.user2)

    def test(self):
        response1 = self.client.post("/events/1/register", follow=True)
        response2 = self.client2.post("/events/1/register", follow=True)
        self.assertNotContains(response1, "There are no free slots.")
        self.assertContains(response2, "There are no free slots.")
