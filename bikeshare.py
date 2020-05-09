import time
import pandas as pd
import calendar

CITY_DATA = { 'chicago': './data/chicago.csv',
              'new york city': './data/new_york_city.csv',
              'washington': './data/washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Which city are you interested in?\n').lower().strip()
            if city in CITY_DATA:
                break
            else:
                print('We haven\'t any data available for this city. Please choose between: {}\n'.format(', '.join(CITY_DATA).title()))
        except KeyboardInterrupt:
            print('This is no valid input. Please choose between the following cities: {}\n'.format(', '.join(CITY_DATA).title()))


    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Which month are you interested in?\n').strip().title()
            if month in calendar.month_name[1:7]:
                month = list(calendar.month_name).index(month)
                break
            elif month in calendar.month_abbr[1:7]:
                month = list(calendar.month_abbr).index(month)
                break
            elif month == 'All':
                break
            else:
                print('We haven\'t any data available for this month. Please enter \'all\' or choose between: {}\n'.format(', '.join(calendar.month_name[1:7])))
        except KeyboardInterrupt:
            print('This is no valid input. Please enter \'all\' or choose between the following months: {}\n'.format(', '.join(calendar.month_name[1:7])))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Which weekday are you interested in?\n').strip().title()
            if day in calendar.day_name:
                day = list(calendar.day_name).index(day)
                break
            elif day in calendar.day_abbr:
                day = list(calendar.day_abbr).index(day)
                break
            elif day == 'All':
                break
            else:
                print('We haven\'t any data available for this weekday. Please enter \'all\' or choose between: {}\n'.format(', '.join(calendar.day_name)))
        except KeyboardInterrupt:
            print('This is no valid input. Please enter \'all\' or choose between the following weekdays: {}\n'.format(', '.join(calendar.day_name)))

    print('-'*40)
    return city, month, day


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

    df = pd.read_csv(CITY_DATA[city])
    df.columns = [c.replace(' ', '_') for c in df.columns]
    df.Start_Time = pd.to_datetime(df.Start_Time)
    df.End_Time = pd.to_datetime(df.End_Time)

    if month != 'All':
        df = df[df.Start_Time.dt.month == month]

    if day != 'All':
        df = df[df.Start_Time.dt.weekday == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if len(df['Start_Time'].dt.strftime('%B').unique()) > 1:
        print('The most common month: {}'.format(df['Start_Time'].dt.strftime('%B').value_counts().idxmax()))

    # display the most common day of week
    if len(df['Start_Time'].dt.strftime('%A').unique()) > 1:
        print('The most common day of week: {}'.format(df['Start_Time'].dt.strftime('%A').value_counts().idxmax()))

    # display the most common start hour
    print('The most common start hour: {}'.format(df['Start_Time'].dt.strftime('%H').value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station: {}'.format(df['Start_Station'].value_counts().idxmax()))

    # display most commonly used end station
    print('The most commonly used end station: {}'.format(df['End_Station'].value_counts().idxmax()))

    # display most frequent combination of start station and end station trip
    most_frequent_route = df.groupby(['Start_Station', 'End_Station']).size().idxmax()
    print('The most frequent combination of start station and end station trip: \'{}\' to \'{}\''.format(most_frequent_route[0], most_frequent_route[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: {}'.format(pd.Timedelta(df['Trip_Duration'].sum(), unit='s')))

    # display mean travel time
    td = pd.Timedelta(df['Trip_Duration'].mean(), unit='s').components
    print('Mean travel time: {}{} minutes and {} seconds'.format(td[1] + ' hours, ' if td[1] > 0 else '', td[2], td[3]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Number of Rentals per User Type:\n{}\n'.format(df['User_Type'].value_counts().to_string()))

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Number of Rentals per Gender:\n{}\n'.format(df['Gender'].value_counts().to_string()))

    # Display earliest, most recent, and most common year of birth
    if 'Birth_Year' in df.columns:
        print('Oldest year of birth: {}'.format(int(df['Birth_Year'].min())))
        print('Youngest year of birth: {}'.format(int(df['Birth_Year'].max())))
        print('Most common year of birth: {}'.format(int(df['Birth_Year'].value_counts().idxmax())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df):
    """Shows lines of raw data if requested."""
    pd.set_option('display.max_columns', None)

    try:
        raw_data_requested = input('\nDo you want to see 5 lines of raw data?\n').lower().strip()

        while True:
            if raw_data_requested == 'yes':
                print(df.sample(5))
                raw_data_requested = input('\nDo you want to see another 5 lines of raw data?\n').lower().strip()
            elif raw_data_requested == 'no':
                break
            else:
                raw_data_requested = input('Sorry, just say \'yes\' or \'no\' please.\n').lower().strip()

    except KeyboardInterrupt:
        print('This is no valid input. Just say \'yes\' or \'no\' please.\n')

def restart_request():
    try:
        restart = input('\nWould you like to restart?\n').lower().strip()
        while True:
            if (restart == 'yes') or (restart == 'no'):
                break
            else:
                restart = input('Sorry, just say \'yes\' or \'no\' please.\n').lower().strip()
    except KeyboardInterrupt:
        print('Sorry, this is no valid input. Just say \'yes\' or \'no\' please.\n')

    if restart == 'yes':
        return True
    else:
        return False

def main():
    run = True

    while run:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        run = restart_request()

if __name__ == "__main__":
	main()
