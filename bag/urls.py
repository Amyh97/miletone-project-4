from django.urls import path
from . import views

urlpatterns = [
    path('', views.bag, name='bag'),
    path('add/<item_id>', views.basket_item, name='basket_item'),
    path('adjust/<item_id>', views.adjust_basket, name='adjust_basket'),
]
