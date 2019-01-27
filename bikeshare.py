import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Input:
        (str) city_input - user entered name of the city to analyze
        (str) time_input - user entered decision regarding time filter preferences. takes values 'month', 'day', and 'none'
        (str) month_input - user entered name of the month to analyze
        (str) day_input - user entered day of week to analyze
    
    List:
        month_list - available month names in the data for comparison with entered month_input
        day_list - available day names in the data for comparison with entered day_input
        
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). 
    # HINT: Use a while loop to handle invalid inputs
    
    # CITY
    while True:
        try:
            city_input = input("Would you like to see data for Chicago, New York City, or Washington? \n").lower().strip()
            if city_input != 'chicago' and city_input!='new york city' and city_input != 'washington':
                print('That\'s not a valid city name! Please try it again')                     
            else:        
                city = city_input
                #print(city)
                print('That\'s a valid city name!')        
                break
        except (ValueError, KeyboardInterrupt):
            print('You run in an error!')  
            
    print('-'*40)   
         
    time_input = input("Would you like to filter the data by month, day, or not at all (none)?\n").lower().strip()
    #print(time_input)
    
    # get user input for month (all, january, february, ... , june)

    if time_input == 'month':
        # MONTH
        months_list = ['january', 'february', 'march', 'april', 'may', 'june']
        
        while True:
            try:
                print('-'*40)
                month_input = input("Which month - January, February, March, April, May, or June? \n").lower().strip()
                if month_input not in months_list:
                    print('That\'s not a valid month name! Please try it again')                     
                else:        
                    month = month_input
                    day = 'all'
                    #print(month)
                    print('That\'s a valid month name!')        
                    break
            except (ValueError, KeyboardInterrupt):
                print('You run in an error!')
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
        
    elif time_input == 'day':
        # DAY
        days_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        while True:
            try:
                print('-'*40)
                day_input = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? \n').lower().strip()
                if day_input not in days_list:
                    print('That\'s not a valid day! Please try it again') 
                else:        
                    day = day_input
                    month = 'all'
                    #print(day)
                    print('That\'s a valid day name!')        
                    break
            except (ValueError, KeyboardInterrupt):
                print('That\'s not a valid day! Please try it again!')
                
    # get user input when month and days are not selected
    elif time_input == 'none': 
        month = 'all'
        day = 'all'
    else:
        month = 'na'
        day = 'na'
        city = 'na'
        print('Ops.. something goes wrong. Please restart the program!')

    print('-'*40)
    return city , month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
	
	# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # I. display the most common MONTH

    if month == 'all':
        
        # create a dictionary with month names for displaying full name instead of numbers
        month_names = {'1' : 'January', '2' : 'February', '3' : 'March', '4' : 'April', '5' : 'May', '6' : 'June', '7' : 'July'}
    
        # extract months from the Start Time column to create a month column
        df['month'] = df['Start Time'].dt.month
               
        # find the most common month
        popular_month = str(df['month'].mode()[0])
        print('Most common month was {}.'.format(month_names[popular_month]))                
    else:
        print('You select just one month. The most common month statistic does not make sense in this case.')
    
    # II. display the most common day of week
    
    if day == 'all':
        # create a dictionary with day names for displaying full name instead of numbers
        day_names = {'0' : 'Monday', '1' : 'Tuesday', '2' : 'Wednesday', '3' : 'Thursday', '4' : 'Friday', '5' : 'Saturday', '6' : 'Sunday'}

        # extract days from the Start Time column to create an day column
        df['day'] = df['Start Time'].dt.dayofweek     
        
        # find the most common day
        popular_dayofweek = str(df['day'].mode()[0])
        print('In month: {} most common day of the week was {}.'.format(month.title(), day_names[popular_dayofweek]))
        
    else:
        print('You select just one day. The most common day statistic does not make sense in this case.')
        
    # III. display the most common start hour
    
    # extract hours from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
        
    # find the most popular hour
    popular_hour = str(df['hour'].mode()[0])
    print('In month: {} and day: {} the most common hour was {}'.format(month.title(), day.title(), popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city):
    """
    Displays statistics on the most popular stations and trip

    Args:
        popular_station - name of the popular start station
        popular_station_count - count of the popular start station
        popular_end_station - name of the popular end station
        popular_end_station_count - count of the popular end station
        popular_route - name of the popular route
        popular_route_count - count of the popular route
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # I. display most commonly used start station
    popular_station = df['Start Station'].mode()[0]
    popular_station_count = df['Start Station'].value_counts()[0]
    print('Most commonly used start station in {} was {}. It was used {} times.'.format(city.title(), popular_station, popular_station_count))

    # II. display most commonly used end station
    popular_end_station = str(df['End Station'].mode()[0])
    popular_end_station_count = df['End Station'].value_counts()[0]
    print('Most commonly used end station in {} was {}. It was used {} times.'.format(city.title(), popular_end_station, popular_end_station_count))

    # III. display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + ' - ' + df['End Station']
    popular_route = df['Route'].mode()[0]
    popular_route_count = df['Route'].value_counts()[0]
    print('Most popular route in {} was {}. It was used {} times. '.format(city.title(), popular_route, popular_route_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # I. display total travel time
    df['Travel Time'] = df['End Time'] - df['Start Time']
    total_travel_time = df['Travel Time'].sum()
    print('The total trevel time was: ', total_travel_time)

    # display mean travel time    
    avg_travel_time = df['Travel Time'].mean()
    print('The meant trevel time was: ', avg_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # I. Display counts of user types
    user_types = df['User Type'].value_counts()
    print('What is the breakdown of users for {}?\n{}'. format(city.title(), user_types))
    
    if city == 'chicago' or city == 'new york city':
    
        # II. Display counts of gender
        gender_types = df['Gender'].value_counts()
        print('\nWhat is the breakdown of gender for {}?\n{}'. format(city.title(), gender_types))
        
        # III. Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        print('\nThe earliest year of birth in {} is {}.'.format(city.title(), earliest_birth_year))
        
        recent_birth_year = int(df['Birth Year'].max())
        print('\nThe most recent year of birth in {} is {}.'.format(city.title(), recent_birth_year))
        
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('\nMost common year of birth in {} is {}.'. format(city.title(), most_common_birth_year )) 

    else:
        print('\nGender and year of birth statistics are not available for Washington.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_output(city):    
    """
    Displays raw data for bikeshare data in the selected city.

    Args:
        (int) i - row 'index' in the data frame
        (int) row_count - total row number in the data frame df minus 1
        (str) see_data - raw user input for data output. takes values 'yes' or 'no'
    """
    
    print('\nDispaying raw data...\n')
    start_time = time.time()
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    i = 0
    #print('i: ', i)
    row_count = (len(df.index)-1)
    #print('row_count ', row_count)

    while i <= row_count:
        
        see_data = input('Do you wand to see raw data? Enter yes or no:\n').lower().strip()
    
        if see_data == 'yes':
            
            if i < row_count:
                i_2 = i + 4
                #print('i_2 = ', i_2)
            else:
                i_2 = row_count  
                #print('i_2 = row_count', i_2)
            
            #print('i = ', i)   
            print(df.loc[i:i_2])
            i += 5
            #print('i = ', i)
                   
        elif see_data == 'no': 
            print('Ok. You do not want see any data.')
            break
        else:
            print('It seems like a typo. Please try it again')
    else:
        print('You saw all raw data.')    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def main():
    while True:
        city, month, day = get_filters()
        
        if city == 'na' and month =='na' and day == 'na':
            restart = input('\nWould you like to restart? Enter yes or no.\n').strip()
            if restart.lower() != 'yes':
                break
        else:       
            df = load_data(city, month, day)
             
            time_stats(df, month, day)
            station_stats(df, city)
            trip_duration_stats(df)
            user_stats(df, city)
            
            # raw data output
            raw_data_output(city)    
            
            restart = input('\nWould you like to restart? Enter yes or no.\n').strip()
            if restart.lower() != 'yes':
                break

if __name__ == "__main__":
	main()
