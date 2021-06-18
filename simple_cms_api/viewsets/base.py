from rest_framework import viewsets

from ..models import Thing
from ..serializers import ThingSerializer
from ..pagination import ResultPagination



class BaseThingViewSet(viewsets.ModelViewSet):

    model_class = Thing
    pagination_class = ResultPagination
    queryset = model_class.objects.all()
    serializer_class = ThingSerializer
