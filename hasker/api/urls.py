from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from .views import *

app_name = 'api'
urlpatterns = [
    url(r'^questions/$', QuestionList.as_view(), name='questions'),
    url(r'^trending/$', TrendingList.as_view(), name='trending'),
    url(r'^search/?$', SearchList.as_view(), name='search'),
    url(r'^questions/(?P<pk>[\d]+)/answers/$', AnswerList.as_view(), name='answers'),
    url(r'^tags/(?P<pk>[\d]+)/questions/$', TagSearchList.as_view(), name='tags_questions'),
    url(r'^questions/(?P<pk>[\d]+)/vote/$', QuestionVote.as_view(), name='question_vote'),
    url(r'^answers/(?P<pk>[\d]+)/vote/$', AnswerVote.as_view(), name='answer_vote'),
    url(r'^api-token-auth/$', obtain_jwt_token, name='api_token_auth'),
]
