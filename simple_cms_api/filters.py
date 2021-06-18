import django_filters


class ThingFilter(django_filters.FilterSet):

    referrer_url = django_filters.CharFilter(method='filter_referrer_url')

    def filter_referrer_url(self, queryset, name, url):
        return queryset
