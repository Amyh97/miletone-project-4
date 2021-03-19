from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableInput(ClearableFileInput):
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    # have to keep on same line to prevent template not being found
    template_name = 'products/custom_widget_templates/custom_clearable_input.html'
