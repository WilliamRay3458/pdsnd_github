import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTH_DATA = {'january': 1,
              'february': 2,
              'march': 3,
              'april': 4,
              'may': 5,
              'june': 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')

    city = input('Please choose which city (Chicago, New York City, or Washington) you would like data on.\n').lower()
    while city not in CITY_DATA:
        print("\nI'm sorry that is not a valid city. Please enter a valid city name you would like data on.\n")
        city = input('Please choose Chicago, New York City, or Washington.\n').lower()

    month = input(
        'Please enter a month January through June or "all" for all months of data.\n').lower()
    while month not in MONTH_DATA.keys() and month != 'all':
        print("I'm sorry that is not a valid month selection")
        month = input('Please enter a valid month selection.\n').lower()

    dotw = input('Please enter the day of the week you would like to see data on. Enter "all" for every day.\n').lower()
    while dotw != 'all' and dotw not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        print("I'm sorry that is not a valid day.\n")
        dotw = input('Please enter a day of the week or enter "all" for the data you would like to see.\n').lower()

    print('-' * 40)
    return city, month, dotw


def load_data(city, month, dotw):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    if city == 'chicago':
        df = pd.read_csv('chicago.csv')
    elif city == 'new york city':
        df = pd.read_csv('new_york_city.csv')
    else:
        df = pd.read_csv('washington.csv')

    if month != 'all':
        month = MONTH_DATA[month]
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['month'] = df['Start Time'].dt.month
        df = df[df['month'] == month]

    if dotw != 'all':
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['dotw'] = df['Start Time'].dt.day_name()
        df = df[df['dotw'] == dotw.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    most_popular_month = df['month'].mode()[0]
    print('\nThe most popular month is:\n\n', most_popular_month)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['dotw'] = df['Start Time'].dt.day_name()
    most_popular_day = df['dotw'].mode()[0]
    print('\nThe most popular day of the week is:\n\n', most_popular_day)

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    most_popular_hour = df['hour'].mode()[0]
    print('\nThe most popular hour (in 24hr time) is:\n\n', most_popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trips...\n')
    start_time = time.time()

    print('\nThe most popular starting stations are:\n\n', df['Start Station'].value_counts().nlargest(1).index[0])
    # See readme.txt.

    print('\nThe most popular ending stations are:\n\n', df['End Station'].value_counts().nlargest(1).index[0])

    most_frequent_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    # See readme.txt.

    print('\nThe most frequent trip taken is:\n', most_frequent_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print('\nThe total number of hours travelled during this time period is:\n\n', df['Trip Duration'].sum() / 60 / 60)

    print('\nThe average number of minutes spent traveling is:\n\n', df['Trip Duration'].mean() / 60)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type = df['User Type'].value_counts()
    print('\nThe type and number of users are:\n\n', user_type)

    if city == 'chicago' or city == 'new york city':
        user_gender = df['Gender'].value_counts()
        print('\nThe user gender and number of each gender is:\n\n', user_gender)
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].value_counts().nlargest(1).index[0]
        print(
            f'\nThe customer with the earliest birth year is {earliest}....WOW!\n\nThe most recent year of birth is {most_recent}.\n\nThe most common birth year is {most_common}.\n')
    else:
        print('\nSorry, there is no gender or birth year data for Washington users.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    """Displays raw data upon user request"""
    start_loc = 0
    end_loc = 5
    view_data = input('\nWould you like to view 5 rows of trip data? Enter "yes" or "no".\n').lower()
    if view_data == 'yes':
        while start_loc < len(df):
            print('\n5 rows of the requested data:\n', df.iloc[start_loc: start_loc + end_loc])
            start_loc += 5
            more_data = input('\nDo you wish to view the next 5 rows? Enter "yes" or "no"\n').lower()
            if more_data != 'yes':
                break


def main():
    while True:
        city, month, dotw = get_filters()
        df = load_data(city, month, dotw)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter "yes" if you wish to continue.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()


