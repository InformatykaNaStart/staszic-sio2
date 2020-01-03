from django.core.management.base import BaseCommand
from staszic.ejudge.server import serve

class Command(BaseCommand):
    def handle(self, *args, **options):
        serve()
