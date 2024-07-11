from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Terminal

class TerminalForm(forms.ModelForm):
    class Meta:
        model = Terminal
        fields = ['unit_id', 'terminal_id', 'terminal_name', 'branch_name', 'port', 'ip', 'location']
        widgets = {
            'location': forms.Select(choices=[('Onsite', 'Onsite'), ('Offsite', 'Offsite')]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
