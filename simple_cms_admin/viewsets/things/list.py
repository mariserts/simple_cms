from django.views import View
from django.shortcuts import render

from ...clients.things.client import ThingListClient
from ...serializers import ThingSerializer


class ThingListView(View):

    page_size = 10
    default_serializer = ThingSerializer
    template = 'simple_cms_admin/things/list.html'

    @property
    def serializer(self):
        return self.get_serializer_for_codename()

    def get(self, request):
        return render(request, self.template, context=self.get_context())

    def get_context(self):

        data = self.get_data()

        return {
            'pagination': {
                'next': '',
                'previous': '',
            },
            'page': self.get_page(data),
            'pages': self.get_page(data),
            'count': self.get_page(data),
            'results': self.get_results(data)
        }

    def get_page(self, data):
        return data.get('page', 0)

    def get_pages(self, data):
        return data.get('pages', 0)

    def get_count(self, data):
        return data.get('count', 0)

    def get_results(self, data):
        return self.serializer(data.get('results', []), many=True).data

    def get_data(self, *args, **kwargs):
        return self.serializer.list(
            request=self.request,
            page=1,
            page_size=self.page_size
        )

    def get_serializer_for_codename(self, codename=None):
        return self.default_serializer
