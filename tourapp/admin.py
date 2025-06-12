from django.contrib import admin
from .models import Destination, DestinationImage

class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 1

class DestinationAdmin(admin.ModelAdmin):
    inlines = [DestinationImageInline]

admin.site.register(Destination, DestinationAdmin)
