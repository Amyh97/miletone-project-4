from django.urls import path
from . import views

urlpatterns = [
    path('', views.bag, name='bag'),
    path('add/<item_id>', views.basket_item, name='basket_item'),
]
