from accounts.models import Wallet, User
from dashboard.models import DailyPayout
from django.core.management.base import BaseCommand, CommandError
import datetime
import decimal
from home.models import Settings

settings = Settings.objects.get(id=1)
charge = settings.earning_in_percentage


class Command(BaseCommand):
    help = 'This is the basic command for the increment tof the user account daily'

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='app_label', nargs='*')

    def handle(self, *args, **options):
        wallet = Wallet.objects.all()
        for i in wallet:
            if i.balance <= 0.00:
                pass
            else:
                percent = i.balance * charge
                i.balance += percent
                DailyPayout.objects.create(wallet=i, amount=percent)
                i.save()

        self.stdout.write(self.style.SUCCESS('Successfully credited wallet'))

