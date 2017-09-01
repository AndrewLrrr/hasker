from django.conf.urls import url

from .views import *

app_name = 'qa'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^ask/$', AskView.as_view(), name='ask'),
    url(r'^popular/?$', PopularView.as_view(), name='popular'),
    url(r'^question/(?P<slug>[^\s]+)/?$', QuestionView.as_view(), name='question'),
    url(r'^like/question/(?P<pk>[\d]+)/?$', question_like_json, name='question_like'),
    url(r'^dislike/question/(?P<pk>[\d]+)/?$', question_dislike_json, name='question_dislike'),
    url(r'^like/answer/(?P<pk>[\d]+)/?$', answer_like_json, name='answer_like'),
    url(r'^dislike/answer/(?P<pk>[\d]+)/?$', answer_dislike_json, name='answer_dislike'),
    url(r'^tag/(?P<slug>[^\s]+)/?$', TagView.as_view(), name='tag'),
    url(r'^search/?', SearchView.as_view(), name='search'),
    url(r'^singup/$', SingUpView.as_view(), name='singup'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^settings/$', SettingsView.as_view(), name='settings'),
]
