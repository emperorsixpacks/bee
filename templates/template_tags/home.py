from django import template
import datetime
from accounts.models import User

register = template.Library()


@register.simple_tag
def year_get_get():
    return datetime.datetime.now().year


