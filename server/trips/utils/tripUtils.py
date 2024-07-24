import pandas as pd
import os
from geopy.distance import geodesic
from trips.exceptions import ColumnNotFoundException


data_base_path = '/Users/zaultavangar/Desktop/Comp Sci/CitiBikeProject/citibike-data'

COLUMN_ABBR_MAP = {
  'amt': 'annual_member_trips',
  'cmt': 'casual_member_trips',
  'stp': 'single_trip_passes',
  '24hp': '24_hr_passes',
  '3dp': '3_day_passes',
  '7dp': '7_day_passes',
  'pam': 'annual_memberships',
  'taam': 'total_annual_active_members',
  'trm': 'membership_revenue',
  'amr': 'annual_membership_revenue',
  'mmr': 'monthly_membership_revenue',
  'crr': 'casual_ridership_revenue',
  'aor': 'all_other_revenue',
  'co': 'carbon_offset (lb)'
}

def get_specific_monthly_data(column_name):
  file_path = 'cleaned_trip_membership_usage_revenue_data.csv'
  full_path = os.path.join(data_base_path, file_path)

  df = pd.read_csv(full_path)

  if column_name in COLUMN_ABBR_MAP:
    standard_column_name = COLUMN_ABBR_MAP[column_name]
  else:
    raise ColumnNotFoundException(f'Data does not exist for :: {column_name}')
  
  df = df[['month_year', standard_column_name]]

  return df.to_json(orient='split')

def calculate_bike_type_metrics(sample_size = 0.15):
  file_paths = [
    '2022-citibike-tripdata/final_2022_trip_data.csv'
    '2023-citibike-tripdata/final_2023_trip_data.csv'
  ]
  all_data = []

  for file_path in file_paths:
    full_path = os.path.join(data_base_path, file_path)
    chunks = pd.read_csv(full_path, chunksize=10000)
    df = pd.concat(chunks, ignore_index=True)

    df = df[['month_year', 'start_lat', 'start_lng','end_lat', 'end_lng',
            'user_type', 'rideable_type', 'trip_duration']]
    
    all_data.append(df)

  combined_df = pd.concat(all_data, ignore_index=True)

  ## Number and percentage of classic and e-bike rides for each month_year
  bike_counts = combined_df.groupby(['month_year', 'rideable_type']).size().unstack(fill_value=0)
  bike_counts = bike_counts / sample_size
  bike_counts['total_rides'] = bike_counts.sum(axis=1)
  bike_counts['classic_percentage'] = (bike_counts['classic_bike'] / bike_counts['total_rides']) * 100
  bike_counts['electric_percentage'] = (bike_counts['electric_bike'] / bike_counts['total_rides']) * 100
  bike_counts.reset_index(inplace=True)
  bike_counts_json = bike_counts.to_json(split='orient')

  # Analyze the distribution of user types and bike types
  user_bike_counts = combined_df.groupby(['user_type', 'rideable_type']).size().unstack(fill_value=0)
  user_bike_counts.reset_index(inplace=True)
  user_bike_counts_json = user_bike_counts.to_json(split='orient')
  print(user_bike_counts)

  # Analyze How Bike Type Affects Trip Duration
  combined_df['distance_km'] = combined_df.apply(calculate_distance, axis=1)
  combined_df['duration_per_km'] = combined_df['trip_duration (s)'] / combined_df['distance_km']
  bike_duration_analysis = combined_df.groupby('rideable_type')['duration_per_km'].describe()
  bike_duration_analysis_json = bike_duration_analysis.to_json(orient='split')


  return {
    "bike_type_counts": bike_counts_json,
    "user_type_bike_type_counts": user_bike_counts_json,
    "bike_duration_analysis": bike_duration_analysis_json
  }

def calculate_distance(row):
    start_coords = (row['start_lat'], row['start_lng'])
    end_coords = (row['end_lat'], row['end_lng'])
    return geodesic(start_coords, end_coords).kilometers


def max_vs_min_trips_metrics():
  file_path = 'cleaned_trip_membership_usage_revenue_data.csv'
  full_path = os.path.join(data_base_path, file_path)

  df = pd.read_csv(full_path)
  df['month_year'] = pd.to_datetime(df['month_year'])
  df['year'] = df['month_year'].dt.year

  df = df[df['year'] != 2016]

  df['total_trips'] = df['annual_member_trips'] + df['casual_trips']

  trips_by_year = df.groupby('year')['total_trips'].agg(['max', 'min'])

  trips_by_year['difference'] = trips_by_year['max'] - trips_by_year['min']

  trips_by_year_json = trips_by_year.to_json(orient='split')

  return trips_by_year_json


def membership_usage_revenue_metrics():
  file_path = 'cleaned_trip_membership_usage_revenue_data.csv'
  full_path = os.path.join(data_base_path, file_path)

  df = pd.read_csv(full_path)
  df['month_year'] = pd.to_datetime(df['month_year'])
  df['year'] = df['month_year'].dt.year

  df = df[df['year'] != 2016]

  usage_revenue = df.groupby('month_year').agg({
    'annual_member_trips': 'sum',
    'casual_trips': 'sum',
    'membership_revenue': 'sum',
    'casual_ridership_revenue': 'sum',
  })

  usage_revenue['total_trips'] = usage_revenue['annual_member_trips'] + usage_revenue['casual_trips']
  usage_revenue['total_revenue'] = usage_revenue['membership_revenue'] + usage_revenue['casual_ridership_revenue']
  usage_revenue['annual_member_trip_percentage'] = (usage_revenue['annual_member_trips'] / usage_revenue['total_trips']) * 100
  usage_revenue['casual_trip_percentage'] = (usage_revenue['casual_trips'] / usage_revenue['total_trips']) * 100
  usage_revenue['membership_revenue_percentage'] = (usage_revenue['membership_revenue'] / usage_revenue['total_revenue']) * 100
  usage_revenue['casual_revenue_percentage'] = (usage_revenue['casual_ridership_revenue'] / usage_revenue['total_revenue']) * 100
  
  return usage_revenue.to_json(orient='split')
  
