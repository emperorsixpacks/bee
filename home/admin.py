from django.contrib import admin
from .models import Settings, Contact, WalletAddress, AboutUsPage


class SettingsAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class AboutAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Settings, SettingsAdmin)
admin.site.register(Contact)
admin.site.register(WalletAddress)
admin.site.register(AboutUsPage, AboutAdmin)
