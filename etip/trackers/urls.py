from django.conf.urls import url

from . import views

app_name = 'trackers'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^trackers/export$', views.export_tracker_list, name='export')
]
