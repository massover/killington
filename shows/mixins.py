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

        html_content = '<p><a href="{}">Click here<a> to confirm your email</p>'.format(link)
        msg.attach_alternative(html_content, "text/html")
        msg.send()