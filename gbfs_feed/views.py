from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, Http404
from .models import Station
import requests
import logging
import datetime

logger = logging.getLogger(__name__)

@csrf_exempt
def station_info_dispatcher(request):
  if request.method == 'POST':
      return update_station_info(request)
  elif request.method == 'GET':
      station_id = request.GET.get('station_id')
      if station_id:
          return get_station_info(request, station_id)
      else:
          return JsonResponse({"error": "Station ID is required for GET requests"}, status=400)
  else:
      return JsonResponse({"error": "Method not allowed"}, status=405)


def update_station_info(request):
  station_information_url = "https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_information.json"
  
  try:
    response = requests.get(station_information_url)
    response.raise_for_status()
  except requests.exceptions.HTTPError as e:
    logger.error(f'Error fetching station information: {e}')
    return JsonResponse({"error:" "Failed to fetch station information"}, status=500)
  
  try:
    data = response.json()
    stations = data['data']['stations']
  except (ValueError, KeyError) as e:
    logger.error(f'Error parsing station information: {e}')
    return JsonResponse({"error": "Failed to parse station information."}, status=500)


  num_stations = len(stations)
  print(f'Num stations: {num_stations}')
  successful = 0

  for station in stations:
    try:
      Station.objects.update_or_create(
        station_id=station['station_id'],
        defaults={
          'name': station['name'],
          'latitude': station['lat'],
          'longitude': station['lon'],
          'capacity': station['capacity']
        }
      )
      successful +=1
    except Exception as e:
      logger.error(f'Error updating/creating station {station['station_id']}: {e}')

  logger.info(f'{successful}/{num_stations} stations updated successfully.')
  return JsonResponse({"message": f"{successful}/{num_stations} updated successfully."})

def get_station_info(request, station_id):
  try:
    station = get_object_or_404(Station, station_id=station_id)
    station_data = {
      'station_id': station.station_id,
      'name': station.name,
      'latitude': station.latitude,
      'longitude': station.longitude,
      'capacity': station.capacity
    }
    return JsonResponse(station_data)
  except Http404:
    logger.error(f'Station with ID {station_id} does not exist.')
    return JsonResponse({"error": f'Station not found with ID ::: {station_id}'}, status=404)
  except Exception as e:
    logger.error(f'Error retrieving station {station_id}: {e}')
    return JsonResponse({"error": 'Failed to retrieve station information'}, status=500)

def get_station_status(request):
  if request.method != 'GET':
    return JsonResponse({"error": "Method not allowed"}, status=405)

  station_status_url = "https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json"
  
  try:
    response = requests.get(station_status_url)
    response.raise_for_status()
  except requests.exceptions.HttpError as e:
    logger.error(f'Error fetching station status: {e}')
    return JsonResponse({"error:" "Failed to fetch station status"}, status=500)
  
  try:
    data = response.json()
    stations = data['data']['stations']
  except (ValueError, KeyError) as e:
    logger.error(f'Error parsing station statuses: {e}')
    return JsonResponse({"error": "Failed to parse station status."}, status=500)
 
  num_stations = len(stations)
  print(f'Num stations: {num_stations}')
  successful = 0

  all_statuses = []
  for station in stations:
    try: 
      last_reported = datetime.datetime.fromtimestamp(station['last_reported'])

      status = {
        "id": station['station_id'],
        "num_docks_available": station['num_docks_available'],
        "num_bikes_available": station['num_bikes_available'],
        "num_ebikes_available": station['num_ebikes_available'],
        "is_renting": True if station['is_renting'] == 1 else False,
        "is_returning": True if station['is_returning'] == 1 else False,
        "last_reported": last_reported
      }
      all_statuses.append(status)
      successful+=1
    except Exception as e:
      logger.error(f'Error fetching status for {station['station_id']}: {e}')

  logger.info(f'{successful}/{num_stations} station statuses successfully.')
  return JsonResponse({
    "message": f"{successful}/{num_stations} statuses retrieved successfully.",
    "data": all_statuses
  })