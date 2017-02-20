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
    # /blog/subscribe
    url(r'^subscribe$', views.subscribe, name='subscribe'),
    # /blog/unsubscribe
    url(r'^unsubscribe$', views.unsubscribe, name='unsubscribe'),
    # /blog/send_post_subscription
    url(r'^send_post_subscription$', views.send_post_subscription, name='send_post_subscription'),
]
