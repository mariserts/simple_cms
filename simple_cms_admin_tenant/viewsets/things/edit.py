from django.shortcuts import render

from simple_cms_admin.viewsets.things.edit import BaseThingDetailView

from ...conf import settings


class TenantThingDetailView(BaseThingDetailView):

    template = 'simple_cms_admin_tenant/things/edit.html'

    def get(self, request, tenant_id, pk):

        data = self.serializer.retrieve(
            request=request,
            tenant_id=tenant_id,
            codename=settings.CODENAME,
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
