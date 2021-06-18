from django.urls import path

from .viewsets.things.detail import HomepageThingDetailView


class HomepageNoLanguageThing:

    codename = 'homepage_no_language'
    urlpattern = path(
        '',
        HomepageThingDetailView.as_view(),
        name=f'thing-{codename}-detail'
    )


class HomepageThing:

    codename = 'homepage'
    urlpattern = path(
        '<str:language>/',
        HomepageThingDetailView.as_view(),
        name=f'thing-{codename}-detail'
    )
