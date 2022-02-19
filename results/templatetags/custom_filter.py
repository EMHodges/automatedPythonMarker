from django.template.defaulttags import register

from results.models import Result


@register.filter
def get_item(dictionary, key):
    print('get item')
    print('dict')
    print(dictionary)
    print('key')
    print(key)
    if not dictionary:
        return None
    print('getting')
    print(dictionary.get(key))
    print('done getting')
    return dictionary.get(key)


@register.filter
def get_failing_subtest_params(result: Result):
    print('failing subtest')
    print(result)
    return result.get_failing_subtest_params()
