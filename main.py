import time
from airfare_scraping import vary_dates
import threading
from communicate import email_lowest_fare, email_with_att, sms_lowest_fare
from pickleling import pickle_data, unpickle_data
from config import params
from analysis import detect_price_drop, df_by_dep_date, graph_df_by_dep_date_data

def thread_search_gather_save():
    ''' This is the only thread that saves DataFrame files.  Purpose is to continuously search for flight prices
    gather prices and save them in folder "data"
    '''

    print('starting search thread')
    count = 0
    while True:
        start= time.time()
        df = vary_dates()
        end = time.time()
        pickle_data(df)
        print(str(count) + ' date_vary in ' + str(round((end - start) / 60., 2)))
        print('averaging ' + str(
            round((params['length period'] * params['freq']) / ((end - start) / 60.), 2)) + ' min / date')
        time.sleep(2*60*60)
        count+=1

def thread_communicate_prices(file_name):

    print('starting communicate thread')
    while True:
        df = unpickle_data(file_name)
        email_lowest_fare(df, params['email_recipient'])
        sms_lowest_fare(df, params['sms_recipient'], params['sms_provider'])
        detect_price_drop(df)
        # communicate prices every 3 hours
        time.sleep(3*60*60)


def thread_plot(file_name):

    print('starting plotting thread')
    while True:
        df = unpickle_data(file_name)
        df_analysis = df_by_dep_date(df)
        graph_file = graph_df_by_dep_date_data(df_analysis)
        email_with_att(graph_file)
        # plot every 12 hours
        time.sleep(12*60*60)


def main():

    df = vary_dates()
    file_name = pickle_data(df)

    t1 = threading.Thread(target=thread_search_gather_save)
    t2 = threading.Thread(target=thread_communicate_prices, args=(file_name,))
    t3 = threading.Thread(target=thread_plot, args=(file_name,))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    print('diego')


if __name__ == "__main__":
    main()

# TODO:
# 1) fix the different length lists
# 2) update detect_price_drop to compare last_min to min_now
# 3) delete old data... add thread to run 1x / day