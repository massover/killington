from django.views.generic import TemplateView
import logging

logger = logging.getLogger(__name__)

class LandingPageView(TemplateView):
    template_name = 'shows/landing_page.html'

    def get(self, request, *args, **kwargs):
        response = super(LandingPageView, self).get(request, *args, **kwargs)
        logger.info('hello world!!!')
        return response