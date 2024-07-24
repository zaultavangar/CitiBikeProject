from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, Http404
import requests
import logging
import datetime
from trips.utils.tripUtils import (
  get_specific_monthly_data, 
  calculate_bike_type_metrics, 
  max_vs_min_trips_metrics,
  membership_usage_revenue_metrics
)
from trips.exceptions import ColumnNotFoundException

# Create your views here.

## NORMALIZE PRICES TO ACCOUNT FOR INFLATION OR OTHER FACTORS!!
## Convert dataframe to JSON to return 

def predictions_dispatcher(request, *args, **kwargs):
  if 'month' in kwargs:
    return get_monthly_trip_predictions(request, kwargs['month'])
  elif 'day' in kwargs:
    return get_daily_trip_predictions(request, kwargs['day'])
  elif request.path == 'predictions/revenue/':
    return get_revenue_predictions(request)
  else:
    return JsonResponse({"error": "Invalid path"}, status=404)
  
def get_monthly_trip_predictions(request, month_str):
  if not is_valid_month_format(month_str):
    return JsonResponse({
      "error": "Invalid month format. Expected yyyy-mm."
    })

  # TODO
  return JsonResponse({
    "message": f"Monthly trip predictions for month {month_str}",
    "data": None
  })

def get_daily_trip_predictions(request, day_str):
  if not is_valid_day_format(day_str):
    return JsonResponse({
      "error": "Invalid day format. Expected yyyy-mm-dd."
    })
  

  # TODO
  return JsonResponse({
    "message": f"Daily trip predictions for month {day_str}",
    "data": None
  })

def get_revenue_predictions(request):
  return JsonResponse({
    "message": "Revenue Predictions",
    "data": None
  })

# ------------
def correlations_dispatcher(request):
  return False

def get_weather_trips_correlation(request):
  return False

def get_weather_revenue_correlation(request):
  return False

# -----------
def monthly_metrics_dispatcher(request):
  if 'max-vs-min' in request.path:
    return get_max_vs_min_trips(request)
  elif 'revenue-pctgs' in request.path:
    return get_membership_usage_revenue(request)
  else:
    column = request.GET.get('column')
    if not column:
      return JsonResponse({"error": 'Column parameter is required'}, status=400)
    return get_monthly_data_for_column(request, column)

def get_monthly_data_for_column(request, column_abbr):
  try:
    df_json = get_specific_monthly_data(column_abbr)
    return JsonResponse({
      "message": "Successfully retrieved data",
      "data": df_json
    })
  except ColumnNotFoundException as e:
    return JsonResponse({"error": f"{e}"}, status=500)

def get_max_vs_min_trips(request):
  try:
    df_json = max_vs_min_trips_metrics()
    return JsonResponse({
      "message": "Successfully retrieved trip metrics",
      "data": df_json
    })
  except Exception as e:
    return JsonResponse({
      "error": e
    }, status=500)

def get_membership_usage_revenue(request):
  try:
    df_json = membership_usage_revenue_metrics()
    return JsonResponse({
      "message": "Successfully retrieved trip metrics",
      "data": df_json
    })
  except Exception as e:
    return JsonResponse({
      "error": e
    }, status=500)

# -----------
def get_bike_type_analysis(request):
  try:
    bike_type_data_map = calculate_bike_type_metrics()
    return JsonResponse({
      "message": "Bike type data retrieved successfully",
      "data": {
        "bike_type_counts": bike_type_data_map['bike_type_counts'],
        "user_type_bike_type_counts": bike_type_data_map['user_bike_counts'],
        "bike_duration_analysis": bike_type_data_map['bike_duration_analysis']
      }
    })
  except Exception as e:
    return JsonResponse({
      "error": e
    }, status=500)

def prices_vs_revenue_analysis(request):
  return False

## DATE UTILS
def is_valid_month_format(month_str):
  try:
    datetime.datetime.strptime(month_str, '%Y-%m')
    return True
  except ValueError:
    return False
  
def is_valid_day_format(day_str):
  try:
    datetime.datetime.strptime(day_str, '%Y-%m-%d')
    return True
  except ValueError:
    return False