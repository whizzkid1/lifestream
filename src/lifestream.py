import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.pyplot import figure
from datetime import datetime
import matplotlib.ticker as mtick

def create_transaction_log(
    df, 
    orderid_col, 
    datetime_col,
    customerid_col, 
    quantity_col, 
    unitprice_col, 
):
    """
    Creates a transaction log that can be used in subsequent methods.

    The sample dataset from UC Irvine doesn't total up the value of 
    a single order/transaction. This method is to prep that transaction log.

    It accepts transaction data, and returns a DataFrame of a standard transaction
    log.

    Future state shall deal with other kinds of anomalies/cases.
    
    Parameters
    ----------
    df: :obj: DataFrame
        a Pandas DataFrame that contains your transactional data.
    orderid_col: string
        the column in df DataFrame that denotes the unique order_id.
    datetime_col:  string
        the column in df DataFrame that denotes the datetime the purchase was made.
    customerid_col: string
        the column in df DataFrame that denotes the unique customer_id.
    quantity_col: string
        the column in df DataFrame that denotes the quantity of items purchased in an order.
    unitprice_col: string
        the column in df DataFrame that denotes the unit price of items purchased in an order.
    Returns
    -------
    :obj: DataFrame
        A DataFrame with an order_id column, date column, customer_id column and a 'OrderValue' column, 
        which represents the total price of one transaction.
    """
    
    df['OrderValue'] = df[quantity_col] * df[unitprice_col]
    grouped = df.groupby([orderid_col, datetime_col, customerid_col])
    transaction_log = grouped.agg({
    'OrderValue': np.sum
    })
    transaction_log.reset_index(inplace = True)
    transaction_log[datetime_col] = transaction_log[datetime_col].astype('datetime64[ns]') 
    return transaction_log

def sales_chart(
    transaction_log, 
    datetime_col, 
    ordervalue_col, 
    customerid_col,
    title = 'Sales Over Time',
    ylabel = 'Sales ($)'
):
    """
    Creates a bar chart of monthly revenue. 
    
    Parameters
    ----------
    transaction_log: :obj: DataFrame
        a Pandas DataFrame that contains your transaction log.
    datetime_col: string
        the column in transaction_log DataFrame that denotes the datetime of an order.
    ordervalue_col: string
        the column in transaction_log DataFrame that contains the total value of an order.
    customerid_col: string
        the column in transaction_log DataFrame that contains the unique customer_id.
    title: string, optional
        the plot's title.
    ylabel: string, optional
        the label for the y-axis of the plot.
    -------
    axes: matplotlib.AxesSubplot
    """

    # Get time format correct of date column correct
    transaction_log[datetime_col] = pd.to_datetime(transaction_log[datetime_col])
    transaction_log = transaction_log.set_index(datetime_col)
    
    # Aggregate data on a monthly basis from transaction log. User user_id totals to create optional stacked 
    # chart in the futre
    df = transaction_log.groupby(pd.Grouper(freq="M"))[ordervalue_col, customerid_col].agg({ordervalue_col: 'sum', 
    customerid_col: 'count'})
    
    # Plot
    ax = plt.subplot()
    plt.gcf().autofmt_xdate()
    height = df[ordervalue_col]
    bars = df.index
    bars = bars.strftime("%b-%Y")
    y_pos = np.arange(len(bars))
    fmt = '${x:,.0f}'
    tick = mtick.StrMethodFormatter(fmt)
    ax.yaxis.set_major_formatter(tick)
    ax.set_xlabel('Month')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.xticks(y_pos, bars)
    plt.bar(y_pos, height)
    every_nth = 3 
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    
def cohort_retention_chart(
    transaction_log, 
    datetime_col,  
    ordervalue_col,
    customerid_col, 
    cohort1, 
    cohort2, 
    cohort3,
    title = 'Cohorts: User Retention',
    ylabel = "Percent of Cohort Purchasing"
):
    """
    Creates a bar chart of monthly revenue. 
    
    Parameters
    ----------
    transaction_log: :obj: DataFrame
        a Pandas DataFrame that contains your transaction log.
    datetime_col: string
        the column in transaction_log DataFrame that denotes the datetime of an order.
    ordervalue_col: string
        the column in transaction_log DataFrame that contains the total value of an order.
    customerid_col: string
        the column in transaction_log DataFrame that contains the unique customer_id.
    cohort1: string
        the cohort in 'YYYY-MM' format whose monthly retention you want plotted.
    cohort2: string
        the cohort in 'YYYY-MM' format whose monthly retention you want plotted.
    cohort3: string
        the cohort in 'YYYY-MM' format whose montly retention you want plotted.
    title: string, optional
        the title of the plot.
    ylabel: string, optional
        the label for the y-axis of the plot.
    -------
    axes: matplotlib.AxesSubplot
    """
     # Define a monthly order period
    transaction_log['OrderPeriod'] = transaction_log[datetime_col].apply(lambda x: x.strftime('%Y-%m'))
    transaction_log.set_index(customerid_col, inplace=True)
    
    # Define the cohort group of a user
    transaction_log['CohortGroup'] = transaction_log.groupby(level=0)[datetime_col].min().apply(lambda x: x.strftime('%Y-%m'))
    transaction_log.reset_index(inplace=True)
    
    # Aggregate data based on cohort and monthly order period
    grouped = transaction_log.groupby(['CohortGroup', 'OrderPeriod'])
    cohorts = grouped.agg({customerid_col: pd.Series.nunique,
                       ordervalue_col: np.sum})
    cohorts.rename(columns={customerid_col: 'TotalUsers'
                        }, inplace=True)

    # Create a cohort period column, which reflects number of months on site. Month of first purchase = 1
    def cohort_period(df):
        df['CohortPeriod'] = np.arange(len(df)) + 1
        return df
    cohorts = cohorts.groupby(level=0).apply(cohort_period)

    # reindex the DataFrame
    cohorts.reset_index(inplace=True)
    cohorts.set_index(['CohortGroup', 'CohortPeriod'], inplace=True)

    # create a Series holding the total size of each CohortGroup
    cohort_group_size = cohorts['TotalUsers'].groupby(level=0).first()

    #User Retention Matrix
    user_retention = cohorts['TotalUsers'].unstack(0).divide(cohort_group_size, axis=1)

    #Plot it
    user_retention[[cohort1, cohort2, cohort3]].plot(figsize=(10,5))
    plt.title(title)
    plt.xticks(np.arange(1, 12.1, 1))
    plt.xlim(1, 12)
    plt.ylabel(ylabel)

def new_customers_chart(
    transaction_log, 
    datetime_col, 
    customerid_col,
    title = 'New Buyers by Month',
    xlabel = 'Month of First Purchase',
    ylabel = 'Number of New Buyers',
    kind = 'bar'
):
    """
    Creates a bar chart of new buyers by month. 
    
    Parameters
    ----------
    transaction_log: :obj: DataFrame
        a Pandas DataFrame that contains your transaction log.
    datetime_col: string
        the column in transaction_log DataFrame that denotes the datetime of an order.
    customerid_col: string
        the column in transaction_log DataFrame that contains the unique customer_id.
    title: string, optional
        the title of the plot.
    xlabel: string, optional
        the label for the x-axis of the plot.
    ylabel: string, optional
        the label for the y-axis of the plot.
    kind: string, optional
        the kind of plot desired. see the .plot method for pandas library for what's supported.
    -------
    axes: matplotlib.AxesSubplot
    """

    transaction_log['OrderPeriod'] = transaction_log[datetime_col].apply(lambda x: x.strftime('%Y-%m'))
    transaction_log.set_index(customerid_col, inplace = True)
    transaction_log['CohortGroup'] = transaction_log.groupby(level=0)[datetime_col].min().apply(lambda x: x.strftime('%Y-%m'))
    transaction_log.reset_index(inplace = True)
    grouped = transaction_log.groupby(['CohortGroup'])
    cohorts = grouped.agg({customerid_col: pd.Series.nunique,
                       })
    cohorts.rename(columns={customerid_col: 'TotalUsers'}, inplace=True)
    def cohort_period(df):
        df['CohortPeriod'] = np.arange(len(df)) + 1
        return df
    cohorts = cohorts.groupby(level=0).apply(cohort_period)
    cohorts.reset_index(inplace=True)
    cohorts.set_index(['CohortGroup', 'CohortPeriod'], inplace=True)
    cohort_group_size = cohorts['TotalUsers'].groupby(level=0).first()
    cohort_group_size.plot(kind = kind, figsize=(10,5))
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

