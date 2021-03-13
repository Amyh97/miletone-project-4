import uuid  # used to create order number

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import products


class Order(models.Model):
    # order number created below and connot be changed
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Counrty *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False,
                                default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    original_basket = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')

    """ underscore at beginning is convention for private methods
    that are only used in this class """
    def _generate_order_number(self):
        """ randomly generate order numbers (32 character string) """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """ update grand total each time a order item is added,
        accounting for delivery costs """

        # or 0 added to this item to prevent error if total is = none
        self.total = self.orderitems.aggregate(Sum('orderitem_total'))
        ['orderitem_total__sum'] or 0
        if self.total < settings.FREE_DELIVERY:
            self.delivery_cost = self.total * settings.\
                                 DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """ Override default save method to set order
        number if it hasn't already got one """

        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='orderitems')
    product = models.ForeignKey(products, null=False, blank=False,
                                on_delete=models.CASCADE)
    size_len = models.CharField(max_length=6)
    finish_img = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    # unable to edit as it will be automatically created
    orderitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                          null=False, blank=False,
                                          editable=False)

    def save(self, *args, **kwargs):
        """ Override original save method to set the orderitem total
        and update the orer total. """

        self.orderitem_total = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f' {self.product.name}, {self.size_len}, {self.finish_img}\
                on order {self.order.order_number}'
