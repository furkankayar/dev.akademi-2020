from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('auth', views.AuthTokenView.as_view(), name='auth'),
    url(r'^classified/load(?:/(?P<id>\d+))?/$', views.PostView.as_view(), name='load'),
    path('classified/post', views.PostView.as_view(), name='post'),
    url(r'^classified/list(?:/(?P<page>\d+))?(?:/(?P<size>\d+))?/$', views.ListView.as_view(), name='list'),
    url(r'^classified/myList(?:/(?P<page>\d+))?(?:/(?P<size>\d+))?/$', views.MyListView.as_view(), name='myList'),
    path('post/category', views.ManageCategoryView.as_view(), name='post_category'),
    path('post/status', views.PostStatusView.as_view(), name='post_status'),
    url(r'^category(?:/(?P<page>\d+))?(?:/(?P<size>\d+))?/$', views.CategoryView.as_view(), name='category'),
]