from django.contrib.admin.helpers import ActionForm
from django.forms import fields
from django import forms

from .models import User


class EnterUserInLotteryForm(ActionForm):
    # Validation on ActionForms sucks. It just ends up saying
    # 'No action selected'. Let's do validation in the action view.
    email = fields.CharField(required=False)



class UserForm(forms.ModelForm):
    full_name = fields.CharField(required=True)

    class Meta:
        model = User
        fields = ('full_name', 'email', 'date_of_birth', 'zipcode', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'input-subscribe'

        self.fields['date_of_birth'].widget.attrs['onfocus'] = '(this.type=\'date\')'

    def clean_full_name(self):
        if len(self.cleaned_data.get('full_name').split()) == 2:
            return self.cleaned_data.get('full_name')

        raise forms.ValidationError('First name and last name required')

    def save(self, commit=True):
        self.instance.first_name = self.cleaned_data['full_name'].split()[0]
        self.instance.last_name = self.cleaned_data['full_name'].split()[1]
        return super(UserForm, self).save(commit=commit)

