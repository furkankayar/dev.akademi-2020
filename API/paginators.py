from rest_framework import pagination

class ListViewPagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 50