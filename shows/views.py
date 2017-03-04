from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, FormView
from .forms import UserForm, UserSubscriptionForm
from .models import User


class LandingPageView(CreateView):
    template_name = 'shows/landing_page.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('subscriptions')


class SubscriptionsView(LoginRequiredMixin, FormView):
    template_name = 'shows/subscriptions.html'
    form_class = UserSubscriptionForm
    model = User
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
        return super(SubscriptionsView, self).form_valid(form)

