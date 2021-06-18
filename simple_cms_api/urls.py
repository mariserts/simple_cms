from django.conf import settings as dj_settings
from django.urls import path, include

from rest_framework import routers

from .registry import get_thing_registry
from .viewsets.thing_types.secure import SecureTenantThingTypeViewset
from .viewsets.things.public import PublicThingViewset
from .viewsets.things.secure import (
    SecureThingReadViewset,
    SecureTenantThingTypeThingViewset
)
from .viewsets.tenants.secure import SecureTenantViewset


registry = get_thing_registry()


secure_router = routers.SimpleRouter()
secure_router.register(
    'tenants',
    SecureTenantViewset,
    basename='secure-tenant'
)
secure_router.register(
    'things',
    SecureThingReadViewset,
    basename='secure-thing'
)
secure_router.register(
    '(?P<tenant_id>[a-zA-Z0-9\-]+)/thing-types',
    SecureTenantThingTypeViewset,
    basename='secure-tenant-thing-type'
)
secure_router.register(
    '(?P<tenant_id>[a-zA-Z0-9\-]+)/(?P<codename>[a-zA-Z0-9\-]+)',
    SecureTenantThingTypeThingViewset,
    basename='secure-tenant-thing'
)


public_router = routers.SimpleRouter()
public_router.register(
    'things',
    PublicThingViewset,
    basename='public-things'
)


urlpatterns = [
    path(
        'secure-api/',
        include(secure_router.urls)
    ),
    path(
        'api/',
        include(registry.router.urls)
    ),
    path(
        'api/',
        include(public_router.urls)
    ),
    path(
        'api-auth/',
        include('rest_framework.urls',
        namespace='rest_framework')
    )
]
