from django.contrib import admin
from .models import DemoApi
# Register your models here.

@admin.register(DemoApi)
class DemoApiAdmin(admin.ModelAdmin):
    list_display = ('title', 'img')