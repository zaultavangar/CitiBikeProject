import sys
import os
import pandas as pd
from tqdm import tqdm
from tabulate import tabulate
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from utils import calculate_trip_cost
from predict import forecast_trips

COLUMN_MAPPINGS = {
    2016: {
        'tripduration': 'trip_duration',
        'starttime': 'started_at',
        'stoptime': 'ended_at',
        'start station id': 'start_station_id',
        'start station name': 'start_station_name',
        'start station latitude': 'start_lat',
        'start station longitude': 'start_lng',
        'end station id': 'end_station_id',
        'end station name': 'end_station_name',
        'end station latitude': 'end_lat',
        'end station longitude': 'end_lng',
        'bikeid': 'bike_id',
        'usertype': 'user_type',
    },
    2017: {
        'tripduration': 'trip_duration',
        'starttime': 'started_at',
        'stoptime': 'ended_at',
        'start station id': 'start_station_id',
        'start station name': 'start_station_name',
        'start station latitude': 'start_lat',
        'start station longitude': 'start_lng',
        'end station id': 'end_station_id',
        'end station name': 'end_station_name',
        'end station latitude': 'end_lat',
        'end station longitude': 'end_lng',
        'bikeid': 'bike_id',
        'usertype': 'user_type',
    },
    2018: {
        'tripduration': 'trip_duration',
        'starttime': 'started_at',
        'stoptime': 'ended_at',
        'start station id': 'start_station_id',
        'start station name': 'start_station_name',
        'start station latitude': 'start_lat',
        'start station longitude': 'start_lng',
        'end station id': 'end_station_id',
        'end station name': 'end_station_name',
        'end station latitude': 'end_lat',
        'end station longitude': 'end_lng',
        'bikeid': 'bike_id',
        'usertype': 'user_type',
    },
    2019: {
        'tripduration': 'trip_duration',
        'starttime': 'started_at',
        'stoptime': 'ended_at',
        'start station id': 'start_station_id',
        'start station name': 'start_station_name',
        'start station latitude': 'start_lat',
        'start station longitude': 'start_lng',
        'end station id': 'end_station_id',
        'end station name': 'end_station_name',
        'end station latitude': 'end_lat',
        'end station longitude': 'end_lng',
        'bikeid': 'bike_id',
        'usertype': 'user_type',
    },
    2020: {
        'tripduration': 'trip_duration',
        'starttime': 'started_at',
        'stoptime': 'ended_at',
        'start station id': 'start_station_id',
        'start station name': 'start_station_name',
        'start station latitude': 'start_lat',
        'start station longitude': 'start_lng',
        'end station id': 'end_station_id',
        'end station name': 'end_station_name',
        'end station latitude': 'end_lat',
        'end station longitude': 'end_lng',
        'bikeid': 'bike_id',
        'usertype': 'user_type',
    },
    2021: {
        'ride_id': 'ride_id',
        'rideable_type': 'rideable_type',
        'started_at': 'started_at',
        'ended_at': 'ended_at',
        'start_station_name': 'start_station_name',
        'start_station_id': 'start_station_id',
        'end_station_name': 'end_station_name',
        'end_station_id': 'end_station_id',
        'start_lat': 'start_lat',
        'start_lng': 'start_lng',
        'end_lat': 'end_lat',
        'end_lng': 'end_lng',
        'member_casual': 'user_type',
        'tripduration': 'trip_duration',
        'bikeid': 'bike_id',
    },
    2022: {
        'ride_id': 'ride_id',
        'rideable_type': 'rideable_type',
        'started_at': 'started_at',
        'ended_at': 'ended_at',
        'start_station_name': 'start_station_name',
        'start_station_id': 'start_station_id',
        'end_station_name': 'end_station_name',
        'end_station_id': 'end_station_id',
        'start_lat': 'start_lat',
        'start_lng': 'start_lng',
        'end_lat': 'end_lat',
        'end_lng': 'end_lng',
        'member_casual': 'user_type',
    },
    2023: {
        'ride_id': 'ride_id',
        'rideable_type': 'rideable_type',
        'started_at': 'started_at',
        'ended_at': 'ended_at',
        'start_station_name': 'start_station_name',
        'start_station_id': 'start_station_id',
        'end_station_name': 'end_station_name',
        'end_station_id': 'end_station_id',
        'start_lat': 'start_lat',
        'start_lng': 'start_lng',
        'end_lat': 'end_lat',
        'end_lng': 'end_lng',
        'member_casual': 'user_type',
    }
}

COMMON_COLUMNS = ['started_at', 'ended_at', 'start_station_id', 'start_station_name', 'start_lat', 'start_lng', 'end_station_id', 'end_station_name', 'end_lat', 'end_lng', 'trip_duration', 'bike_id', 'user_type']

def getBaseCitibikePath(year):
    return f'/Users/zaultavangar/Desktop/Comp Sci/CitiBikeProject/citibike-data/{year}-citibike-tripdata'

def getCitiBikeFilePaths(year):
    return [
        f'1_January/{year}01-citibike-tripdata_1.csv',
        f'1_January/{year}01-citibike-tripdata_2.csv',
        f'2_February/{year}02-citibike-tripdata_1.csv',
        f'2_February/{year}02-citibike-tripdata_2.csv',
        f'3_March/{year}03-citibike-tripdata_1.csv',
        f'3_March/{year}03-citibike-tripdata_2.csv',
        f'3_March/{year}03-citibike-tripdata_3.csv',
        f'4_April/{year}04-citibike-tripdata_1.csv',
        f'4_April/{year}04-citibike-tripdata_2.csv',
        f'4_April/{year}04-citibike-tripdata_3.csv',
        f'5_May/{year}05-citibike-tripdata_1.csv',
        f'5_May/{year}05-citibike-tripdata_2.csv',
        f'5_May/{year}05-citibike-tripdata_3.csv',
        f'5_May/{year}05-citibike-tripdata_4.csv',
        f'6_June/{year}06-citibike-tripdata_1.csv',
        f'6_June/{year}06-citibike-tripdata_2.csv',
        f'6_June/{year}06-citibike-tripdata_3.csv',
        f'6_June/{year}06-citibike-tripdata_4.csv',
        f'7_July/{year}07-citibike-tripdata_1.csv',
        f'7_July/{year}07-citibike-tripdata_2.csv',
        f'7_July/{year}07-citibike-tripdata_3.csv',
        f'7_July/{year}07-citibike-tripdata_4.csv',
        f'8_August/{year}08-citibike-tripdata_1.csv',
        f'8_August/{year}08-citibike-tripdata_2.csv',
        f'8_August/{year}08-citibike-tripdata_3.csv',
        f'8_August/{year}08-citibike-tripdata_4.csv',
        f'8_August/{year}08-citibike-tripdata_5.csv',
        f'9_September/{year}09-citibike-tripdata_1.csv',
        f'9_September/{year}09-citibike-tripdata_2.csv',
        f'9_September/{year}09-citibike-tripdata_3.csv',
        f'9_September/{year}09-citibike-tripdata_4.csv',
        f'10_October/{year}10-citibike-tripdata_1.csv',
        f'10_October/{year}10-citibike-tripdata_2.csv',
        f'10_October/{year}10-citibike-tripdata_3.csv',
        f'10_October/{year}10-citibike-tripdata_4.csv',
        f'11_November/{year}11-citibike-tripdata_1.csv',
        f'11_November/{year}11-citibike-tripdata_2.csv',
        f'11_November/{year}11-citibike-tripdata_3.csv',
        f'12_December/{year}12-citibike-tripdata_1.csv',
        f'12_December/{year}12-citibike-tripdata_2.csv',
        f'12_December/{year}12-citibike-tripdata_3.csv'
    ]

def getTripsPerDayFilePaths():
    years = list(range(2016, 2024))
    file_paths = []
    for year in years:
        file_paths.append(f'/Users/zaultavangar/Desktop/Comp Sci/CitiBikeProject/citibike-data/{year}-citibike-tripdata/final_{year}_trip_data.csv')
    return file_paths

base_weather_path = '/Users/zaultavangar/Desktop/Comp Sci/CitiBikeProject/weather-data'
initial_weather_data_file_path = 'daily-weather-data-cp.csv'

# Most active stations 
# Most common routes

# Predict most active stations 
  # By time of day 
  # By month 

# Estimate revenue


pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def load_and_preprocess_citibike_trip_data(year, sample_fraction=0.15):
    base_path = getBaseCitibikePath(year)
    final_file_path = os.path.join(base_path, f'final_{year}_trip_data.csv')

    if os.path.exists(final_file_path):
        print(f'Trip Data :: {final_file_path} already exists. Skipping preprocessing and loading the existing file')
        chunks = pd.read_csv(final_file_path, chunksize=10000)
        return pd.concat(chunks, ignore_index=True)

    all_data = []
    for file_path in getCitiBikeFilePaths(year):
        full_path = os.path.join(base_path, file_path)

        if not os.path.exists(full_path):
            print(full_path)
            continue

        total_lines = sum(1 for _ in open(full_path))
        print(f"Total lines in {full_path}: ", total_lines)

        header_df = pd.read_csv(full_path, nrows=1)
        chunks = pd.read_csv(full_path, chunksize=10000)

        sampled_chunks = []
        for chunk in tqdm(chunks, total=total_lines//10000, desc=f"Reading CitiBike Trip Data from {file_path}"):
            sampled_chunk = chunk.sample(frac=sample_fraction, random_state=1)
            sampled_chunks.append(sampled_chunk)

        df = pd.concat(sampled_chunks, ignore_index=True)

        df.columns = header_df.columns

        # Rename columns based on year
        if year in COLUMN_MAPPINGS:
            df.rename(columns=COLUMN_MAPPINGS[year], inplace=True)
        
        # Standardize user_type values
        if 'user_type' in df.columns:
            df['user_type'] = df['user_type'].replace({'Subscriber': 'member', 'Customer': 'casual'})

        # Keep only the common columns

        common_cols = COMMON_COLUMNS.copy()
        if year > 2021:
            common_cols.append('rideable_type')
            
        df = df[[col for col in common_cols if col in df.columns]]

        # Remove any rows with null values in any of the columns
        df.dropna(axis=0, how='any', inplace=True)

        # Convert date columns to datetime
        df['started_at'] = pd.to_datetime(df['started_at'])
        df['ended_at'] = pd.to_datetime(df['ended_at'])

        # Calculate trip duration in minutes
        df['trip_duration (s)'] = (df['ended_at'] - df['started_at']).dt.total_seconds()

        # Filter out trips with negative or zero duration
        df = df[df['trip_duration (s)'] > 0]

        if 'rideable_type' in df.columns:
            df['trip_cost ($)'] = df.apply(calculate_trip_cost, axis=1)

        # Check for and remove any duplicates
        df.drop_duplicates(inplace=True)

        all_data.append(df)

    # Concatenate all the data together
    final_df = pd.concat(all_data, ignore_index=True)
    final_df['month_year'] = final_df['started_at'].dt.to_period('M')

    # TRIPS PER DAY
    final_df['date'] = final_df['started_at'].dt.date

    final_df.to_csv(os.path.join(base_path, final_file_path), index=False)
   
    return final_df

def load_and_preprocess_weather_data(base_path, file_path, start_date, end_date):
    full_path = os.path.join(base_path, file_path)
    final_file_path = os.path.join(base_path, f'final_daily_weather_data_cp_{start_date[:4]}_{end_date[:4]}.csv')

    if os.path.exists(final_file_path):
        print(f'Weather Data :: {final_file_path} already exists. Skipping preprocessing and loading the existing file')
        return pd.read_csv(final_file_path)

    total_lines = sum(1 for _ in open(full_path))

    header_df = pd.read_csv(full_path)
    chunks = pd.read_csv(full_path, chunksize=10000)
    df = pd.concat([chunk for chunk in tqdm(chunks, total=(total_lines//10000), desc="Reading Daily Weather Data CSV")])

    df.columns = header_df.columns

    df['DATE'] = pd.to_datetime(df['DATE'])

    df = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date)]

    df.rename(columns={'DATE': 'date'}, inplace=True)

    # ADPT = Adapted Temperature, RHAV = Average Relative Humidity, Other? 'WSFG', 'ELEVATION'

    df = df[['date', 'PRCP', 'SNOW', 'TMAX', 'TMIN',]]
    df['TMAX'] = df['TMAX']/10.0;
    df['TMIN'] = df['TMIN']/10.0;
    df['TAVG'] = ((df['TMAX']+df['TMIN'])/2.0).round(2)

    df.to_csv(os.path.join(base_path, final_file_path), index=False)

    return df

def save_and_combine_trips_per_day(sample_fraction=0.15):
    final_file_path = '/Users/zaultavangar/Desktop/Comp Sci/CitiBikeProject/citibike-data/trips_per_day_2016_2023.csv'
    if os.path.exists(final_file_path):
        print(f'{final_file_path} Already exists, retrieving saved CSV...')
        df = pd.read_csv(final_file_path)
        return df

    all_data = []

    file_paths = getTripsPerDayFilePaths();
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f'File path {file_path} does not exist, skipping')
            continue

        chunk_size = 10000
        chunk_list = []
        total_lines = sum(1 for _ in open(file_path)) -1
        chunks = pd.read_csv(file_path, chunksize=chunk_size)
        for chunk in tqdm(pd.read_csv(file_path, chunksize=chunk_size), 
                          total=total_lines//chunk_size,
                          desc=f'Reading {file_path}'
                          ):
            chunk_list.append(chunk)
        
        df = pd.concat(chunks, ignore_index=True)
        trips_per_day = df.groupby('date').size().reset_index(name = 'num_trips')

        trips_per_day['num_trips'] = round(trips_per_day['num_trips'] / sample_fraction, 0)

        all_data.append(trips_per_day)

        print(tabulate(trips_per_day.head(5), headers='keys', tablefmt='pqsl'))
    
    all_trips_per_day = pd.concat(all_data, ignore_index=True)

    all_trips_per_day.to_csv(final_file_path, index=False)

    print(tabulate(all_trips_per_day.sample(20), headers='keys', tablefmt='pqsl'))

    return all_trips_per_day


def save_monthly_revenue(file_path, year, membership_cost, average_member_rides_per_year = 120, sample_fraction = 0.15):
    ## ONLY FOR 2022-2023
    print('Can only get revenue information for after (and including) 2022')

    base_path = getBaseCitibikePath(year)
    full_path = os.path.join(base_path, file_path)

    chunks = pd.read_csv(full_path, chunksize=10000)
    df = pd.concat(chunks, ignore_index=True)

    monthly_revenue = df.groupby('month_year')['trip_cost ($)'].sum().reset_index()
    monthly_revenue.rename(columns={'trip_cost ($)': 'Revenue ($)'}, inplace=True)

    num_members = df[df['user_type'] == 'member'].count()
    num_non_members = df[df['user_type'] == 'casual'].count()

    # Note: on average, a Citi Bike member takes approximately 120 rides annually
    estimated_annual_revenue_from_memberships = membership_cost * (num_members / sample_fraction) / average_member_rides_per_year
    monthly_revenue['Revenue ($)'] += estimated_annual_revenue_from_memberships/12

    monthly_revenue.to_csv(os.path.join(base_path, f'final_{year}_monthly_revenue.csv'), index=False)

def getCitibikeTripData(year):
    final_citibike_trip_data = load_and_preprocess_citibike_trip_data(year)
    print(f'CITIBIKE TRIP DATA FOR {year}')
    print(tabulate(final_citibike_trip_data.head(10), headers='keys', tablefmt='psql'))
    print(f'{year} trip data #rows: {str(len(final_citibike_trip_data))}')

def getWeatherData(start_date, end_date):
    final_weather_data = load_and_preprocess_weather_data(
        base_path=base_weather_path, 
        file_path= initial_weather_data_file_path,
        start_date=start_date,
        end_date=end_date
    )

    print(f'WEATHER DATA FROM {start_date[:4]} to {end_date[:4]}')
    print(tabulate(final_weather_data.head(20), headers='keys', tablefmt='psql'))
    print('Weather data #rows: ' + str(len(final_weather_data)))


def predict(end_year, specific_date = None):
    trips_per_day_base_path = '/Users/zaultavangar/Desktop/Comp Sci/CitiBikeProject/citibike-data'
    trips_per_day_file_path = 'trips_per_day_2016_2023.csv'
    trips_per_day_full_path = os.path.join(trips_per_day_base_path, trips_per_day_file_path)

    trips_per_day_2016_2023 = pd.read_csv(trips_per_day_full_path)

    weather_data_base_path = '/Users/zaultavangar/Desktop/Comp Sci/CitiBikeProject/weather-data'
    weather_data_file_path='final_daily_weather_data_cp_2016_2023.csv'
    weather_data_full_path = os.path.join(weather_data_base_path, weather_data_file_path)
    
    weather_data = pd.read_csv(weather_data_full_path)
    
    predictions = forecast_trips(trips_per_day_2016_2023, weather_data, end_year)

    print(tabulate(predictions.sample(50), headers='keys', tablefmt='pqsl'))

    if specific_date:
        specific_date = pd.to_datetime(specific_date)
        specific_prediction = predictions[predictions['ds'] == specific_date]
        if not specific_prediction.empty:
            estimated_trips = round(specific_prediction['yhat'].values[0],0)
            print(f'Estimated trips for {specific_date.date()}: {estimated_trips}')
        else:
            print(f'No prediction available for {specific_date.date()}')

    predictions['year'] = predictions['ds'].dt.year
    predictions['month'] = predictions['ds'].dt.month

    warmest_months = [6, 7, 8]
    coldest_months = [12, 1, 2]

    # Calculate the average number of trips for warmest and coldest months
    average_trips = predictions.groupby(['year', 'month'])['yhat'].mean().reset_index()

    warmest_avg = average_trips[average_trips['month'].isin(warmest_months)].groupby('year')['yhat'].mean()
    coldest_avg = average_trips[average_trips['month'].isin(coldest_months)].groupby('year')['yhat'].mean()

    # Calculate the difference between warmest and coldest months' averages for each year
    diff_avg = warmest_avg - coldest_avg
    diff_avg = diff_avg.reset_index().rename(columns={'yhat': 'diff'})

    print("\nDifference Between Warmest and Coldest Months' Average Number of Trips by Year:")
    print(tabulate(diff_avg, headers='keys', tablefmt='psql'))

    # PLOT - CitiBike Trip Forecast
    plt.figure(figsize=(15, 8))
    plt.plot(trips_per_day_2016_2023['date'], trips_per_day_2016_2023['num_trips'], label='Historical Data')
    plt.plot(predictions['ds'], predictions['yhat'], label='Forecasted Data')
    plt.fill_between(predictions['ds'], predictions['yhat_lower'], predictions['yhat_upper'], color='gray', alpha=0.2, label='Confidence Interval')
    plt.axvline(pd.to_datetime('2023-12-31'), color='red', linestyle='--', label='Forecast Start')
    plt.xlabel('Date')
    plt.ylabel('Number of Trips')
    plt.title('CitiBike Trip Forecast')
    plt.legend()

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 6)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.xticks(rotation=90)

    plt.show()

    # PLOT - Difference Between Warmest and Coldest Months' Average Number of Trips by Year
    plt.figure(figsize=(15, 8))
    plt.plot(diff_avg['year'], diff_avg['diff'], marker='o', linestyle='-')
    plt.xlabel('Year')
    plt.ylabel('Difference in Number of Trips')
    plt.title("Difference Between Warmest and Coldest Months' Average Number of Trips by Year")
    plt.grid(True)

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xticks(rotation=45)

    plt.show()

   

# predictFutureTrips()
# getCitibikeTripData(2022)
# getWeatherData('2016-01-01', '2023-12-31')
# save_and_combine_trips_per_day()
predict(2050, '2025-12-30')








