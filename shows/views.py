from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from .forms import UserForm, SubscriptionForm
from .models import User


class LandingPageView(CreateView):
    template_name = 'shows/landing_page.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('subscriptions')


class SubscriptionsView(FormView, LoginRequiredMixin):
    template_name = 'shows/subscriptions.html'
    form_class = SubscriptionForm
