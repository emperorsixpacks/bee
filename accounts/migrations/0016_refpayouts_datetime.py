# Generated by Django 4.0.3 on 2022-04-18 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_refpayouts'),
    ]

    operations = [
        migrations.AddField(
            model_name='refpayouts',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
