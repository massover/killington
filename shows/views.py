from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.forms import Form
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.generic import CreateView, FormView
from .forms import UserForm, UserSubscriptionForm
from .mixins import (AnonymousRequiredMixin, EmailConfirmationRequiredMixin,
                     SendConfirmationEmailMixin)
from . import utils


class LandingPageView(AnonymousRequiredMixin, SendConfirmationEmailMixin,
                      CreateView):
    template_name = 'shows/landing_page.html'
    model = get_user_model()
    form_class = UserForm
    success_url = reverse_lazy('email-confirmation')

    def form_valid(self, form):
        response = super().form_valid(form)
        auth.login(self.request, self.object)
        self.send_confirmation_email()
        return response


class EmailConfirmationView(LoginRequiredMixin, SendConfirmationEmailMixin,
                            FormView):
    template_name = 'shows/email_confirmation.html'
    form_class = Form
    success_url = reverse_lazy('email-confirmation')

    def form_valid(self, form):
        self.request.user.confirmation_code = utils.generate_confirmation_code()
        self.request.user.save()
        self.send_confirmation_email()
        messages.success(self.request, 'Email confirmation sent. Please check your email.')
        return super().form_valid(form)


@login_required
def email_confirmation_code_validation(request, confirmation_code):
    if confirmation_code != request.user.confirmation_code:
        return HttpResponse(status=400)

    request.user.is_confirmed = True
    request.user.save()
    return redirect(reverse('subscriptions'))


class SubscriptionsView(LoginRequiredMixin, EmailConfirmationRequiredMixin,
                        FormView):
    template_name = 'shows/subscriptions.html'
    form_class = UserSubscriptionForm
    model = get_user_model()
    success_url = reverse_lazy('subscriptions')

    def get_initial(self):
        return {
            'subscribed_shows': self.request.user.subscribed_shows.all(),
        }

    def form_valid(self, form):
        if self.request.POST['button'] == 'unsubscribe-from-all':
            self.request.user.subscribed_shows.set([])
        else:
            queryset = form.cleaned_data['subscribed_shows']
            self.request.user.subscribed_shows.set(list(queryset))

        messages.success(self.request, 'Successfully updated subscriptions')
        return super().form_valid(form)


def acme_challenge(request):
    return HttpResponse(settings.ACME_CHALLENGE_CONTENT)