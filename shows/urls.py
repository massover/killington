from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.LandingPageView.as_view(), name='landing-page'),
]