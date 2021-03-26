from django import forms

# reuse code in products as it will be the same
from products.widgets import CustomClearableInput
from .models import Services


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'

    image = forms.ImageField(label='Image', required=True,
                             widget=CustomClearableInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.items():
            field.widget.attrs['class'] = 'admin-form'
