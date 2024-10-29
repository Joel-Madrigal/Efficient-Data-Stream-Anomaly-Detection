import random
import matplotlib

def get_season_temp(day_of_year):
    '''
    This method serves as a helper to avoid repetition in the superceding two methods. We need this 
    because I use similar logic in both to find ranges of temperatures depending on season. Gives us 
    ranges of temperatues I decided based upon its' season.
    
    Parameters:
        day_of_year(int): The day in the year.

    Returns:
        tuple(int: int): The temperature range for the current season.
    '''
    seasonal_temp = {
        'spring': (50, 80),
        'summer': (80, 110),
        'autumn': (20, 50),
        'winter': (-10, 20)
    }

    # Check for seasonal temp ranges.    
    if day_of_year <= 60 or day_of_year > 300:
        return seasonal_temp['winter']
    elif day_of_year > 60 and day_of_year <= 150:
        return seasonal_temp['spring']
    elif day_of_year > 150 and day_of_year <= 240:
        return seasonal_temp['summer']
    else:
        return seasonal_temp['autumn']


def data_stream(years, get_season_temp):
    '''
    This method creates an array of temperatures(farenheit) of # of years of
    your choice. The created data stream contains some manufactured 'anomalies'
    desinged to be random and picked up purposefully by the anomaly detecting
    algorithm. Order of Jan 1st - Dec 31.

    Parameters:
        years(int): Years to represent how many days we get back in the array.
        get_season_temp(tuple -> (int: int)): Tuple providing range of temperatures for given day in season.

    Returns:
        data_holder(array -> floats): Temperatures.
    '''

    # Final data_stream array storage
    data_holder = []

    # Calculate days in x-years.
    days = years * 365

    # Accumulator for logging # of years to the array.
    year = 0

    # 3% chance theres an anomaly - so to speak.
    spike_chance = 0.03

    for i in range(days):

        # Determining day of said year, so we can use in a range.
        day_of_year = i % 365
        temp_range = get_season_temp(day_of_year)

        # If a year has gone by, increment accumulator and store in array.
        if i % 365 == 0:
            year += 1
            data_holder.append(year)

        # 'Randomly' choose a temperature from said temp range.
        daily_temp = random.uniform(*temp_range)

        # Check if randomly generated float is less than .03, add or subtract 40
        # to the corresponding temperature score if that is the case.
        if random.random() < spike_chance:
            spike_applier = random.uniform(-40, 40)
            daily_temp += spike_applier
        
        # Round our number to more readable 2 dec. places.
        usable = round(daily_temp, 2)

        # Add temps. to the array.
        data_holder.append(usable)

    return data_holder



def anomaly_detector(stream, get_season_temp):
    '''
    Method for determining anomalies in the stream produced from the data_stream
    method. 

    Parameters:
        stream(array -> floats): Data stream fetched from the data_stream method.
        get_season_temp(tuple -> (int: int)): Tuple providing range of temperatures for given day in season.

    Returns:
        anomalies(dict -> int: array -> floats): Dictionary representing the
        anomalies of which occured in that year.
    '''

    # Dict for our final return dictionary
    anomalies = {}

    # Buffer value to run the temperatures against to determine if they are normal or anomalistic.
    buffer = 20
    
    for i in range(len(stream)):

        # Dynamically update years to serve as readability when looking at the dict.
        years = (i // 365) + 1

        # Current day in the data_stream, used as argument for helper function to give us a range of temps.
        day_of_year = i % 365

        # Initialize dictionary with fillable values and keys.
        if years not in anomalies:
            anomalies[years] = []

        # Call helper to get range of temps.
        temp_range = get_season_temp(day_of_year)

        # Use buffer to determine if we spill over the normal max range or if we fall under.
        # Either way, its anomalistic.
        if stream[i] > temp_range[1] + buffer or stream[i] < temp_range[0] - buffer:
            anomalies[years].append(stream[i])

    return anomalies


print(anomaly_detector(data_stream(2, get_season_temp), get_season_temp))

def visualize_data_and_anomalies(years):
    temperature_data = data_stream(years, get_season_temp)
    anomalies = anomaly_detector(temperature_data, get_season_temp)

    # Plotting the data
    plt.figure(figsize=(15, 6))
    plt.plot(temperature_data, label='Temperature Data', color='blue', alpha=0.6)

    # Highlighting the anomalies
    for year, anomaly_temps in anomalies.items():
        anomaly_indices = [(i + (year - 1) * 365) for i in range(len(temperature_data)) if temperature_data[i] in anomaly_temps]
        plt.scatter(anomaly_indices, [temperature_data[i] for i in anomaly_indices], color='red', label='Anomalies' if year == 1 else "", zorder=5)

    plt.title(f'Temperature Data and Anomalies Over {years} Years')
    plt.xlabel('Days')
    plt.ylabel('Temperature (°F)')
    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.legend()
    plt.grid()
    plt.show()

# Example usage
visualize_data_and_anomalies(90)
