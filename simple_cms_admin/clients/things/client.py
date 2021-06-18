import requests

from django.conf import settings as dj_settings


class ThingDetailClient:

    def get(self, tenant_id=None, codename=None, pk=None, *args, **kwargs):

        url = dj_settings.API_URL
        url += f'/secure-api/{tenant_id}/{codename}/{pk}/'

        req = requests.get(url)

        if req.status_code != 200:
            req.raise_for_status()

        return req.json()


class ThingListClient:

    def get(
            self,
            tenant_ids=[],
            codenames=[],
            page=1,
            page_size=10,
            *args,
            **kwargs):

        q = kwargs.get('q', None)
        is_published = kwargs.get('is_published', None)
        is_unpublished = kwargs.get('is_unpublished', None)
        created_by_me = kwargs.get('created_by_me', None)

        url = dj_settings.API_URL
        url += dj_settings.API_SECURE_THINGS_ENDPOINT
        url += f'?page_size={page_size}'
        url += f'?page={page}'
        url += f'&ordering=-created_at'

        for tenant_id in tenant_ids:
            url += f'&tenant_id={tenant_id}'

        for codename in codenames:
            url += f'&codename={codename}'

        req = requests.get(url)

        if req.status_code != 200:
            req.raise_for_status()

        return req.json()
