from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math


class InventoryPagination(PageNumberPagination):
    page_size = 24

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': math.ceil(self.page.paginator.count / self.page_size),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })