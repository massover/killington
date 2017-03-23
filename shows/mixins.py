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
        self.request.user.email_user(
            subject='Confirm registration for nycbroadwayclub.com',
            message='Verify your account using this link: {}'.format(link),
            from_email='noreply@nycbroadwayclub.com',
        )