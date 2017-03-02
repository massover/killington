from django.conf.urls import url
from django.contrib.auth.views import logout, login
from django.urls import reverse_lazy

from . import views

urlpatterns = [
    url(r'^$', views.LandingPageView.as_view(), name='landing-page'),
    url(r'^subscriptions/$', views.SubscriptionsView.as_view(), name='subscriptions'),
    url(r'logout$',
        logout,
        {'next_page': reverse_lazy('landing-page')},
        name='logout'),
]