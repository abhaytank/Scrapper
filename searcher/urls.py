
from django.conf.urls import url ,include

from . import views


urlpatterns = [

    url(r'^$', views.searchq ,name='search'),
    url(r'^index/$', views.index ,name='index'),
    url(r'^about/$', views.about ,name='about'),
]
