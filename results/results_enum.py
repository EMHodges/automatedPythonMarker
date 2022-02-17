from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _


class ResultsEnums(models.TextChoices):
    SUCCESS = 'SU', _('Success')
    FAIL = 'F', _('Fail')
    ERROR = 'E', _('Error')

    @staticmethod
    def get_yo(existing_results_enum, new_results_enum):
        if existing_results_enum == ResultsEnums.ERROR or new_results_enum == ResultsEnums.ERROR:
            return ResultsEnums.ERROR
        if existing_results_enum == ResultsEnums.FAIL or new_results_enum == ResultsEnums.FAIL:
            return ResultsEnums.FAIL
        return ResultsEnums.SUCCESS
