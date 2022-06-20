import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

filepath = '/Users/brookeknowles/Downloads/netflix-report'

def get_users():
    """ Gets all of the unique users on the Netflix account """
    users = []
    df = pd.read_csv(filepath + '/PROFILES/Profiles.csv')

    for i in df.index:
        users.append(df['Profile Name'][i])

    return users


def convert_string_to_seconds(s):
    """ Helper function for get_viewing_time(). Converts a time in the format 'HH:MM:SS' to seconds float """
    hours, minutes, seconds = [float(x) for x in s.split(':')]
    return (hours * 3600) + (minutes * 60) + seconds


def get_watch_time():
    """ Finds the total watch time for each user """
    df = pd.read_csv(filepath + '/CONTENT_INTERACTION/ViewingActivity.csv')

    users = get_users()
    users_watch_time = []     # store each user's viewing time in same order as they appear in users list

    for user in users:
        current_user = user
        current_user_time = 0
        for i in df.index:
            if current_user != df['Profile Name'][i]:
                current_user_time += convert_string_to_seconds(df['Duration'][i])
        users_watch_time.append(current_user_time)

    plt.pie(users_watch_time, labels=users)         # Plot
    plt.title("Users total watch time")             # Labelling plot
    plt.show()                                      # Display

    return users_watch_time


def convert_date_string_to_weekday(s):
    """ Converts a string in the form YYYY-MM-DD HH:MM:SS to an int representing a weekday.
        0 = Monday, 1 = Tuesday, 2 = Wednesday, 3 = Thursday, 4 = Friday, 5 = Saturday, 6 = Sunday"""
    dt = datetime.fromisoformat(s)
    return dt.weekday()


def get_most_watched_days_of_week():
    """ Finds which days of the week have the most Netflix activity """

    df = pd.read_csv(filepath + '/CONTENT_INTERACTION/ViewingActivity.csv')

    activity = [0, 0, 0, 0, 0, 0, 0]        # list that will be indexed like 0 = monday activity to 6 = sunday activity
    for i in df.index:
        activity_day = convert_date_string_to_weekday(df['Start Time'][i])
        activity[activity_day] += 1         # if there's activity on a day, increment activity for that day

    days = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']

    plt.bar(days, activity, color='red', width=0.4)     # Plot
    plt.xlabel("Day of week")                           # Labelling plot
    plt.ylabel("No. of shows/movies watched")
    plt.title("Netflix activity by day of week")
    plt.show()                                          # Display


def get_money_paid():
    """ Finds the total amount of money paid to Netflix over the years, and makes a time series plot of price
    increases/decreases in that time period """

    df = pd.read_csv(filepath + '/PAYMENT_AND_BILLING/BillingHistory.csv')

    money_paid = 0
    temp = ''
    for i in df.index:
        # for some reason the netflix data has each transaction twice so checks if a date is the same as previous
        if temp != df['Transaction Date'][i]:
            money_paid += df['Gross Sale Amt'][i]
            temp = df['Transaction Date'][i]
        else:   # it is a double up, so drop the row
            temp = df['Transaction Date'][i]
            df = df.drop(index=i)

    df["Transaction Date"] = df["Transaction Date"].astype("datetime64")    # Changing the datatype
    df = df.set_index("Transaction Date")                                   # Setting the Date as index

    plt.plot(df["Gross Sale Amt"], marker='o')      # Plot
    plt.xlabel("Date")                              # Labelling plot
    plt.ylabel("Cost for a month of Netflix")
    plt.title("Netflix cost over time")
    plt.show()                                      # Display

    return "{:.2f}".format(money_paid)              # Convert to 2dp like actual money
