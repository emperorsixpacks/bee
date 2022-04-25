from django.db import models


class Settings(models.Model):
    deposit_text = models.TextField(max_length=1800)
    withdrawal_text = models.TextField(max_length=1800)
    withdrawal_charge = models.DecimalField(decimal_places=2, max_digits=14, default=0)
    daily_earning = models.DecimalField(decimal_places=2, max_digits=14, default=0)
    first_gen_referral = models.DecimalField(decimal_places=2, max_digits=14, default=0)
    second_gen_referral = models.DecimalField(decimal_places=2, max_digits=14, default=0)

    @property
    def charge_in_percentage(self):
        return self.withdrawal_charge / 100

    @property
    def earning_in_percentage(self):
        return self.daily_earning / 100\

    @property
    def first_gen_percentage(self):
        return self.first_gen_referral / 100\

    @property
    def second_gen_percentage(self):
        return self.second_gen_referral / 100


class Contact(models.Model):
    email = models.EmailField(null=True)
    message = models.TextField(max_length=2000)
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class WalletAddress(models.Model):
    TYPE = (
        ('USDT(TRC20)', 'USDT(TRC20)'),
        ('USDT(Bep20)', 'USDT(Bep20)')
    )
    type = models.CharField(choices=TYPE, max_length=30, null=True)
    address = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(self.address)

    class Meta:
        verbose_name_plural = 'Wallet Address'


class AboutUsPage(models.Model):
    about_us_section = models.TextField(max_length=2000)
    why_you_can_trust_us_section = models.TextField(max_length=1800)
    our_mission_section = models.TextField(max_length=1800)

    class Meta:
        verbose_name_plural = 'About US Page'

    def __int__(self):
        return int(self.id)
