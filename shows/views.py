from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserForm
from .models import User


class LandingPageView(CreateView):
    template_name = 'shows/landing_page.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('subscribe')


def subscribe(request):
    return HttpResponse()