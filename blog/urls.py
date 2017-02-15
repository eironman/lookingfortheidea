from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    # /blog
    url(r'^$', views.posts_list, name='posts_list'),
    # /blog/comment/url
    url(r'^comment/(?P<post_url>.+)/$', views.comment, name='comment'),
    # /blog/url
    url(r'^(?P<post_url>.+)/$', views.content, name='post_content'),
]
