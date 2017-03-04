from django.contrib.admin.helpers import ActionForm
from django.forms import fields
from django import forms
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import User, Show


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



class ThumbnailCheckboxWidget(forms.SelectMultiple):
    def render(self, name, value, attrs=None):
        if value is None:
            value = []
        options = self.render_options(value)
        return mark_safe(options)

    def render_options(self, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in self.choices:
            output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        show = Show.objects.get(id=option_value)

        option_value = force_text(option_value)
        if option_value in selected_choices:
            checked = 'checked'
        else:
            checked = ''

        html = (
             '<div class="col-sm-4">\n'
             '  <div class="thumbnail text-center">\n'
             '    <img src="{img}">\n'
             '    <div class="caption">\n'
             '      <div class="checkbox">\n'
             '         <label>\n'
             '           <input type="checkbox" name="subscribed_shows" value={id} {checked}> {name}\n'
             '         </label>\n'
             '       </div>\n'
             '    </div>\n'
             '  </div>\n'
             '</div>\n'
        ).format(img=show.img, checked=checked, id=option_value, name=show.name)
        return format_html(html)


class UserSubscriptionForm(forms.Form):
    subscribed_shows = forms.ModelMultipleChoiceField(
        queryset=Show.objects.all(),
        widget=ThumbnailCheckboxWidget(),
        label='',
        required=False,
    )