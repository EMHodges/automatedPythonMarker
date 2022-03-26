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
    string = "<ul>"
    for i in result.get_failing_subtest_params():
        string += f"<li>{i}</li>"
    string += "</ul>"
    return string


@register.filter
def get_roman_numeral(number: int):
    return roman.toRoman(number).lower()


@register.filter
def get_mark(results):
    return sum(results.values_list('mark', flat=True))


@register.filter
def is_composite_question(dictionary):
    return len(dictionary) > 1


@register.filter
def get_total_marks(dictionary):
    total = 0
    for i in list(dictionary.values()):
        total += sum(i.values_list('mark', flat=True))
    return total


@register.filter
def get_total_available_marks(dictionary):
    return sum([sub_question.max_mark for sub_question in list(dictionary.keys())])


@register.filter
def replace_underscores(string):
    print('in filter')
    print(string)
    print(string.replace('_', ' '))
    return string.replace('_', ' ')