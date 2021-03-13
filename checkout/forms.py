from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2', 'town_or_city',
                  'postcode', 'country',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add place holders ro render to form, fields from above
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Contact Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'town_or_city': 'Town or City',
            'postcode': 'Post Code',
            'counrty': 'Counrty',
        }

        # autofocus starts cursor in this box when page loads
        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    # '*' used when field is required in the model
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'order-form'
            # labels are false here as we have placeholders instead
            self.fields[field].label = False
