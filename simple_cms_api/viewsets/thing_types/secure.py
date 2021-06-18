from rest_framework import viewsets
from rest_framework.response import Response

from ..base import BaseThingViewSet
from ..mixins import NotImplementedMethodsMixin
from ... import models
from ...pagination import ResultPagination
# from ...permissions import AuthenticatedUserPermission
from ...serializers import ThingTypeSerializer


# Secure tenant types
# /secure-api/<str:tenant_id>/thing-types/

class SecureTenantThingTypeViewset(
        NotImplementedMethodsMixin,
        viewsets.ModelViewSet):

    http_method_names = ['get']
    model_class = models.ThingType
    queryset = model_class.objects.all()
    pagination_class = ResultPagination
    # permission_classes = [AuthenticatedUserPermission]
    serializer_class = ThingTypeSerializer

    def list(self, request, tenant_id):

        queryset = self.model_class.objects.filter(
            is_active=True
        )

        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
