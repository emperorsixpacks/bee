from accounts.models import Wallet
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'This is the basic command for the increment tof the user account daily'

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='app_label', nargs='*')

    def handle(self, *args, **options):
        wallet = Wallet.objects.filter(balance=0.00)
        for i in wallet:
            self.stdout.write(self.style.SUCCESS(f'wallet {i} been inactive. \n Contact the user on  {i.user.email}'))



