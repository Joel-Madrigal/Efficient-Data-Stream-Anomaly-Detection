import random
import matplotlib.pyplot as plt

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

    # Handle bad data.
    if not isinstance(years, int) or years <= 0:
        raise ValueError("Enter positive integers.")

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
    
    Reason as to why this algorithm is efficient, clean, and accurate:
    This algorithm runs in linear time complexity, we know this because we iterate
    through our stream length once, iteratively. Looking at the space allocation and efficiency,
    this is very efficient through the use of constant data structures like a dictionary for fast lookups and insertions.
    Not only this, but its accurate and effective because we don't utilize the seasonal 
    dictionary to have fast lookup of a range of temperatures, from which we can determine 
    if the current tempurature is anomalistic due to bounds checking. On top of this, we add 
    a buffer value to avoid false positive data and focus on data points that truly are anomalies.

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
    buffer = 10
    
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


def visualize_data_and_anomalies(years):
    '''
    Method to visually display anomalies on top of the original data stream.
    Reference: https://www.w3schools.com/python/matplotlib_intro.asp

    Parameters:
        years(int): Used to create the data stream and anomaly methods.

    Returns:
        None
    '''

    # Get the data stream and anomaly data.
    stream = data_stream(years, get_season_temp)
    anomalies = anomaly_detector(stream, get_season_temp)

    # Plot the original data stream, make it blue and give it a legent label.
    plt.plot(stream, label='Temperature Data', color='blue')

    # Used to prevent mass printing of anomalies on the legend
    anomaly_labeled = False  

    # This was tricky, first, dictname.values() is the only way I know how to 
    # extract dictionary data out to a list, instead of other finnicky data types.
    for anomaly_vals in anomalies.values():

        # So now since anomaly_vals is a list with the anomaly data, 
        # lets loop through it to manipulate the actual floats.
        for anom in anomaly_vals:

            # Find the index of said anomaly in the original data stream so it can be represented usefully in the plot.
            anomaly_index = stream.index(anom)

            # If we haven't labeled the legend for anomalies yet, plot the anomalies and label the legend.  
            if anomaly_labeled == False:
                plt.scatter(anomaly_index, anom, color='red', label='Anomalies')

            # If we have, do same, just don't keep adding anomaly to the legend.
            else:
                plt.scatter(anomaly_index, anom, color='red', label='')
            anomaly_labeled = True  

    # Standard plotlib markup.
    plt.title(f'Temperature Data and Anomalies Over {years} Years')
    plt.xlabel('Days')
    plt.ylabel('Temperature (°F)')
    plt.axhline(0, color='black', linewidth=0.5)
    plt.legend()
    plt.show()


def main():
    print('data_stream of 1 year: ', data_stream(1, get_season_temp))
    print('data_stream of 5 years: ', data_stream(5, get_season_temp))
    print('data_stream of 50 years: ', data_stream(50, get_season_temp))

    print('anomaly_detector of 1 year: ', anomaly_detector(data_stream(1, get_season_temp), get_season_temp))
    print('anomaly_detector of 5 years: ', anomaly_detector(data_stream(5, get_season_temp), get_season_temp))
    print('anomaly_detector of 50 years: ', anomaly_detector(data_stream(50, get_season_temp), get_season_temp))

    # Run these one at a time:
    visualize_data_and_anomalies(1)
    #visualize_data_and_anomalies(5)
    #visualize_data_and_anomalies(50)

main()