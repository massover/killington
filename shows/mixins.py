from django.shortcuts import redirect
from django.urls import reverse


class AnonymousRequiredMixin(object):
    """
    CBV mixin which verifies that the current user is authenticated.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('subscriptions'))
        return super().dispatch(request, *args, **kwargs)