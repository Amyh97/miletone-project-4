from django.contrib import admin
from .models import Order, OrderItem


class OrderItemAdminInline(admin.TabularInline):
    """ so we can see editable line items on one page """
    model = OrderItem
    readonly_fields = ('orderitem_total',)


class OrderAdmin(admin.ModelAdmin):
    """ firelds that can be accessed through the Django admin pannel """

    inlines = (OrderItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'total', 'grand_total',
                       'original_basket', 'stripe_pid',)

    # order fields in admin pannel
    fields = ('order_number', 'date', 'full_name', 'email',
              'phone_number', 'country', 'postcode', 'town_or_city',
              'street_address1', 'street_address2', 'county', 'delivery_cost',
              'total', 'grand_total', 'original_basket', 'stripe_pid',)

    list_display = ('order_number', 'date', 'full_name', 'total',
                    'delivery_cost', 'grand_total',)

    # puts most rencent order at the top
    ordering = ('-date',)


""" register Order and Order Admin, but not OrderInlineItem a
 it is assessed through the inlines """
admin.site.register(Order, OrderAdmin)
