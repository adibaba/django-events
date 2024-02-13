from datetime import datetime, timedelta
from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand, CommandError
import random
from events.models import Country, Level, Unit, Event, Registration, Person


class Command(BaseCommand):
    # See: https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/

    help = "Populates data: Creates User, Person, Event and Registration objects"

    def __init__(self):
        BaseCommand.__init__(self)
        self.number_of_users = 20
        self.number_of_events = 40
        self.password = "django"

    def add_arguments(self, parser):
        # See: https://docs.python.org/3/library/argparse.html
        parser.add_argument(
            "--users", type=int, help="Number of users/persons to create, default: " + str(self.number_of_users)
        )
        parser.add_argument(
            "--events", type=int, help="Number of events to create, default: " + str(self.number_of_events)
        )
        parser.add_argument(
            "--password",
            help="Password for users, default: " + self.password,
        )

    def prob_bool(self, probability):
        return random.random() < probability

    def int_to_roman(self, input):
        """Convert an integer to a Roman numeral.
        See: https://www.oreilly.com/library/view/python-cookbook/0596001673/ch03s24.html"""
        ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
        nums = ("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I")
        result = []
        for i in range(len(ints)):
            count = int(input / ints[i])
            result.append(nums[i] * count)
            input -= ints[i] * count
        return "".join(result)

    def populate_user(self, number, password):
        """Creates new users. Sets a superuser and moderators (20%)."""
        users = []
        group_moderators = Group.objects.get(name="moderators")
        try:
            max_user_id = User.objects.all().order_by("-id")[0].id
        except IndexError:
            # No users exist
            max_user_id = 0
        for user_id in range(max_user_id + 1, max_user_id + 1 + number):
            username = "dteamson" + str(user_id)
            email = "devola.teamson" + str(user_id) + "@example.org"
            first_name = "Devola " + self.int_to_roman(user_id) + "."
            last_name = "Teamson"
            user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)

            # Add a superuser
            if user_id == max_user_id + 1:
                user.first_name += " A."
                user.is_staff = True
                user.is_superuser = True

            # Add some moderators
            if user_id % 5 == 0:
                user.first_name += " M."
                user.is_staff = True
                user.groups.add(group_moderators)

            user.save()
            users.append(user)
        return users

    def populate_person(self, users):
        """Creates a Person for each User. Sets supervisors (33%) and representatives."""
        persons = []
        supervisors = []
        countries = list(Country.objects.all())
        levels = list(Level.objects.all())
        units = list(Unit.objects.all())
        for user in users:
            # Create person related to user
            person = Person.objects.get(user__id=user.pk)

            # Add random properties
            person.country = random.choice(countries)
            person.level = random.choice(levels)
            person.unit = random.choice(units)

            # Add supervisor for this person
            if len(supervisors) > 0:
                person.supervisor = random.choice(supervisors)

            # Create at least one supervisor
            if len(supervisors) == 0 or user.pk % 3 == 0:
                person.is_supervisor = True
                user.first_name += " S."
                # Set one represenative
                if len(supervisors) > 0:
                    person.representatives.add(random.choice(supervisors))
                supervisors.append(person)

            user.save()
            person.save()
            persons.append(person)
        return persons

    def populate_events(self, number, persons):
        """Creates events. The dates are between the past 6 years and the upcoming 7 years.
        Distribution: Leisure 25%, Published 80%, Canceled 10%."""
        events = []
        for i in range(number):
            # Choose 1 or 2 presenters
            if len(persons) == 1:
                presenters = persons[0]
            else:
                presenters = random.sample(persons, 2)

            title = "Party of"
            description = "Feel free to bring some stuff."
            date = datetime.today() + timedelta(days=random.randint(-365 * 6, 365 * 7))
            maximum_participants = 2
            event = Event.objects.create(
                title=title, description=description, date=date, maximum_participants=maximum_participants
            )

            for p, presenter in enumerate(presenters):
                event.presenters.add(presenter)
                if p != 0:
                    event.title += " and "
                event.title += " " + presenter.user.first_name + " " + presenter.user.last_name

            if i % 4 == 0:
                event.title = "Birthday " + event.title
            else:
                event.leisure = False
                event.project_numbers = random.randint(100_000, 999_999)

            event.published = self.prob_bool(0.8)
            if not event.published:
                event.title = "Possible " + event.title

            event.canceled = self.prob_bool(0.1)
            if event.canceled:
                event.title = "No " + event.title

            event.save()
            events.append(event)
        return events

    def populate_registrations(self, events, persons):
        """Creates a Registration object for each given event.
        Distribution: Approved 50%, Cancelled 10%."""
        registrations = []
        for i, event in enumerate(events):
            person_options = list(persons)
            for presenter in event.presenters.all():
                person_options.remove(presenter)
            try:
                person = random.choice(person_options)
            except IndexError:
                # All persons are presenters
                continue
            registration = Registration.objects.create(event=event, person=person)
            if i % 3 == 0:
                registration.approvement_state = True
            elif i % 3 == 1:
                registration.approvement_state = False
            else:
                pass  # None/null -> Approval not set yet
            registration.canceled = self.prob_bool(0.1)
            registration.save()
            registrations.append(registration)
        return registrations

    def handle(self, *args, **options):
        if options["users"] is not None:
            self.number_of_users = options["users"]
        if options["events"] is not None:
            if self.number_of_users < 1:
                raise CommandError("At least one user is required to create events")
            self.number_of_events = options["events"]
        if options["password"]:
            self.password = options["password"]

        self.stdout.write(
            self.style.MIGRATE_HEADING(
                "Populating " + str(self.number_of_users) + " users and " + str(self.number_of_events) + " events:"
            )
        )

        self.stdout.write("  Creating User objects... ", ending="")
        self.stdout.flush()
        users = self.populate_user(self.number_of_users, self.password)
        self.stdout.write(self.style.SUCCESS("OK"))

        self.stdout.write("  Creating Person objects... ", ending="")
        self.stdout.flush()
        persons = self.populate_person(users)
        self.stdout.write(self.style.SUCCESS("OK"))

        self.stdout.write("  Creating Event objects... ", ending="")
        self.stdout.flush()
        events = self.populate_events(self.number_of_events, persons)
        self.stdout.write(self.style.SUCCESS("OK"))

        self.stdout.write("  Creating Registration objects... ", ending="")
        self.stdout.flush()
        self.populate_registrations(events, persons)
        self.stdout.write(self.style.SUCCESS("OK"))

        self.stdout.write("Populated data. Superuser: ", ending="")
        self.stdout.write(self.style.NOTICE(users[0].username), ending="")
        self.stdout.write(" with password ", ending="")
        self.stdout.write(self.style.NOTICE(self.password))
