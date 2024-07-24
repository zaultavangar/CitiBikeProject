from django.urls import path
from . import views

urlpattern = [
  path('predictions/trips/month/<int:month>/', views.predictions_dispatcher),
  path('predictions/trips/day/<int:day>/', views.predictions_dispatcher),
  path('predictions/revenue/', views.predictions_dispatcher),
  
  path('correlations/', views.correlations_dispatcher, name='correlations-dispatcher'),

  path('monthly-metrics/', views.monthly_metrics_dispatcher, name='monthly-metrics-dispatcher'),
  path('monthly-metrics/max-vs-min/', views.monthly_metrics_dispatcher, name='monthly-metrics-dispatcher'),
  path('monthly-metrics/revenue-pctgs/', views.monthly_metrics_dispatcher, name='monthly-metrics-dispatcher'),

  path('bike-type-analysis/', views.get_bike_type_analysis, name='bike-type-analysis'),
  path('prices-vs-revenue/', views.prices_vs_revenue_analysis, name='prices-vs-revenue')
]