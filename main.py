import time
from airfare_scraping import vary_dates
from communicate import email_lowest_fare, email_with_att, sms_lowest_fare
from config import params
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


def main():

    while True:
        df = search_gather_save()
        communicate_prices(df)
       # plot(df)
        del df
        print('going to sleep')
        time.sleep(1*60*60)

if __name__ == "__main__":
    main()

# TODO:
# 1) fix the different length lists
# 2) write purchase ticket function if price below threshold