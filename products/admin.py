from django.contrib import admin
from .models import products, categories, finish, sizes

# Register your models here.
admin.site.register(products)
admin.site.register(categories)
admin.site.register(finish)
admin.site.register(sizes)
