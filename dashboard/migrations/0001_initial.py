# Generated by Django 4.0.3 on 2022-04-15 11:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Withdraws',
            fields=[
                ('trans_ID', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14, null=True)),
                ('wallet_address', models.CharField(max_length=100, null=True)),
                ('date_and_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Success', 'Success')], default='Pending', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Withdrawals',
                'db_table': 'withdraws',
            },
        ),
        migrations.CreateModel(
            name='Deposits',
            fields=[
                ('trans_ID', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('secrets', models.CharField(editable=False, max_length=10, null=True)),
                ('date_and_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Success', 'Success')], default='Pending', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Deposits',
                'db_table': 'deposits',
            },
        ),
        migrations.CreateModel(
            name='DailyPayout',
            fields=[
                ('trans_ID', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14, null=True)),
                ('date_and_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('secrets', models.CharField(editable=False, max_length=10, null=True)),
                ('wallet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.wallet')),
            ],
            options={
                'verbose_name_plural': 'Daily Payout',
                'db_table': 'daily_payout',
            },
        ),
    ]
