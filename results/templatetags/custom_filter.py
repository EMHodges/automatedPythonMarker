import roman
from django.template.defaulttags import register

from results.models import Result


@register.filter
def get_item(dictionary, key):
    if not dictionary:
        return None
    return dictionary.get(key)


@register.filter
def get_failing_subtest_params(result: Result):
    return result.get_failing_subtest_params()


@register.filter
def get_roman_numeral(number: int):
    return roman.toRoman(number).lower()


@register.filter
def get_mark(results):
    return sum(results.values_list('mark', flat=True))


@register.filter
def is_composite_question(dictionary):
    return len(dictionary) > 1
