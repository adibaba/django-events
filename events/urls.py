from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    path("", views.StartView.as_view(), name="start"),
    path("signup", views.signup_view, name="signup"),
    path(settings.LOGIN_URL, views.EventsLoginView.as_view(), name="login"),
    path("logout", views.logout_view, name="logout"),
    path("settings", views.settings_view, name="settings"),
    path("person/<int:pk>", views.PersonDetailView.as_view(), name="person_detail"),
    path(
        "events",
        views.EventListView.as_view(),
        {"mode": "upcoming"},
        name="event_list_upcoming",
    ),
    path(
        "events/past",
        views.EventListView.as_view(),
        {"mode": "past"},
        name="event_list_past",
    ),
    path(
        "events/registrations",
        views.UserEventListView.as_view(),
        {"mode": "participant"},
        name="event_list_participant",
    ),
    path(
        "events/organization",
        views.UserEventListView.as_view(),
        {"mode": "host"},
        name="event_list_host",
    ),
    path("events/<int:pk>", views.EventDetailView.as_view(), name="event_detail"),
    path("events/create", views.EventCreateView.as_view(), name="event_create"),
    path("events/<int:pk>/update", views.EventUpdateView.as_view(), name="event_update"),
    path(
        "events/<int:event_pk>/register",
        views.registration_create_view,
        name="registration_create",
    ),
    path(
        "events/<int:event_pk>/cancel",
        views.registration_cancel_view,
        name="registration_cancel",
    ),
    path(
        "support",
        views.PersonSupportListView.as_view(),
        name="person_list_support",
    ),
    path("approvals", views.ApprovalView.as_view(), name="registration_list"),
    path(
        "approvals/<int:registration_pk>/approve",
        views.registration_approval_view,
        name="registration_approve",
    ),
    path(
        "approvals/<int:registration_pk>/reject",
        views.registration_rejection_view,
        name="registration_reject",
    ),
]
