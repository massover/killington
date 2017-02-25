from django.views.generic import TemplateView

class LandingPageView(TemplateView):
    template_name = 'shows/landing_page.html'