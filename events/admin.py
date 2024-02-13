from django.contrib import admin

from .models import Country, Event, Person, Registration, Level, Unit


class PersonAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email")

    def first_name(self, instance) -> str:
        return instance.user.first_name

    def last_name(self, instance) -> str:
        return instance.user.last_name

    def email(self, instance) -> str:
        return instance.user.email


class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date")


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "person", "person_id")

    def person_id(self, instance) -> int:
        return instance.person.id


admin.site.register(Country)
admin.site.register(Event, EventAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Level)
admin.site.register(Unit)
