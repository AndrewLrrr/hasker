from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class QuestionsSetPagination(PageNumberPagination):
    page_size = settings.QUESTIONS_PER_PAGE
    page_size_query_param = 'page_size'
    max_page_size = 100
