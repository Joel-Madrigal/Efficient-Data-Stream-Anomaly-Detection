import random


def data_stream(years):
    '''
    This method creates an array of temperatures(farenheit) of # of years of
    your choice. The created data stream contains some manufactured 'anomalies'
    desinged to be random and picked up purposefully by the anomaly detecting
    algorithm. Order of Jan 1st - Dec 31.

    Parameters:
        years(int): Years to represent how many days we get back in the array.

    Returns:
        data_holder(array -> floats): Temperatures.
    '''

    # Dict to store seasonal temp ranges.
    seasonal_temp = {
        'spring': (50, 80),
        'summer': (80, 110),
        'autumn': (20, 50),
        'winter': (-10, 20)
    }

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
        season_determiner = i % 365

        # If a year has gone by, increment accumulator and store in array.
        if i % 365 == 0:
            year += 1
            data_holder.append(year)

        # Fetch corresponding temperature range for season in dictionary.
        if season_determiner <= 60 or season_determiner > 300:
            temp_range = seasonal_temp['winter']
        elif season_determiner > 60 and season_determiner <= 150:
            temp_range = seasonal_temp['spring']
        elif season_determiner > 150 and season_determiner <= 240:
            temp_range = seasonal_temp['summer']
        else:
            temp_range = seasonal_temp['autumn']

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


def anomaly_detector(stream):
    '''
    Method for determining anomalies in the stream produced from the data_stream
    method. 

    Parameters:
        stream(array -> floats): Data stream fetched from the data_stream method.

    Returns:
        anomalies(dict -> int: array -> floats): Dictionary representing the
        anomalies of which occured in that year.
    '''
    anomalies = {}
    norm_range = 30
    # anomaly_buffer = 40

    for i in range(len(stream)):
        top_bound = stream[i] + norm_range
        lower_bound = stream[i] - norm_range

        years = i // 365 + 1

        if years not in anomalies:
            anomalies[years] = []

        if stream[i] > top_bound:
            anomalies[years].append(stream[i])

        elif stream[i] < lower_bound:
            anomalies[years].append(stream[i])

    return anomalies


print(anomaly_detector(data_stream(10)))
