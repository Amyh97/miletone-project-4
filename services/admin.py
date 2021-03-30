from django.contrib import admin
from .models import Services, Lengths, Images


class ServiceAdmin(admin.ModelAdmin):
    # dictates what fields are visable in what order in django admin panel
    list_display = (
        'service',
        'image',
        'description',
    )
    # list data by image name a-z
    ordering = ('service',)


class LengthAdmin(admin.ModelAdmin):
    # dictates what fields are visable in what order in django admin panel
    list_display = (
        'length',
        'price',
    )
    # orders price low to high
    ordering = ('price',)


class ImageAdmin(admin.ModelAdmin):
    # dictates what fields are visable in what order in django admin panel
    list_display = (
        'images',
        'price',
    )
    # orders price low to high
    ordering = ('price',)


# Register your models here.
admin.site.register(Services, ServiceAdmin)
admin.site.register(Lengths, LengthAdmin)
admin.site.register(Images, ImageAdmin)
