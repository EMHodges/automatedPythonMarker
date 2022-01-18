from django.db import models
from django.utils.translation import gettext_lazy as _


class ResultsEnums(models.TextChoices):
    SUCCESS = 'SU', _('Success')
    FAIL = 'F', _('Fail')
    ERROR = 'E', _('Error')
