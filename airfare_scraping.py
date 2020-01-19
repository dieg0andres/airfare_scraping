import itertools
import datetime
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from config import inputs, params, my_number, my_provider
from communicate import sms_msg


def setup_webdriver():
    driver = -1
    try:
        driver = webdriver.Firefox(executable_path = './geckodriver')
        driver.set_window_position(-15000, 15000)
        driver.set_page_load_timeout(60)

    except Exception as e:
        msg = 'an error occurred while setting up webdriver\n' + str(e)
        print(msg)
        sms_msg(msg, my_number, my_provider)

    finally:
        return driver

def initial_search(driver):
    """
    conducts search based on inputs
    returns a selenium webdriver object
    """
    try:
        driver.get("http://expedia.com")
        time.sleep(6)
        driver.find_element_by_xpath("//button[@id='tab-flight-tab-hp']").click()
        time.sleep(1)
        if inputs['flight_type'] == 'one way':
            driver.find_element_by_xpath("//label[@id='flight-type-one-way-label-hp-flight']").click()
            time.sleep(1)
            driver.find_element_by_xpath("//input[@id='flight-departing-single-hp-flight']").send_keys(
                inputs['dep_date'])
        else:
            driver.find_element_by_xpath("//label[@id='flight-type-roundtrip-label-hp-flight']").click()
            time.sleep(1)
            driver.find_element_by_xpath("//input[@id='flight-departing-hp-flight']").send_keys(inputs['dep_date'])
            time.sleep(1)
            for i in range(12):
                driver.find_element_by_xpath("//input[@id='flight-returning-hp-flight']").send_keys(Keys.BACKSPACE)
            driver.find_element_by_xpath("//input[@id='flight-returning-hp-flight']").send_keys(inputs['return_date'])
        time.sleep(1)
        driver.find_element_by_xpath("//input[@id='flight-origin-hp-flight']").send_keys(inputs['dep'])
        time.sleep(1)
        driver.find_element_by_xpath("//input[@id='flight-destination-hp-flight']").send_keys(inputs['arr'])
        time.sleep(1)
        driver.find_element_by_xpath("//a[@id='flight-advanced-options-hp-flight']").click()
        time.sleep(1)
        Select(driver.find_element_by_xpath(
            "//select[@id='flight-advanced-preferred-class-hp-flight']")).select_by_visible_text(inputs['fare_type'])
        time.sleep(1)
        driver.find_element_by_xpath("//button[@class='btn-primary btn-action gcw-submit']").send_keys(Keys.ENTER)
        time.sleep(20)

    except Exception as e:
        msg = 'an error ocurred while conducting search\n' + str(e)
        print(msg)
        sms_msg(msg, my_number, my_provider)


def update_search(driver, dep_date, ret_date):

    temp1 = inputs['dep_date']
    temp2 = inputs['return_date']

    inputs['dep_date'] = dep_date
    inputs['return_date'] = ret_date

    initial_search(driver)

    inputs['dep_date'] = temp1
    inputs['return_date'] = temp2


def gather_initial_data(driver):
    '''
    driver: selenium webdriver pointing to the website with search results.  Should come from function setup_webdriver
    returns a Pandas df with flight price, duration, time, airline, etc.

    '''
    # INFO: Get the data from the browser

    try:
        airlines = driver.find_elements_by_xpath("//span[@data-test-id='airline-name']")
        airlines_list = [str(value.text) for value in airlines]
        del airlines

        prices = driver.find_elements_by_xpath("//span[@data-test-id='listing-price-dollars']")
        prices_list = [value.text for value in prices]
        del prices

        durations = driver.find_elements_by_xpath("//span[@data-test-id='duration']")
        durations_list = [value.text for value in durations]
        del durations

        stops = driver.find_elements_by_xpath("//span[@class='number-stops']")
        stops_list = [str(value.text) for value in stops]
        del stops

        dep_times = driver.find_elements_by_xpath("//span[@data-test-id='departure-time']")
        dep_times_list = [str(value.text) for value in dep_times]
        del dep_times

        arr_times = driver.find_elements_by_xpath("//span[@data-test-id='arrival-time']")
        arr_times_list = [str(value.text) for value in arr_times]
        del arr_times

        time.sleep(2)

    except Exception as e:
        msg = 'an error ocurred while gathering data\n' + str(e)
        print(msg)
        sms_msg(msg, my_number, my_provider)

    # INFO: edit data to get desired format

    # edit prices_list to convert to integer
    prices = []
    for price in prices_list:
        price = list(price)
        price.pop(price.index('$'))
        if ',' in price: price.pop(price.index(','))
        price = int(''.join(price))
        prices.append(price)
    prices_list = prices
    del prices

    # edit durations to get a float in hours
    durations = []
    for duration in durations_list:
        duration = duration.split(' ')
        hours = int(duration[0].replace('h', ''))
        minutes = int(duration[1].replace('m', ''))
        duration = hours + minutes / 60.
        durations.append(round(duration, 2))
    durations_list = durations
    del durations

    # edit layover / stops count
    stops = []
    for stop in stops_list:
        if stop == '(Nonstop)':
            stops.append(0)
        else:
            stops.append(int(stop[1]))
    stops_list = stops
    del stops

    # INFO: save data in pandas dataframe
    list_len = len(prices_list)
    now = datetime.datetime.now()

    # Check length of list as a troubleshooting measure to prevent script crash if lengths are different
    if len(airlines_list) == len(prices_list) and \
        len(prices_list) == len(durations_list) and \
        len(durations_list) == len(stops_list) and \
        len(stops_list) == len(dep_times_list) and \
        len(dep_times_list) == len(arr_times_list):
        pass
    else:
        msg = 'length of lists gathered are not all equal:'
        print(msg)
        print('airlines', len(airlines_list), 'prices', len(prices_list), 'durations', len(durations_list), 'stops',
              len(stops_list), 'dep_times', len(dep_times_list), 'arr_times', len(arr_times_list))
        sms_msg(msg, my_number, my_provider)
        return pd.DataFrame()

    data = {'airlines': airlines_list,
            'prices': prices_list,
            'durations': durations_list,
            'stops': stops_list,
            'dep_times': dep_times_list,
            'arr_times': arr_times_list,
            'dep' : itertools.repeat(inputs['dep'], list_len),
            'arr': itertools.repeat(inputs['arr'], list_len),
            'flight_type': itertools.repeat(inputs['flight_type'], list_len),
            'fare_type': itertools.repeat(inputs['fare_type'], list_len),
            'dep_date': itertools.repeat(inputs['dep_date'], list_len),
            'return_date': itertools.repeat(inputs['return_date'], list_len),
            'info_date' : itertools.repeat(now, list_len)
            }

    df = pd.DataFrame(data)
    return df

def gather_updated_data(driver, dep_date, ret_date):

    temp1 = inputs['dep_date']
    temp2 = inputs['return_date']

    inputs['dep_date'] = dep_date
    inputs['return_date'] = ret_date

    df = gather_initial_data(driver)

    inputs['dep_date'] = temp1
    inputs['return_date'] = temp2

    return df

def vary_dates():
    '''
    :return: a DataFrame with flight data for the range of dates from departure date and return_date plus 'length period' at a frequency 'freq'
    '''

    def generate_date_list(date_type): # date type can only be: 'dep_date' or 'return_date'
        '''
        returns: a list of string dates based on the inputs
        '''

        date_str = inputs[date_type].split('/')
        dates = []#inputs[date_type]]

        for i in range(0, params['length period'], params['freq']):

            month = int(date_str[0])
            day = int(date_str[1])
            year = int(date_str[2])

            date = datetime.datetime(year, month, day)
            date = date + datetime.timedelta(days=params['freq'])

            if date.month < 10:
                month = '0' + str(date.month)
            else:
                month = str(date.month)

            if date.day < 10:
                day = '0' + str(date.day)
            else:
                day = str(date.day)

            date_str = month + '/' + day + '/' + str(date.year)
            dates.append(date_str)
            date_str = date_str.split('/')

        return dates

    # Generate data first

    df = pd.DataFrame()
    dep_dates_list = generate_date_list('dep_date')
    ret_dates_list = list(dep_dates_list)

    if inputs['flight_type'] == 'roundtrip':
        ret_dates_list = generate_date_list('return_date')

    driver = setup_webdriver()
    initial_search(driver)
    df = pd.concat([df, gather_initial_data(driver)], ignore_index=True)
    driver.close()

    for d_d, r_d in list(zip(dep_dates_list, ret_dates_list)):
        print(inputs['arr']+': on '+str(dep_dates_list.index(d_d)+1)+' scrape out of '+str(len(dep_dates_list)))
        driver = setup_webdriver()
        update_search(driver, d_d, r_d)
        df = pd.concat([df, gather_updated_data(driver, d_d, r_d)], ignore_index=True)
        driver.close()

    return df
