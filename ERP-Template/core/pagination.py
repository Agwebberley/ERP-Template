from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        start_index = self.page.start_index()
        end_index = self.page.end_index()
        total_count = self.page.paginator.count
        content_range = f'items {start_index}-{end_index}/{total_count}'
        response = Response({
            'count': total_count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
        response['Content-Range'] = content_range
        return response
