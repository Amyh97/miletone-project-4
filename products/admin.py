from django.contrib import admin
from .models import products, categories, finish, sizes


class ProductAdmin(admin.ModelAdmin):
    # dictates what fields are visable in what order in django admin panel
    list_display = (
        'name',
        'category',
        'date',
        'image',
        'description',
    )
    # list data by image name a-z
    ordering = ('name',)


class CategoriesAdmin(admin.ModelAdmin):
    # dictates what fields are visable in what order in django admin panel
    list_display = (
        'friendly_name',
        'name',

    )


class FinishAdmin(admin.ModelAdmin):
    # dictates what fields are visable in what order in django admin panel
    list_display = (
        'finish',
        'price',
    )
    # orders price low to high
    ordering = ('price',)


class SizesAdmin(admin.ModelAdmin):
    # dictates what fields are visable in what order in django admin panel
    list_display = (
        'sizes',
        'price',
    )
    # orders price low to high
    ordering = ('price',)


# Register your models here.
admin.site.register(products, ProductAdmin)
admin.site.register(categories, CategoriesAdmin)
admin.site.register(finish, FinishAdmin)
admin.site.register(sizes, SizesAdmin)
