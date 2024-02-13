from django.conf import settings
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    TemplateView,
)
from django.views.generic.base import RedirectView
from .forms import PersonForm, UserForm, SignupForm, EventCreateForm, EventUpdateForm
from .models import Event, Registration, Person


def is_representative(request):
    """Returns if the current user is logged in and if the user is listed as representative"""
    if request.user.is_authenticated:
        return Person.objects.filter(representatives=request.user.person).exists()
    else:
        return False


class StartView(RedirectView):
    """Redirects to upcoming events list"""

    pattern_name = "event_list_upcoming"


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have singed up successfully.")
            return redirect("settings")
        else:
            return render(request, "events/signup.html", {"form": form})
    else:  # GET
        return render(request, "events/signup.html", {"form": SignupForm()})


class EventsLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = "events/login.html"

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return self.render_to_response(self.get_context_data(form=form))


@login_required
def logout_view(request):
    """Log out and redirect to startpage"""
    logout(request)
    return redirect("start")


class PersonSupportListView(ListView):
    context_object_name = "persons"

    def get_queryset(self):
        return Person.objects.all().filter(user__groups__name="moderators") | Person.objects.all().filter(
            user__is_superuser=True
        )

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context["is_representative"] = is_representative(self.request)  # Required for menu
        context["only_leisure"] = settings.EVENTS["ONLY_LEISURE"]
        return context


class PersonDetailView(LoginRequiredMixin, DetailView):
    model = Person
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context["is_representative"] = is_representative(self.request)  # Required for menu
        return context


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventCreateForm

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context["is_representative"] = is_representative(self.request)  # Required for menu
        context["mode"] = "create"
        return context

    def get_form_kwargs(self):
        # Put additional info in kwargs for form
        kwargs = super(CreateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        kwargs.update({"only_leisure": settings.EVENTS["ONLY_LEISURE"]})
        return kwargs

    def form_valid(self, form):
        # Force current person to be a presenter, even if not selected
        form.cleaned_data["presenters"] = (
            form.cleaned_data["presenters"]
            .order_by()
            .union(Person.objects.filter(id=self.request.user.person.id).order_by())
        )
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventUpdateForm

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        context["is_representative"] = is_representative(self.request)  # Required for menu
        context["title"] = "Edit Event"
        context["mode"] = "edit"

        return context

    def get_form_kwargs(self):
        # Put current user in kwargs for form
        kwargs = super(UpdateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        kwargs.update({"only_leisure": settings.EVENTS["ONLY_LEISURE"]})
        return kwargs

    def form_valid(self, form):
        # Force current person to be a presenter, even if not selected
        form.cleaned_data["presenters"] = (
            form.cleaned_data["presenters"]
            .order_by()
            .union(Person.objects.filter(id=self.request.user.person.id).order_by())
        )

        return super().form_valid(form)


class EventDetailView(DetailView):
    def get_queryset(self):
        query_set = Event.objects.filter(pk=self.kwargs["pk"]).prefetch_related("presenters")
        return query_set

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        context["is_representative"] = is_representative(self.request)  # Required for menu
        context["time_zone"] = settings.TIME_ZONE
        context["presenters"] = self.object.presenters.all()

        if self.request.user.is_authenticated:
            # Case: Current user is presenter of current event
            registrations = Registration.objects.filter(event=self.object)
            if self.request.user.person in self.object.presenters.all():
                context["is_host"] = True
                context["registrations"] = registrations

            # Case: Current user has registrated to event
            user_registrations = registrations.filter(person=self.request.user.person)
            if user_registrations:
                context["user_registration"] = user_registrations.first()

        return context


class EventListView(ListView):
    """Lists events. Modes: host, participant, past, upcoming."""

    model = Event
    fields = "__all__"
    context_object_name = "events"
    paginate_by = 10

    def get_queryset(self):
        if self.kwargs["mode"] == "host":  # Organization view, user is presenter of events
            return Event.objects.filter(presenters=self.request.user.person).order_by("-date", "time_begin")
        elif self.kwargs["mode"] == "participant":  # Registration view
            registrations = Registration.objects.filter(person=self.request.user.person.id)
            return Event.objects.filter(registration__in=registrations).order_by("-date", "time_begin")
        if self.kwargs["mode"] == "past":  # Past events
            return (
                Event.objects.filter(published=True)
                .filter(canceled=False)
                .filter(date__lt=date.today())
                .order_by("-date", "time_begin")
            )
        else:  # Default mode "upcoming": Todays and upcoming events
            return (
                Event.objects.filter(published=True)
                .filter(canceled=False)
                .filter(date__gte=date.today())
                .order_by("date", "time_begin")
            )

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context["is_representative"] = is_representative(self.request)  # Required for menu
        context["mode"] = self.kwargs["mode"]

        # Set title according to mode (set by urls.py)
        if context["mode"] == "host":
            context["title"] = "Organization"
        elif context["mode"] == "participant":
            context["title"] = "Registrations"
        elif context["mode"] == "past":
            context["title"] = "Past Events"
        else:  # Default mode: "upcoming"
            context["title"] = "Upcoming Events"

        return context


class UserEventListView(LoginRequiredMixin, EventListView):
    """EventListView with a required login"""

    pass


@login_required
def registration_create_view(request, event_pk):
    """
    Creates new registration for the the logged in user and the current event.
    If the registration exists, the cancelation is reversed.
    If the given event is in the past, a error message is set to be displayed.
    """
    event = Event.objects.get(pk=event_pk)

    # Presenter can not attend their own events
    if event.presenters.contains(request.user.person):
        messages.error(
            request,
            "You cannot register for your own events.",
        )
        return redirect("event_detail", pk=event.pk)

    if event.is_in_past():  # Forbit registration actions for past events
        messages.error(request, "Events is in the past")
    elif event.get_free_slots() > 0:
        registrations = Registration.objects.filter(person=request.user.person, event=Event.objects.get(pk=event_pk))
        if len(registrations) == 1:  # Registration exists: Reverse cancelatoin
            registration = registrations.first()
            registration.canceled = False
        else:  # Registration does not exist: Create new registration
            registration = Registration(person=request.user.person, event=event)
        registration.save()
    else:
        messages.error(request, "There are no free slots.")

    return HttpResponseRedirect(reverse("event_detail", args=[event_pk]))


@login_required
def registration_cancel_view(request, event_pk):
    """
    Canceles registration for the the logged in user and the current event.
    If the given event is in the past, a error message is set to be displayed.
    """
    registration = Registration.objects.get(person=request.user.person, event=Event.objects.get(pk=event_pk))
    if registration.event.is_in_past():  # Forbit registration actions for past events
        messages.error(request, "Events is in the past")
    else:
        registration.canceled = True  # Cancel registration
        registration.save()
    return HttpResponseRedirect(reverse("event_detail", args=[event_pk]))


class ApprovalView(LoginRequiredMixin, TemplateView):
    template_name = "events/approvals.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_representative"] = is_representative(self.request)  # Required for menu

        # Get supervisors represented by current person
        represents_persons = Person.objects.filter(representatives=self.request.user.person).order_by()
        # Add current person (A=A|B equals A|=B)
        represents_persons |= Person.objects.filter(pk=self.request.user.person.id)
        # Get all persons directly or indirectly supervised
        supervised_persons = Person.objects.filter(supervisor__in=represents_persons).order_by()

        # Get registrations of supervised persons
        registrations = (
            Registration.objects.filter(person__id__in=supervised_persons)
            .filter(canceled=False)  # Registration not canceled
            .filter(event__leisure=False)  # Event in working time
            .filter(event__published=True)  # Event published
            .filter(event__canceled=False)  # Event not canceled
            .filter(event__date__gte=date.today())  # Event from today or upcoming
            .order_by(  # Sort by next event, then first show older registrations
                "event__date",
                "event__time_begin",
                "pk",
            )
            .select_related("event")
            .select_related("person")
            .select_related("person__user")
            .only(  # Reduce number of SQL queries
                "approvement_state",
                "event__title",
                "event__date",
                "person__user__first_name",
                "person__user__last_name",
                "person__user__email",
            )
        )
        context["registrations"] = registrations
        return context


@login_required
def registration_approval_view(request, registration_pk):
    """
    Approves the given registration.
    """
    registration = Registration.objects.get(id=registration_pk)

    # Check free slots
    if registration.event.get_free_slots() == 0:
        messages.error(
            request,
            "You can not withdraw your rejection as there are no free slots left for the event.",
        )
        return redirect("registration_list")

    registration.approvement_state = True
    registration.save()
    return redirect("registration_list")


@login_required
def registration_rejection_view(request, registration_pk):
    """
    Rejects the given registration.
    """
    registration = Registration.objects.get(id=registration_pk)
    registration.approvement_state = False
    registration.save()
    return redirect("registration_list")


@login_required
@transaction.atomic
def settings_view(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        person_form = PersonForm(request.POST, instance=request.user.person)
        if user_form.is_valid() and person_form.is_valid():
            user_form.save()
            person_form.save()
            messages.success(request, "Your settings have been updated.")
            return redirect("settings")
        else:
            return render(
                request,
                "events/profile.html",
                {"is_representative": is_representative(request)},  # Required for menu
            )
    else:
        user_form = UserForm(instance=request.user)
        person_form = PersonForm(instance=request.user.person)
    return render(
        request,
        "events/settings.html",
        {
            "user_form": user_form,
            "person_form": person_form,
            "is_representative": is_representative(request),  # Required for menu
            "only_leisure": settings.EVENTS["ONLY_LEISURE"],
        },
    )
