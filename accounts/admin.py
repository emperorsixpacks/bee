from django.contrib import admin
from .models import UserProfile, User, LinkCount, Wallet, RefPayouts
from dashboard.models import DailyPayout


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_gen_get']
    list_filter = ['is_verified']

    def first_gen_get(self, instance):
        return [i.username for i in instance.first_gen.all()]


class RefInline(admin.TabularInline):
    model = RefPayouts
    fk_name = 'user'

    def has_add_permission(self, request, obj):
        return False


class PayoutInline(admin.TabularInline):
    model = DailyPayout
    fk_name = 'wallet'

    def has_add_permission(self, request, obj):
        return False


class UsersAdmin(admin.ModelAdmin):
    inlines = [RefInline]


class WalletAdmin(admin.ModelAdmin):
    inlines = [PayoutInline]


admin.site.register(User, UsersAdmin)
admin.site.register(LinkCount)
admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(Wallet, WalletAdmin)
