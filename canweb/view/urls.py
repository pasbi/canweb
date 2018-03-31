from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from view import views

urlpatterns = [
    url(r'song/view/(?P<pk>[0-9]+)/$', views.view_song),
    url(r'song/edit/(?P<pk>[0-9]+)/$', views.edit_song),
    url(r'song/list/', views.view_song_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)