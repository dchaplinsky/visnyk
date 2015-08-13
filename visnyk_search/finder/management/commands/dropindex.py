from django.core.management.base import BaseCommand
from finder.elastic_models import visnyk_index


class Command(BaseCommand):
    def handle(self, *args, **options):
        visnyk_index.delete(ignore=404)
        visnyk_index.create()
