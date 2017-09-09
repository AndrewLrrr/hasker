from django.conf.urls import url

from .views import *

app_name = 'api'
urlpatterns = [
    url(r'^questions$', QuestionList.as_view(), name='questions'),
]
