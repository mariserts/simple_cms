from django.conf import settings as dj_settings
from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from ..base import BaseThingViewSet
from ..mixins import ListMethodMixin, NotImplementedMethodsMixin
from ... import models
from ...pagination import ResultPagination
from ...serializers import ThingSerializer


class PublicThingViewset(
        ListMethodMixin,
        NotImplementedMethodsMixin,
        viewsets.ModelViewSet):

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter
    ]
    filterset_fields = [
        'tenant_id',
        'thing_type__codename'
    ]
    http_method_names = [
        'get'
    ]
    model_class = models.Thing
    queryset = model_class.objects.all()
    serializer_class = ThingSerializer

    def list(self, request):

        queryset = self.get_queryset().filter(
            is_deleted=False
        )

        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        queryset = self.get_queryset().filter(
            is_deleted=False,
            pk=pk
        ).select_related(
            'tenant',
            'thing_type',
        ).prefetch_related(
            'translatables',
        ).first()

        if queryset is None:
            raise exceptions.NotFound()

        serializer = self.get_serializer(queryset, many=False)

        return Response(serializer.data)
