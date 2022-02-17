from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _


class ResultsEnums(models.TextChoices):
    SUCCESS = 'SU', _('Success')
    FAIL = 'F', _('Fail')
    ERROR = 'E', _('Error')

    @staticmethod
    def get_ordered(results: QuerySet):
        g = [i[0] for i in results]
        if ResultsEnums.ERROR in g:
            return ResultsEnums.ERROR
        if ResultsEnums.FAIL in g:
            return ResultsEnums.FAIL
        return ResultsEnums.SUCCESS
