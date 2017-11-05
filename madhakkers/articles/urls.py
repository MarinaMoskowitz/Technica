from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^real.*', views.real),
    url(r'^$', views.index, name='index'),
]
