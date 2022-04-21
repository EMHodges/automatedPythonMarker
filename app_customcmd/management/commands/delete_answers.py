from django.core.management.base import BaseCommand

from app_customcmd.management.functions.delete_from_databases import delete_answers


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        delete_answers()

