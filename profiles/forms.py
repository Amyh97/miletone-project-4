from django import forms
from .models import UserProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        """
        get fields from user profile model
        ecxept user, checking one per person
        """
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        # add placeholders to form
        super().__init__(*args, **kwargs)
        # not conurty as this is set in model
        placeholders = {
            'default_contact_number': 'Phone number',
            'default_street_address1': 'Address Line 1',
            'default_street_address2': 'Address Line 2',
            'default_town': 'Town or City',
            'default_postcode': 'Post Code',
        }

        # start cursor on first field of form
        self.fields['default_contact_number'].widget.attrs['autofocus'] = True
        # use place holders except counrty
        for field in self.fields:
            if field != 'default_counrty':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # add class for styling
            self.fields[field].widget.attrs['class'] = 'profile-form-input'
            # no lables and use placeholder above
            self.fields[field].label = False
