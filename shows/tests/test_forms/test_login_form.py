from ...forms import LoginForm

def test_it_updates_css_class():
    form = LoginForm()
    for field_name in form.fields:
        field = form.fields[field_name]
        assert field.widget.attrs['class'] == 'login-form'