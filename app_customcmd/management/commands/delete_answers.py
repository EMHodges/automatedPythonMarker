from django.core.management.base import BaseCommand

from results.models import Result, Subtest
from static_lint.models import StaticLint
from submission.models import Submission


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Subtest.objects.all().delete()
        Result.objects.all().delete()
        StaticLint.objects.all().delete()
        Submission.object.all().delete()

