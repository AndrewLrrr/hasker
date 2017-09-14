from django.conf.urls import url

from .views import *

app_name = 'api'
urlpatterns = [
    url(r'^questions/$', QuestionList.as_view(), name='questions'),
    url(r'^trending/$', TrendingList.as_view(), name='trending'),
    url(r'^search/?$', SearchList.as_view(), name='search'),
    url(r'^questions/(?P<pk>[\d]+)/answers/$', AnswerList.as_view(), name='answers'),
    url(r'^tags/(?P<pk>[\d]+)/questions/$', TagSearchList.as_view(), name='tags_questions'),
]
