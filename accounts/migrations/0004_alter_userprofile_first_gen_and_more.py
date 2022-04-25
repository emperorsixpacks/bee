# Generated by Django 4.0.3 on 2022-04-17 17:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_userprofile_first_gen_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='first_gen',
            field=models.ManyToManyField(related_name='first_gen', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='second_gen',
            field=models.ManyToManyField(related_name='second_gen', to=settings.AUTH_USER_MODEL),
        ),
    ]
