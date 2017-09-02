from django.conf.urls import url

from .views import *

app_name = 'qa'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^ask/$', AskView.as_view(), name='ask'),
    url(r'^question/(?P<slug>[^\s]+)/?$', QuestionView.as_view(), name='question'),
    url(r'^vote/question/(?P<pk>[\d]+)/?$', QuestionVoteView.as_view(), name='question_vote'),
    url(r'^vote/answer/(?P<pk>[\d]+)/?$', AnswerVoteView.as_view(), name='answer_vote'),
    url(r'^mark/answer/(?P<pk>[\d]+)/?$', AnswerMarkView.as_view(), name='answer_mark'),
    url(r'^tag/(?P<slug>[^\s]+)/?$', TagView.as_view(), name='tag'),
    url(r'^search/?', SearchView.as_view(), name='search'),
    url(r'^singup/$', SingUpView.as_view(), name='singup'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^settings/$', SettingsView.as_view(), name='settings'),
    url(r'^profile/(?P<username>[^\s]+)/?$', ProfileView.as_view(), name='profile'),
]
