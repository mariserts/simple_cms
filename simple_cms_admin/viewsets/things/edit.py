from django.conf import settings as dj_settings
from django.contrib import messages
from django.views import View
from django.shortcuts import redirect, render

from ...conf import settings
from ...forms import ThingForm
from ...serializers import ThingSerializer
from ...utils import get_thing_url


class BaseThingDetailView(View):

    template = 'simple_cms_admin/things/edit.html'

    @property
    def initial_data(self):

        codename = self.request.resolver_match.kwargs.get('codename', None)
        pk = self.request.resolver_match.kwargs.get('pk', None)
        tenant_id = self.request.resolver_match.kwargs.get('tenant_id', None)

        data = self.serializer.retrieve(
            request=self.request,
            tenant_id=tenant_id,
            codename=codename,
            pk=pk
        )

        return data

    @property
    def form(self):
        codename = self.request.resolver_match.kwargs.get('codename', None)
        return self._get_form_class(codename)

    @property
    def serializer(self):
        codename = self.request.resolver_match.kwargs.get('codename', None)
        return self._get_serializer_class(codename)

    def get(self, request, tenant_id, codename, pk):

        data = self.serializer.retrieve(
            request=request,
            tenant_id=tenant_id,
            codename=codename,
            pk=pk
        )

        return render(
            request,
            self.template,
            context={
                'form': self.form(initial=data),
                'instance': self.serializer(data, many=False).data
            }
        )

    def post(self, request, tenant_id, codename, pk):

        data = self.serializer.retrieve(
            request=request,
            tenant_id=tenant_id,
            codename=codename,
            pk=pk
        )

        submited_data = getattr(request, request.method)

        form = form(submited_data, inital=data)
        if form.is_valid() is False:
            return render(
                request,
                self.template,
                context={
                    'form': form,
                    'instance': self.serializer(data, many=False).data
                }
            )

        data = self.serializer.update(
            request=request,
            tenant_id=tenant_id,
            codename=codename,
            pk=pk,
            data=validated_data
        )

        redirect_url = self._get_thing_url(data)

        messages.success(
            request,
            'Thing was updated successfuly'
        )

        return redirect(redirect_url)

    #

    def _get_form_class(self, codename):

        registry = getattr(
            dj_settings,
            settings.GLOBAL_THING_REGISTRY,
            None
        )

        return registry.get_form_class(codename)

    def _get_serializer_class(self, codename):

        registry = getattr(
            dj_settings,
            settings.GLOBAL_THING_REGISTRY,
            None
        )

        return registry.get_serializer_class(codename)

    def _get_thing_url(data):
        return get_thing_url(data)


class ThingDetailView(BaseThingDetailView):
    pass
