from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ResultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page': self.page.number,
            'pages': self.page.paginator.num_pages,
            'pagination': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'results': data
        })
