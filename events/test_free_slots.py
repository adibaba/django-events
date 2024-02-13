from django.contrib.auth.models import User
from django.test import TestCase
from events.models import Event, Registration


class FreeSlotsTestCase(TestCase):
    """
    Tests the computation of free slots of events
    """

    def create_event(
        self,
        title=None,
        presenters=None,
        maximum_participants=1,
        published=False,
        canceled=False,
        leisure=True,
    ):
        """Helper method to create events"""
        e = Event.objects.create(
            maximum_participants=maximum_participants,
            published=published,
            canceled=canceled,
            leisure=leisure,
        )
        if title:
            e.title = title
        if presenters:
            e.presenters.set(presenters)
        e.save()
        return e

    def get_info(self):
        """Returns debbung infos for failed tests"""
        strings = []
        for r in Registration.objects.all():
            strings.append("[" + r.event.title)
            strings.append(r.person.user.username)
            strings.append(str(r.approvement_state) + "]")
        return " ".join(strings)

    def setUp(self):
        """Creates general objects to use in tests"""
        self.u1 = User.objects.create(username="u1", first_name="u1")
        self.u2 = User.objects.create(username="u2", first_name="u2")
        self.u3 = User.objects.create(username="u3", first_name="u3")

    def test_1(self):
        """
        Tests free slots defaults
        """
        # Create events
        e1 = self.create_event(title="e1", presenters=[self.u1.person], leisure=True)
        e2 = self.create_event(title="e2", presenters=[self.u1.person], leisure=False)
        self.assertEqual(1, e1.get_free_slots())
        self.assertEqual(1, e2.get_free_slots())

        # Register to events
        r1 = Registration.objects.create(person=self.u2.person, event=e1)
        r2 = Registration.objects.create(person=self.u3.person, event=e2)
        self.assertEqual(0, e1.get_free_slots(), "free slots of leisture event " + self.get_info())
        self.assertEqual(0, e2.get_free_slots(), "free slots of working event " + self.get_info())

        # Delete registrations
        r1.delete()
        r2.delete()
        self.assertEqual(1, e1.get_free_slots())
        self.assertEqual(1, e2.get_free_slots())

    def test_2_canceled(self):
        """
        Tests free slots with canceled registrations
        """
        # Create events
        e1 = self.create_event(title="e1", presenters=[self.u1.person], leisure=True)
        e2 = self.create_event(title="e2", presenters=[self.u1.person], leisure=False)
        self.assertEqual(1, e1.get_free_slots())
        self.assertEqual(1, e2.get_free_slots())

        # Register to events
        r1 = Registration.objects.create(person=self.u2.person, event=e1, canceled=True)
        r2 = Registration.objects.create(person=self.u3.person, event=e2, canceled=True)
        self.assertEqual(
            1,
            e1.get_free_slots(),
            "free slots of leisture event, canceled registration " + self.get_info(),
        )
        self.assertEqual(
            1,
            e2.get_free_slots(),
            "free slots of working event, canceled registration " + self.get_info(),
        )

        # Delete registrations
        r1.delete()
        r2.delete()
        self.assertEqual(1, e1.get_free_slots())
        self.assertEqual(1, e2.get_free_slots())

    def test_3_approvals(self):
        """
        Tests free slots with different approval states
        """
        # Create events
        e1 = self.create_event(title="e1", presenters=[self.u1.person], leisure=True)
        e2 = self.create_event(title="e2", presenters=[self.u1.person], leisure=False)
        self.assertEqual(1, e1.get_free_slots())
        self.assertEqual(1, e2.get_free_slots())

        # Register to events, unprocessed approval
        r1 = Registration.objects.create(person=self.u2.person, event=e1, approvement_state=None)
        r2 = Registration.objects.create(person=self.u3.person, event=e2, approvement_state=None)
        self.assertEqual(
            0,
            e1.get_free_slots(),
            "free slots of leisture event, unprocessed approval " + self.get_info(),
        )
        self.assertEqual(
            0,
            e2.get_free_slots(),
            "free slots of working event, unprocessed approval " + self.get_info(),
        )

        # Accepted approval
        r1.approvement_state = True
        r2.approvement_state = True
        r1.save()
        r2.save()
        self.assertEqual(
            0,
            e1.get_free_slots(),
            "free slots of leisture event, accepted approval " + self.get_info(),
        )
        self.assertEqual(
            0,
            e2.get_free_slots(),
            "free slots of working event, accepted approval " + self.get_info(),
        )

        # Rejected approval
        r1.approvement_state = False
        r2.approvement_state = False
        r1.save()
        r2.save()
        self.assertEqual(False, r1.approvement_state)
        self.assertEqual(
            0,
            e1.get_free_slots(),
            "free slots of leisture event, rejected approval " + self.get_info(),
        )
        self.assertEqual(
            1,
            e2.get_free_slots(),
            "free slots of working event, rejected approval " + self.get_info(),
        )

        # Delete registrations
        r1.delete()
        r2.delete()
        self.assertEqual(1, e1.get_free_slots())
        self.assertEqual(1, e2.get_free_slots())
