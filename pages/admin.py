from django.contrib import admin
from .models import Config


# Register your models here.
class ConfigAdmin(admin.ModelAdmin):
    list_display = (
        'remote_account', 'local_account', 'delay',
        'last_ping', 'status',)
    excludes = ()


admin.site.register(Config, ConfigAdmin)
