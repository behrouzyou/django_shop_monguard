from django import template
from datetime import datetime, timezone
import jdatetime


register = template.Library()


@register.filter
def divide_thousand(value):
    return int(value/1000)


@register.filter
def timesince_fa(dt, default="همین الآن"):
    now = datetime.now(timezone.utc)
    diff = now - dt
    periods = (
        (diff.days / 365, "سال"),
        (diff.days / 30, "ماه"),
        (diff.days / 7, "هفته"),
        (diff.days, "روز"),
        (diff.seconds / 3600, "ساعت"),
        (diff.seconds / 60, "دقیقه"),
        (diff.seconds, "ثانیه"),
    )
    for period, unit in periods:
        if period >= 1:
            return f"{period:.0f} {unit} قبل "
    return default


@register.simple_tag
def convert_to_shamsi(date):
    shamsi = jdatetime.datetime.fromgregorian(date=date)
    return shamsi.strftime("%d %B %Y, %H:%M:%S")


@register.inclusion_tag("home/categories_inclusion.html", takes_context=True)
def load_categories(context, categories):
    request = context['request']
    return {'categories':categories}
