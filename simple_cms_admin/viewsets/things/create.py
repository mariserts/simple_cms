from django.contrib import messages
from django.views import View
from django.shortcuts import redirect

from ...clients.things.client import ThingDetailClient
from ...forms import ThingForm
from ...serializers import ThingSerializer
from ...utils import get_thing_url


class ThingCreateView(View):

    form = ThingForm
    default_serializer = ThingSerializer
    template = 'simple_cms_admin/things/create.html'

    @property
    def serializer(self):
        codename = self.request.resolver_match.kwargs.get('codename', None)
        return self.get_serializer_for_codename(codename)

    def get(self, request, tenant_id, codename):

        return render(
            request,
            self.template,
            context={
                'form': self.form(),
                'instance': {
                    'admin_display': {
                        'title': f'Create new "{codename}"',
                        'codename': codename
                    }
                }
            }
        )

    def post(self, request, tenant_id, codename):

        validated_data = self.get_validated_data(request)

        data = ThingDetailClient().create(
            tenant_id,
            codename,
            validated_data
        )

        redirect_url = _get_thing_url(data)

        messages.success(
            request,
            'Thing was created successfuly'
        )

        return redirect(redirect_url)

    def get_validated_data(self, request):
        return getattr(request, request.method)

    def _get_thing_url(data):
        return get_thing_url(data)

    def get_serializer_for_codename(self, codename=None):
        return self.default_serializer
