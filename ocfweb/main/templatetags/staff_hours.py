from django import template

from ocfweb.templatetags.lab_hours import lab_hours_holiday as holiday_hours

register = template.Library()


@register.filter
def gravatar(staffer, size):
    return staffer.gravatar(size)

@register.filter
def lab_holidays(hours):
    return holiday_hours(hours)

@register.filter
def not_weekend(day):
    return not (day == "Sunday" or  day == "Saturday")

def rotate_list(lst, shift):
    return lst[shift:] + lst[:shift]

@register.filter
def sort_days_of_week(Days):
    for index in range(len(Days)):
        if Days[index].weekday == "Monday":
            return rotate_list(Days, index)

