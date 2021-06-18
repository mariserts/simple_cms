from rest_framework import viewsets
from rest_framework.response import Response

from ..mixins import NotImplementedMethodsMixin
from ... import models
from ...pagination import ResultPagination
from ...permissions import AuthenticatedUserPermission
from ...serializers import TenantSerializer


# Secure tenants
# /secure-api/tenants/

class SecureTenantViewset(
        NotImplementedMethodsMixin,
        viewsets.ModelViewSet):

    http_method_names = ['get']
    model_class = models.Tenant
    pagination_class = ResultPagination
    # permission_classes = [AuthenticatedUserPermission]
    queryset = model_class.objects.all()
    serializer_class = TenantSerializer

    def list(self, request):

        if request.user.is_superuser is False:
            queryset = self.model_class.objects.filter(
                users__id=request.user.id,
                is_active=True
            ).prefetch_related(
                'users'
            )

        else:
            queryset = self.model_class.objects.all(
                is_active=True
            )

        # queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
