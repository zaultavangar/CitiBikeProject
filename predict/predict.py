import pandas as pd
from prophet import Prophet
import numpy as np
from tabulate import tabulate
from sklearn.metrics import mean_absolute_error, mean_squared_error


# 2013-07-01
def forecast_trips(trips_per_day_2016_2023, weather_data, end_year):
    trips_per_day_2016_2023['date'] = pd.to_datetime(trips_per_day_2016_2023['date'])
    weather_data['date'] = pd.to_datetime(weather_data['date'])
    weather_data = weather_data[['date', 'TMAX', 'TMIN', 'TAVG', 'PRCP']]

    complete_date_range = pd.date_range(start=trips_per_day_2016_2023['date'].min(), end=trips_per_day_2016_2023['date'].max(), freq='D')
    trips_per_day_2016_2023 = trips_per_day_2016_2023.set_index('date').reindex(complete_date_range).rename_axis('date').reset_index()
    trips_per_day_2016_2023['num_trips'].ffill(inplace=True)
    trips_per_day_2016_2023['num_trips'].bfill(inplace=True)
    
    # Merge trip data with weather data
    merged_df = pd.merge(trips_per_day_2016_2023, weather_data, on='date', how='left')

    print(tabulate(merged_df.head(10), headers='keys', tablefmt='pqsl'));
        
    # Identify missing dates
    missing_dates = complete_date_range.difference(merged_df['date'])
    print(f'Missing Dates: {len(missing_dates)}')
    print(missing_dates)

    # Reindex the dataframe to include all dates in the range
    merged_df = merged_df.set_index('date').reindex(complete_date_range).rename_axis('date').reset_index()

    weather_columns = ['TMAX', 'TMIN', 'TAVG', 'PRCP']
    merged_df = fill_missing_with_monthly_median(merged_df, weather_columns)

    df_prophet = merged_df.rename(columns={'date': 'ds', 'num_trips': 'y'})


    model = Prophet(
        daily_seasonality=True,
        yearly_seasonality=True,
    )
    model.add_seasonality(name='monthly', period=30.5, fourier_order=2)

    # Add weather data as regressors
    for col in weather_columns:
        model.add_regressor(col, prior_scale=20.0, standardize=True)


    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=(end_year-2023)*365, freq='D')

    # Merge future dataframe with weather data
    future = pd.merge(future, weather_data, left_on='ds', right_on='date', how='left')
    future.drop(columns=['date'], inplace=True)

    future = future.rename(columns={'ds': 'date'})
    future = fill_missing_with_monthly_median(future, weather_columns)
    future = future.rename(columns={'date': 'ds'})

    forecast = model.predict(future)

    train_forecast = model.predict(df_prophet)
    mae = mean_absolute_error(df_prophet['y'], train_forecast['yhat'])
    mse = mean_squared_error(df_prophet['y'], train_forecast['yhat'])
    rmse = np.sqrt(mse)
    
    print(f'Model Performance:')
    print(f'MAE: {mae}')
    print(f'RMSE: {rmse}')

    # Return the forecasted values
    return forecast

def fill_missing_with_monthly_median(df, weather_columns):
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    for col in weather_columns:
        for index, row in df[df[col].isnull()].iterrows():
            month = row['month']
            year = row['year']

            # Try to fill missing value with median for the same month and year
            median_val = df[(df['month'] == month) & (df['year'] == year)][col].median()

            # If the median value for the same month and year is NaN, use the median from the previous year
            if pd.isna(median_val):
                median_val = df[(df['month'] == month) & (df['year'] == year - 1)][col].median()

            # If still NaN, use the overall median
            if pd.isna(median_val):
                median_val = df[col].median()

            df.at[index, col] = median_val

    df.drop(columns=['month', 'year'], inplace=True)
    return df