import inspect

from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response


class ListMethodMixin:

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class NotImplementedMethodsMixin:

    def list(self, request):
        self.raise_not_implemented()

    def create(self, request):
        self.raise_not_implemented()

    def retrieve(self, request, pk=None):
        self.raise_not_implemented()

    def update(self, request, pk=None):
        self.raise_not_implemented()

    def partial_update(self, request, pk=None):
        self.raise_not_implemented()

    def destroy(self, request, pk=None):
        self.raise_not_implemented()

    #

    def raise_not_implemented(self, method=None):
        if method is None:
            method = inspect.stack()[1][3]
        raise MethodNotAllowed(
            method,
            detail=_(f'Method "{method}" is not allowed'),
        )
