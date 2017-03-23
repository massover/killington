from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.urls import reverse


class AnonymousRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('subscriptions'))
        return super().dispatch(request, *args, **kwargs)


class EmailConfirmationRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_confirmed:
            return redirect(reverse('email-confirmation'))
        return super().dispatch(request, *args, **kwargs)


class SendConfirmationEmailMixin(object):
    def send_confirmation_email(self):
        kwargs = {'confirmation_code': self.request.user.confirmation_code}
        uri = reverse('email-confirmation-code-validation', kwargs=kwargs)
        link = self.request.build_absolute_uri(uri)

        subject = 'Confirm registration for nycbroadwayclub.com'
        text_content = 'Almost there!'
        from_email = 'noreply@nycbroadwayclub.com'
        to = [self.request.user.email]
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)

        content = ('<p>Hey {}, you are almost ready to start using nycbroadwayclub.<br>'.format(self.request.user.first_name) +
                   '  <a href="{}">Click here<a> to verify your email.'.format(link) +
                   '</p>')
        msg.attach_alternative(content, "text/html")
        msg.send()