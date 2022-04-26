from django.db import models
from accounts.models import Wallet
import random
import string
from decimal import Decimal
from accounts.models import User, UserProfile
from accounts.models import RefPayouts
from home.models import Settings

settings = Settings.objects.get(id=1)
charge = settings.charge_in_percentage


def random_string(letter_count, digit_count):
    str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))
    str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))

    sam_list = list(str1)
    random.shuffle(sam_list)
    final_string = ''.join(sam_list)
    return final_string


class Deposits(models.Model):
    StatusPayment = (
        ('Pending', 'Pending'),
        ('Success', 'Success'),
    )
    trans_ID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=14, default=0)
    secrets = models.CharField(max_length=10, null=True, editable=False)
    wallet_address = models.CharField(max_length=100, null=True)
    date_and_time = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(
        choices=StatusPayment,
        default='Pending',
        max_length=10
    )

    def __str__(self):
        return f'{self.trans_ID} {self.user}'

    def save(self, *args, **kwargs) -> None:
        self.secrets = random_string(5, 5)
        user = UserProfile.objects.get(user=self.user)
        if self.status == 'Success' and not user.has_paid and user.is_verified:
            if user.referral:
                referral_top_user = User.objects.get(username=user.referral)
                referral_top_wallet = Wallet.objects.get(user=referral_top_user)
                percent2 = eferral_top_wallet.balance * settings.first_gen_percentage
                referral_top_wallet.balance += percent2
                referral_top_wallet.save()
                RefPayouts.objects.create(user=referral_top_user, amount=self.amount, generation='First',
                                          sender=self.user)
                if referral_top_user.userprofile.referral:
                    referral_top_top_user = User.objects.get(username=referral_top_user.userprofile.referral)
                    referral_top_top_wallet = Wallet.objects.get(user=referral_top_top_user)
                    percent =referral_top_top_wallet.balance * settings.second_gen_percentage
                    referral_top_top_wallet.balance += percent
                    referral_top_top_wallet.save()
                    RefPayouts.objects.create(user=referral_top_top_user, amount=self.amount, generation='Second',
                                              sender=self.user)
                else:
                    pass
                UserProfile.objects.filter(user=self.user).update(has_paid=True)
        else:
            pass
        if self.status == 'Success':
            wallet = Wallet.objects.get(user=self.user)
            wallet.balance += Decimal(self.amount)
            wallet.total_deposited += Decimal(self.amount)
            wallet.save()
        super(Deposits, self).save(*args, **kwargs)

    class Meta:
        db_table = 'deposits'
        verbose_name_plural = 'Deposits'

    @property
    def get_date(self):
        return self.date_and_time.strftime('%a %b %y')

    @property
    def get_time(self):
        return self.date_and_time.strftime('%I:%M%p')


class Withdraws(models.Model):
    StatusPayment = (
        ('Pending', 'Pending'),
        ('Success', 'Success'),
    )
    trans_ID = models.AutoField(
        primary_key=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=14, null=True)
    wallet_address = models.CharField(max_length=100, null=True)
    date_and_time = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(
        choices=StatusPayment,
        default='Pending',
        max_length=10
    )

    def __str__(self):
        return f'{self.trans_ID} {self.user}'

    def save(self, *args, **kwargs) -> None:
        if self.status == 'Success':
            wallet = Wallet.objects.get(user=self.user)
            wallet.balance -= Decimal(self.amount)
            wallet.total_withdrawn += Decimal(self.amount)
            wallet.save()
        super(Withdraws, self).save(*args, **kwargs)

    class Meta:
        db_table = 'withdraws'
        verbose_name_plural = 'Withdrawals'

    @property
    def get_date(self):
        return self.date_and_time.strftime('%a %b %y')

    @property
    def get_time(self):
        return self.date_and_time.strftime('%I:%M%p')


class DailyPayout(models.Model):
    trans_ID = models.AutoField(primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=14, null=True)
    date_and_time = models.DateTimeField(auto_now_add=True, null=True)
    secrets = models.CharField(max_length=10, null=True, editable=False)

    def save(self, *args, **kwargs) -> None:
        self.secrets = random_string(5, 5)
        super(DailyPayout, self).save(*args, **kwargs)

    class Meta:
        db_table = 'daily_payout'
        verbose_name_plural = 'Daily Payout'

    @property
    def get_date(self):
        return self.date_and_time.strftime('%a %b %y')

    @property
    def get_time(self):
        return self.date_and_time.strftime('%I:%M%p')

    def __str__(self):
        return "{}_{}".format(self.wallet.__str__(), self.amount.__str__(), self.get_date.__str__())
