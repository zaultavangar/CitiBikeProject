from django.urls import path
from . import views

urlpatterns = [
  path('station-info/', views.station_info_dispatcher, name='station_info_dispatcher'),
  path('station-status/', views.get_station_status)
]