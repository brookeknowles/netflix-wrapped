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
    """ Helper function for get_watch_time(). Converts a time in the format 'HH:MM:SS' to seconds float """
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


def is_tv_show(title):
    """ Returns a boolean true if the title is a TV show, false if it's a movie"""
    if "Episode" in title:
        return True
    return False


def strip_tv_show(title):
    """ Strips the title of a tv show from the format Show : Season (Episode) to just the show.
        e.g. 'Parks and Recreation: Season 1: Pilot (Episode 1)' becomes 'Parks and Recreation' """
    if "Season" in title:
        split_string = title.split(": Season")
    elif "Collection" in title:
        split_string = title.split(": Collection")
    elif "Limited Series" in title:
        split_string = title.split(": Limited Series")
    elif "Series" in title:
        split_string = title.split(": Series")
    else:
        return title
    return split_string[0]


def get_most_common_title():
    """ Finds the 10 most popular TV Shows from their titles.
        Note this could technically include movies/non series too, but would be fairly unlikely as
        you'd have to watch alot of times for it to beat the series' to the top 10"""
    df = pd.read_csv(filepath + '/CONTENT_INTERACTION/ViewingActivity.csv')

    for i in df.index:
        if is_tv_show(df['Title'][i]):
            old_title = df['Title'][i]
            new_title = strip_tv_show(df['Title'][i])
            df['Title'] = df['Title'].replace([old_title], new_title)
        if df['Title'][i] == "NullCompleteVideo":
            df = df.drop(index=i)

    n = 10                                                                      # number of titles to include on graph
    most_common_titles = df['Title'].value_counts().index.tolist()[:n]
    most_common_values = df['Title'].value_counts().values.tolist()[:n]

    plt.figure(figsize=(15, 5))
    plt.bar(most_common_titles, most_common_values, color='red', width=0.4)     # Plot
    plt.xlabel("Series")                                                        # Labelling plot
    plt.ylabel("No. of times watched")
    plt.title("Most popular TV series")
    plt.tight_layout()                                                          # adjust figure area so labels fit nice
    plt.show()                                                                  # Display


def get_most_common_movies():
    """ Finds the most popular movies/non series from their titles

    TODO: fix plots so that long movie titles dont get all jumbled up
    """
    df = pd.read_csv(filepath + '/CONTENT_INTERACTION/ViewingActivity.csv')

    for i in df.index:
        if is_tv_show(df['Title'][i]) or df['Title'][i] == "NullCompleteVideo":
            df = df.drop(index=i)

    n = 10                                                                      # number of titles to include on graph
    most_common_titles = df['Title'].value_counts().index.tolist()[:n]
    most_common_values = df['Title'].value_counts().values.tolist()[:n]

    plt.figure(figsize=(15, 5))
    plt.bar(most_common_titles, most_common_values, color='red', width=0.4)     # Plot
    plt.xlabel("Movie")                                                         # Labelling plot
    plt.ylabel("No. of times watched")
    plt.title("Most popular movies")
    plt.locator_params(axis="y", integer=True, tight=True)                      # Force Y Axis to be integer values only
    plt.tight_layout()                                                          # adjust figure area so labels fit nice
    plt.show()                                                                  # Display
