import requests
import json
import datetime

station_information_url = "https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_information.json"
station_status_url = "https://gbfs.lyft.com/gbfs/2.3/bkn/en/station_status.json"

def get_station_information():
    response = requests.get(station_information_url)

    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()
        
        # Access the station information
        station_data = data['data']['stations']
        
        # Print out some example station data
        for station in station_data[:5]:  # Print the first 5 stations as a sample
            print(f"Station ID: {station['station_id']}")
            print(f"Name: {station['name']}")
            print(f"Latitude: {station['lat']}")
            print(f"Longitude: {station['lon']}")
            print(f"Capacity: {station['capacity']}")
            print("-" * 20)
        print(len(station_data))
    else:
        print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")

def get_station_status():
    response = requests.get(station_status_url)

    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()
        
        # Access the station information
        station_data = data['data']['stations']
        
        # Print out some example station data
        for station in station_data[:5]:  # Print the first 5 stations as a sample
            last_reported = datetime.datetime.fromtimestamp(station['last_reported'])

            print(f"Station ID: {station['station_id']}")
            print(f"Num Docks Available: {station['num_docks_available']}")
            print(f"Num Bikes Available: {station['num_bikes_available']}")
            print(f"Num E-Bikes Available: {station['num_ebikes_available']}")
            print(f"Is Renting: {True if station['is_renting'] == 1 else False}")
            print(f"Is Returning: {True if station['is_returning'] == 1 else False}")
            print(f"Last Reported: {last_reported}")
            print("-" * 20)
        print(len(station_data))
    else:
        print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")

get_station_information()
get_station_status()