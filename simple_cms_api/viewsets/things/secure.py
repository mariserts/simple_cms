from django.conf import settings as dj_settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions, filters, serializers, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from ..base import BaseThingViewSet
from ..mixins import NotImplementedMethodsMixin
from ... import models
from ...conf import settings
from ...pagination import ResultPagination
# from ...permissions import AuthenticatedUserPermission
from ...serializers import ThingSerializer


# Secure things
# /secure-api/things/

class SecureThingReadViewset(
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
    http_method_names = ['get']
    model_class = models.Thing
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    pagination_class = ResultPagination
    # permission_classes = [AuthenticatedUserPermission]
    queryset = model_class.objects.all()
    serializer_class = ThingSerializer

    def list(self, request):

        if request.user.is_superuser is False:
            queryset = self.model_class.objects.filter(
                tenant__users__id=request.user.id,
                is_deleted=False
            ).select_related(
                'tenant',
            ).prefetch_related(
                'tenant__users'
            )

        else:
            queryset = self.model_class.objects.all(
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

        queryset = self.model_class.objects.filter(
            pk=pk
        ).select_related(
            'tenant',
            'thing_type',
        ).first()

        if queryset is None:
            raise exceptions.NotFound()

        try:
            serializer_class = self._get_serializer_class(
                queryset.thing_type.codename)
        except ValueError as e:
            raise exceptions.NotFound(e)

        serializer = serializer_class(queryset, many=False)

        return Response(serializer.data)

    def _get_serializer_class(self, codename):

        registry = getattr(
            dj_settings,
            settings.GLOBAL_THING_REGISTRY,
            None
        )

        return registry.get_serializer_class(codename)


# Secure tenant types with items
# /secure-api/<str:tenant_id>/<str:codename>/<str:pk>/

class SecureTenantThingTypeThingViewset(BaseThingViewSet):

    # permission_classes = [AuthenticatedUserPermission]

    def list(self, request, tenant_id, codename):

        try:
            serializer_class = self._get_serializer_class(codename)
        except ValueError as e:
            raise exceptions.NotFound(e)

        queryset = self.model_class.objects.filter(
            thing_type__codename=codename,
            tenant_id=tenant_id
        ).select_related(
            'thing_type'
        )

        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True)

        return Response(serializer.data)

    def create(self, request, tenant_id, codename):

        try:
            serializer_class = self._get_serializer_class(codename)
        except ValueError as e:
            raise exceptions.NotFound(e)

        data = getattr(request, request.method)
        thing_type = ThingType.objects.get(codename=codename)

        data['tenant_id'] = tenant_id
        data['thing_type_id'] = str(thing_type.id)

        serializer = serializer_class(
            data=data,
            many=False
        )

        if serializer.is_valid() is True:
            serializer.save()

        return Response(serializer.data, status=201)

    def retrieve(self, request, tenant_id, codename, pk=None):

        try:
            serializer_class = self._get_serializer_class(codename)
        except ValueError as e:
            raise exceptions.NotFound(e)

        queryset = self.model_class.objects.filter(
            thing_type__codename=codename,
            tenant_id=tenant_id,
            pk=pk
        ).select_related(
            'thing_type'
        ).first()

        if queryset is None:
            raise ObjectDoesNotExist()

        serializer = serializer_class(queryset, many=False)

        return Response(serializer.data)

    def update(self, request, tenant_id, codename, pk=None):

        try:
            serializer_class = self._get_serializer_class(codename)
        except ValueError as e:
            raise exceptions.NotFound(e)

        try:
            queryset = self.model_class.objects.get(
                thing_type__codename=codename,
                tenant_id=tenant_id,
                pk=pk
            ).select_related(
                'thing_type'
            )
        except ObjectDoesNotExist as e:
            raise exceptions.NotFound(e)

        serializer = serializer_class(
            queryset,
            data=getattr(request, request.method),
            many=False
        )

        if serializer.is_valid() is False:
            return Response(serializer.errors, status_code=400)

        serializer.save()

        return Response(serializer.data)

    def partial_update(self, request, tenant_id, codename, pk=None):

        try:
            serializer_class = self._get_serializer_class(codename)
        except ValueError as e:
            raise exceptions.NotFound(e)

        try:
            queryset = self.model_class.objects.get(
                thing_type__codename=codename,
                tenant_id=tenant_id,
                pk=pk
            ).select_related(
                'thing_type'
            )
        except ObjectDoesNotExist as e:
            raise exceptions.NotFound(e)

        serializer = serializer_class(
            queryset,
            data=getattr(request, request.method),
            many=False,
            partial=True
        )

        if serializer.is_valid() is False:
            return Response(serializer.errors, status_code=400)

        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, tenant_id, codename, pk=None):

        try:
            queryset = self.model_class.objects.get(
                thing_type__codename=codename,
                tenant_id=tenant_id,
                pk=pk,
                is_deleted=False,
            ).select_related(
                'thing_type'
            )
        except ObjectDoesNotExist as e:
            raise exceptions.NotFound(e)

        queryset['is_deleted'] = True
        queryset.save()

        return Response()

    def _get_serializer_class(self, codename):

        registry = getattr(
            dj_settings,
            settings.GLOBAL_THING_REGISTRY,
            None
        )

        return registry.get_serializer_class(codename)
