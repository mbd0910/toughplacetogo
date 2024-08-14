from django.contrib import admin

# Register your models here.
from .models import Confederation, Country

class ConfederationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    ordering = ['code']

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'confederation')
    ordering = ['name']

admin.site.register(Confederation, ConfederationAdmin)
admin.site.register(Country, CountryAdmin)