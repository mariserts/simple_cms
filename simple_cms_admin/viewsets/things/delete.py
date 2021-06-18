from django.contrib import messages
from django.views import View
from django.shortcuts import redirect

from ...clients.things.client import ThingDetailClient
from ...forms import ThingForm
from ...serializers import ThingSerializer
from ...utils import get_admin_home_url


class ThingDeleteView(View):

    default_serializer = ThingSerializer

    @property
    def serializer(self):
        codename = self.request.resolver_match.kwargs.get('codename', None)
        return self.get_serializer_for_codename(codename)

    def delete(self, request, tenant_id, codename, pk):

        data = ThingDetailClient().delete(tenant_id, codename, pk)

        redirect_url = self._get_admin_home_url()

        messages.success(
            request,
            'Thing was deleted successfuly'
        )

        return redirect(redirect_url)

    def _get_admin_home_url(self):
        return get_admin_home_url()

    def get_serializer_for_codename(self, codename=None):
        return self.default_serializer
