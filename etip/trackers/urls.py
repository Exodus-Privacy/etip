from django.urls import path

from . import views

app_name = 'trackers'
urlpatterns = [
    path('', views.home, name='home'),
    path('trackers/all', views.index, name='index'),
    path('trackers/review', views.review, name='review'),
    path('trackers/approved', views.approved, name='approved'),
    path('trackers/<id>/', views.display_tracker, name='display_tracker'),
    path('trackers/<id>/approve/', views.approve, name='approve'),
    path('trackers/<id>/revoke/', views.revoke, name='revoke'),
    path('trackers/<id>/ship/', views.ship, name='ship'),
    path('trackers/export', views.export_tracker_list, name='export')
]
