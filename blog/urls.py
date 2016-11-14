from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    # /blog
    url(r'^$', views.posts_list, name='posts_list'),
    # /blog/1
    url(r'^(?P<post_id>[0-9]+)/$', views.content, name='content'),
    # /blog/1/comment
    url(r'^(?P<post_id>[0-9]+)/comment/$', views.comment, name='comment'),
]
