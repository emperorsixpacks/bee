from django.contrib import admin
from .models import Withdraws, Deposits


class DepositsAdmin(admin.ModelAdmin):
    list_filter = ('status',)


class WithdrawAdmin(admin.ModelAdmin):
    list_filter = ('status',)


admin.site.register(Deposits, DepositsAdmin)
admin.site.register(Withdraws, WithdrawAdmin)
