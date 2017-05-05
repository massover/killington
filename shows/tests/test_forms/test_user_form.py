from datetime import datetime

import pytest
from django import forms
from django.contrib.auth import get_user_model

from ...forms import UserForm
from ..utils import fake


def test_clean_full_name():
    form = UserForm()
    form.cleaned_data = {'full_name': fake.first_name_male()}
    with pytest.raises(forms.ValidationError):
        form.clean_full_name()

def test_clean_date_of_birth():
    form = UserForm()
    form.cleaned_data = {'date_of_birth': datetime.now().date()}
    with pytest.raises(forms.ValidationError):
        form.clean_date_of_birth()

def test_it_updates_css_class():
    form = UserForm()
    for field_name in form.fields:
        field = form.fields[field_name]
        assert field.widget.attrs['class'] == 'input-subscribe'


def test_it_updates_date_of_birth_onclick():
    form = UserForm()
    field = form.fields['date_of_birth']
    assert field.widget.attrs['onclick'] == '(this.type=\'date\')'


def test_it_updates_date_of_birth_touchstart():
    form = UserForm()
    field = form.fields['date_of_birth']
    assert field.widget.attrs['ontouchstart'] == '(this.type=\'date\')'


@pytest.mark.django_db
def test_save():
    data = {
        'full_name': '{} {}'.format(fake.first_name(), fake.last_name()),
        'email': fake.email(),
        'zipcode': fake.zipcode(),
        'password': fake.password(),
        'date_of_birth': '1989-01-01',
    }
    form = UserForm(data=data)
    assert form.is_valid(), form.errors

    form.save()
    User = get_user_model()
    assert User.objects.count() == 1

    user = User.objects.first()
    assert user.first_name == data['full_name'].split()[0]
    assert user.last_name == data['full_name'].split()[1]
    assert user.zipcode == data['zipcode']
    assert user.date_of_birth is not None
    assert user.password is not None