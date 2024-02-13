# https://docs.djangoproject.com/en/4.2/ref/forms/validation/
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, EmailField
from .models import Person, Registration, Event


class LoginForm(AuthenticationForm):
    pass


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
        )

    first_name = CharField(max_length=150, required=True)
    last_name = CharField(max_length=150, required=True)
    email = EmailField(required=True)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ("country", "level", "unit", "supervisor", "representatives")
        help_texts = {
            "representatives": "Your representatives can approve event registrations of persons "
            + "whose supervisor you are. (In case you are on vacation for example.)",
        }

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        if not self.instance.is_supervisor:
            self.fields.pop("representatives")
        self.fields["supervisor"].disabled = True

        # Do not show supervisor when only leisure events are used
        if settings.EVENTS["ONLY_LEISURE"]:
            self.fields.pop("supervisor")


class AbstractEventForm(ModelForm):
    """Abstract event form to inherit from."""

    def __init__(self, *args, **kwargs):
        # Get and remove additional arguments
        user = kwargs.pop("user")
        self.only_leisure = kwargs.pop("only_leisure")

        super().__init__(*args, **kwargs)

        # Remove current user from choices
        self.fields["presenters"].queryset = Person.objects.all().exclude(pk=user.person.pk)
        self.fields["presenters"].label = "Additional presenters"

    def clean_published(self):
        published = self.cleaned_data["published"]
        # If a published event has registrations, it can not be unpublished
        if not published and self.instance.published:
            if Registration.objects.filter(event=self.instance).exists():
                raise ValidationError(
                    "You can not withdraw the publication of your event as persons already registered. "
                    + "(You could cancel your event or edit it.)"
                )
        return published


class EventCreateForm(AbstractEventForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "date",
            "time_begin",
            "duration",
            "maximum_participants",
            "presenters",
            "project_numbers",
            "leisure",
            # "published",  # Do not show as provided by button
            # "canceled",  # Do not show as creating an event and cancel it makes no sene
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove working time fields
        if self.only_leisure:
            self.fields.pop("leisure")
            self.fields.pop("project_numbers")


class EventUpdateForm(AbstractEventForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "date",
            "time_begin",
            "duration",
            "maximum_participants",
            "presenters",
            "project_numbers",
            "leisure",
            "published",
            "canceled",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove working time fields
        if self.only_leisure:
            self.fields.pop("leisure")
            self.fields.pop("project_numbers")

        # Set possible actions
        if not self.instance.published and not self.instance.canceled:
            # Event is in draft mode. It can not be canceled (but published).
            self.fields.pop("canceled")
        elif self.instance.published and not self.instance.canceled:
            if not Registration.objects.filter(event=self.instance).exists():
                # Published event has no registrations. It can not be canceled (but unpublished).
                self.fields.pop("canceled")
            else:
                # Published event has registrations, so it can not be unpublished (but canceled).
                self.fields.pop("published")
        elif self.instance.canceled:
            # Canceled event can not be published anymore:
            self.fields.pop("published")
            self.fields.pop("canceled")
