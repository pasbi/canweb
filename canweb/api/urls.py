from django.conf.urls import url
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    url(r'song/list$', views.SongList.as_view()),
    url(r'song/(?P<pk>[0-9]+)/$', views.SongDetail.as_view()),
    path(r'search/<str:service>/<str:query>/', views.searchPattern),
    path(r'pattern/<str:service>/<str:query>/', views.getPattern),
    path(r'transpose/<int:d>', views.transpose)
]

urlpatterns = format_suffix_patterns(urlpatterns)