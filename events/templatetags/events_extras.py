import html
import markdown as md
from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import urllib.parse

register = template.Library()


@register.simple_tag
@stringfilter
def setting(name):
    return settings.EVENTS[name]


@register.filter()
@stringfilter
def quote_url_parameter(value):
    return urllib.parse.quote(value)


@register.filter()
@stringfilter
def markdown(value):
    return mark_safe(md.markdown(html.escape(value)).replace("<a ", '<a target="_blank" '))


@register.simple_tag
def update_variable(value):
    """Allows to update existing variable in template"""
    return value


@register.filter()
@stringfilter
def email_break(value):
    """Allows to break email addresses at @ character"""
    return mark_safe(value.replace("@", "@<wbr>"))


@register.filter(name="has_group")
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
