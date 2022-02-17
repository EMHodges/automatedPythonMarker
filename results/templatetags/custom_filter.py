from django.template.defaulttags import register

from results.models import Result


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_failing_subtest_params(result: Result):
    return result.get_failing_subtest_params()


@register.filter
def get_test_result(result: Result):
    return result.get_test_result()
