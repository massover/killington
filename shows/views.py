from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, FormView
from .forms import UserForm, UserSubscriptionForm
from .mixins import AnonymousRequiredMixin


class LandingPageView(AnonymousRequiredMixin, CreateView):
    template_name = 'shows/landing_page.html'
    model = get_user_model()
    form_class = UserForm
    success_url = reverse_lazy('subscriptions')

    def form_valid(self, form):
        response = super().form_valid(form)
        auth.login(self.request, self.object)
        return response


class SubscriptionsView(LoginRequiredMixin, FormView):
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
