from django.contrib import admin
from .models import TODO
# Register your models here.

class TodoAdmin(admin.ModelAdmin):
    readonly_fields=('created',)

admin.site.register(TODO,TodoAdmin)