from django.urls import path

from . import views

app_name = 'trackers'
urlpatterns = [
    path('', views.index, name='index'),
    path('trackers/<id>/', views.display_tracker, name='display_tracker'),
    path('trackers/export', views.export_tracker_list, name='export')
]
