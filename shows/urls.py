from django.conf.urls import url
from django.contrib.auth.views import logout, login
from django.urls import reverse_lazy

from . import views
from .forms import LoginForm

urlpatterns = [
    url(r'^$', views.LandingPageView.as_view(), name='landing-page'),
    url(r'^subscriptions/$', views.SubscriptionsView.as_view(), name='subscriptions'),
    url(r'^logout/$', logout,
        {'next_page': reverse_lazy('landing-page')},
        name='logout'),
    url(r'^login/$', login,
        {'template_name': 'shows/login.html',
         'authentication_form': LoginForm,
         'redirect_authenticated_user': True,},
        name='login'),
    url(r'^.well-known/acme-challenge/.*$', views.acme_challenge, name='acme-challenge')
]