import pandas as pd

filepath = '/Users/brookeknowles/Downloads/netflix-report'

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
    import matplotlib.pyplot as plt                                         # Import Library

    plt.plot(df["Gross Sale Amt"], marker='o')      # Plot

    # Labelling plot
    plt.xlabel("Date")
    plt.ylabel("Cost for a month of Netflix")
    plt.title("Netflix cost over time")

    plt.show()                                      # Display

    return "{:.2f}".format(money_paid)              # Convert to 2dp like actual money
