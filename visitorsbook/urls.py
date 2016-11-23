from django.conf.urls import url

from . import views

app_name = 'visitorsbook'
urlpatterns = [
    # /visitorsbook
    url(r'^$', views.visitorsbook, name='visitorsbook'),
    # /visitorsbook/publish
    url(r'^publish$', views.publish, name='publish'),
]
