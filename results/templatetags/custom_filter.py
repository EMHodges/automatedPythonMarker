from django.template.defaulttags import register

from results.models import Result
from results.results_enum import ResultsEnums


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_failing_subtest_params(result: Result):
    failing = result.subtest_set.all().exclude(test_result=ResultsEnums.SUCCESS)
    return [message for message in failing.values_list('message', flat=True)]
