import pandas as pd

def calculate_trip_cost(row):  
    output = 0.0  
    if row['user_type'] == 'member':
        if row['rideable_type'] == 'classic_bike':
            if row['trip_duration (s)'] > 45*60:
                output = 0.24 * (row['trip_duration (s)'] - 45*60)
        elif row['rideable_type'] == 'electric_bike':
            output = 0.24 * (row['trip_duration (s)']/60.0)
    elif row['user_type'] == 'casual':
        if row['rideable_type'] == 'classic_bike':
            if row['trip_duration (s)'] > 30*60:
                output = 4.79 + 0.36 * (row['trip_duration (s)'] - 30*60)
            else:
                output = 4.79
        elif row['rideable_type'] == 'electric_bike':
            output =  0.36 * (row['trip_duration (s)']/60.0)
    
    return round(output, 2)