from django import forms
from .models import products, categories


class ProductForm(forms.ModelForm):
    class Meta:
        model = products
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category = categories.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in category]

        self.fields['categories'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'admin-form'
