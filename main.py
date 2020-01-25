import time
import pickle
import datetime
from airfare_scraping import vary_dates
from communicate import email_lowest_fare, email_with_att, sms_lowest_fare
from config import params, inputs
from analysis import df_by_dep_date, graph_df_by_dep_date_data

def search_gather_save():

    print('starting search')
    start= time.time()
    df = vary_dates()
    end = time.time()
    print('date_vary in ' + str(round((end - start) / 60., 2))+' minutes')
    return df

def communicate_prices(df):

    print('start communicate_prices')
    email_lowest_fare(df, params['email_recipient'])
    sms_lowest_fare(df, params['sms_recipient'], params['sms_provider'])

def plot(df):

    print('start plot')
    df_analysis = df_by_dep_date(df)
    graph_file = graph_df_by_dep_date_data(df_analysis)
    email_with_att(graph_file)

def pickle_data(df):
    try:
        file_name = inputs['arr'] + '.pickle'
        file1 = open(file_name, 'wb')
        pickle.dump(df, file1)
        file1.close()
    except Exception as e:
        print('error while pickling df', e)

def main():

    price_communicated = 10**6
    last_communication = datetime.date.today() - datetime.timedelta(days=10)

    while True:

        df = search_gather_save()
        pickle_data(df)

        if df['prices'].min() < price_communicated or last_communication < datetime.date.today():
            communicate_prices(df)
            price_communicated = df['prices'].min()
            last_communication = datetime.date.today()

        del df
        print('going to sleep')
        time.sleep(1*60*60)

if __name__ == "__main__":
    main()

# TODO:
# 2) write purchase ticket function if price below threshold