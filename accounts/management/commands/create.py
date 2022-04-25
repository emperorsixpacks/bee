from home.models import AboutUsPage, Settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'This is the basic command for the increment tof the user account daily'

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='app_label', nargs='*')

    def handle(self, *args, **options):
        AboutUsPage.objects.create()
        Settings.objects.create()



