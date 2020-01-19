import matplotlib.pyplot as plt
import datetime
import pandas as pd
from IPython import get_ipython
from config import inputs, my_provider, my_number, params
from communicate import sms_msg

def df_by_dep_date(df):

    df_by_dep_date = pd.DataFrame()

    dates = df.dep_date.unique()
    mean, max_, min_, med = 0, 0, 0, 0
    now = datetime.datetime.now()
    temp = dict()

    for d in dates:
        mean = df.loc[df.dep_date == d]["prices"].mean()
        max_ = df.loc[df.dep_date == d]["prices"].max()
        min_ = df.loc[df.dep_date == d]["prices"].min()
        med =  df.loc[df.dep_date == d]["prices"].median()

        temp = {'table_creation_date': [now],
                'dep_date': [d],
                'max_price': [max_],
                'mean_price': [mean],
                'median_price': [med],
                'min_price': [min_]}

        df_by_dep_date = pd.concat([df_by_dep_date, pd.DataFrame(temp)], ignore_index=True)
        temp = dict()

    return df_by_dep_date


def graph_df_by_dep_date_data(df):
    '''
    plots the max, avg, min prices and saves graph as pdf
    df comes from df_by_dep_date function
    returns the file_name of the graph (with path)
    '''

    try:
        # get_ipython().run_line_magic('matplotlib', 'inline')
        # get_ipython().run_line_magic('matplotlib', 'qt')

        plt.plot(df['dep_date'], df['mean_price'], color='r')
        plt.plot(df['dep_date'], df['max_price'], color='b')
        plt.plot(df['dep_date'], df['min_price'], color='b')
        plt.xlabel('departure date')
        plt.ylabel('price, $')
        plt.title(inputs['dep'] + ' --> ' + inputs['arr'] + ' | ' + inputs['fare_type'] + ' | ' + str(datetime.date.today()))



        file_name = 'graph_'

        for i in inputs.keys():
            file_name = file_name + str(inputs[i]) + '_'

        file_name = file_name.replace('/', '_')
        file_name = './graphs/' + file_name + '.pdf'

        plt.savefig(file_name)

        plt.show()

        return file_name

    except Exception as e:
        msg = 'an error occurred while plotting data\n' + str(e)
        print(msg)
        sms_msg(msg, my_number, my_provider)


def detect_price_drop(df):

    last_run = df['info_date'].max()
    last_min = df[df.info_date == last_run]['prices'].min()

    # delete rows from last run
    index_last_run = df[df['info_date'] == last_run].index
    df.drop(index_last_run, inplace=True)

    min_ = df['prices'].min()
    dates_of_min = df[df.prices==last_min]['dep_date'].unique()
    airline = str(df[df.prices == last_min]['airlines'].unique())

    if last_min  < min_ * params['price_drop_threshold']:
        print('detected price drop; attempt to notify via sms')
        msg = 'PRICE DROP! ' + inputs['dep'] + '->' + inputs['arr'] + '\ndep ' + str(
            dates_of_min) + '; $' + str(last_min) + '; '+airline
        sms_msg(msg, params['sms_recipient'], params['sms_provider'])

