import decimal
from django.db.models import Q
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from .managers import UserManager
from PIL import Image
from django.urls import reverse
import secrets
from django.dispatch import receiver

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Rather not say', 'Rather not say')
)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    gender = models.CharField(
        max_length=15,
        choices=GENDER,
        null=True
    )
    is_customer = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    objects = UserManager()

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return str(self.username)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


def _upload_path(instance, filename):
    return instance.get_upload_path(filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    referral = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='referral', blank=True)
    profile_pic = models.ImageField(
        upload_to=_upload_path,
        null=True,
        default='defaultdp.png'
    )
    code = models.CharField(
        max_length=10,
        null=True
    )
    has_paid = models.BooleanField(default=False)
    first_gen = models.ManyToManyField(User, related_name='first_gen', blank=True)
    second_gen = models.ManyToManyField(User, related_name='second_gen', blank=True)

    def __str__(self):
        return str(self.user.username)

    def get_upload_path(self, filename):
        return 'profile_pics/users/' + str(self.user.username) + '/' + filename

    def save(self, *args, **kwargs):
        while not self.code:
            code = secrets.token_urlsafe(6)
            object_with_similar_ref = UserProfile.objects.filter(code=code)
            if not object_with_similar_ref:
                self.code = code
        super(UserProfile, self).save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height >= 800 or img.width >= 800:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

    def ref_link(self):
        return reverse('referral', kwargs={'code': self.code})


class LinkCount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sent_count = models.IntegerField()

    def __str__(self):
        return str(self.user)


class Wallet(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, max_digits=14, default=0)
    total_deposited = models.DecimalField(decimal_places=2, max_digits=14, default=0)
    total_earned = models.DecimalField(decimal_places=2, max_digits=14, default=0)
    total_withdrawn = models.DecimalField(decimal_places=2, max_digits=14, default=0)

    def __str__(self):
        return str(self.user)

    def date_valid(self):
        return self.user.date_joined.strftime('%m/%y')

    def date_valid_day(self):
        return self.user.date_joined.strftime('%a').upper()


@receiver(post_save, sender=User)
def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        Wallet.objects.create(user=instance)
        LinkCount.objects.create(user=instance, sent_count=0)


@receiver(post_save, sender=User)
def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        instance.userprofile.save()
        instance.wallet.save()
        instance.linkcount.save()


@receiver(post_save, sender=User)
def save_count(sender, instance, **kwargs):
    try:
        instance.linkcount.save()
    except Exception as err:
        print(err)


class RefPayouts(models.Model):
    GENERATION = (
        ('First', 'First'),
        ('Second', 'Second'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=14, null=True)
    generation = models.CharField(choices=GENERATION, max_length=10)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sender')
    datetime = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "{}_{}".format(self.user.__str__(), self.amount.__str__(), self.sender.__str__())

    @property
    def get_date(self):
        return self.datetime.strftime('%a %b %y')

    @property
    def get_time(self):
        return self.datetime.strftime('%I:%M%p')