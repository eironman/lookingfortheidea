from django.conf.urls import url

from . import views

app_name = 'contact'
urlpatterns = [
    # /contact
    url(r'^$', views.contact, name='contact'),
    # /contact/message
    url(r'^message$', views.message, name='message'),
]
