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


