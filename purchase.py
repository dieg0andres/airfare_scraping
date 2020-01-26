import time
import sys
from selenium.webdriver.support.ui import Select
from config import trav1, trav2, payment, my_number, my_provider
from communicate import sms_msg


def buy_tickets(driver, price):
    try:
        # select the lowest price flight
        delay0 = 4
        driver.find_element_by_xpath("//button[@class='btn-secondary btn-action t-select-btn']").click()
        time.sleep(delay0)

        # select return flight
        driver.find_element_by_xpath("//button[@class='btn-secondary btn-action t-select-btn']").click()
        time.sleep(delay0)

        # no thanks to special offer
        driver.find_element_by_xpath("//a[@id='forcedChoiceNoThanks']").click()
        time.sleep(delay0)

        # switch to active tab
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(delay0)

        # continue with booking
        driver.find_element_by_xpath("//button[@class='btn-primary btn-action bookButton']").click()
        time.sleep(delay0)

        # fill out form for first passenger
        delay = 0.25 # seconds
        driver.find_element_by_xpath("//input[@id='firstname[0]']").send_keys(trav1['fname'])
        time.sleep(delay)
        driver.find_element_by_xpath("//input[@id='lastname[0]']").send_keys(trav1['lname'])
        time.sleep(delay)
        driver.find_element_by_xpath("//input[@id='phone-number[0]']").send_keys(trav1['pnum'])
        time.sleep(delay)

        if trav1['gen'] == 'male':
            driver.find_element_by_xpath("//input[@id='gender_male[0]']").click()
        else:
            driver.find_element_by_xpath("//input[@id='gender_female[0]']").click()

        time.sleep(delay)

        try:
            driver.find_element_by_xpath("//input[@id='date_of_birth_month[0]']").send_keys(trav1['mdob'])
            time.sleep(delay)
            driver.find_element_by_xpath("//input[@id='date_of_birth_day[0]']").send_keys(trav1['ddob'])
            time.sleep(delay)
            driver.find_element_by_xpath("//input[@id='date_of_birth_year[0]']").send_keys(trav1['ydob'])
            time.sleep(delay)
        except Exception as e:
            Select(driver.find_element_by_xpath("//select[@id='date_of_birth_month0']")).select_by_visible_text(month_dob[ trav1['mdob'] ])
            time.sleep(delay)
            Select(driver.find_element_by_xpath("//select[@id='date_of_birth_day[0]']")).select_by_visible_text(str(trav1['ddob']))
            time.sleep(delay)
            Select(driver.find_element_by_xpath("//select[@id='date_of_birth_year[0]']")).select_by_visible_text(str(trav1['ydob']))
            time.sleep(delay)


        # fill out form for second passenger
        driver.find_element_by_xpath("//input[@id='firstname[1]']").send_keys(trav2['fname'])
        time.sleep(delay)
        driver.find_element_by_xpath("//input[@id='lastname[1]']").send_keys(trav2['lname'])
        time.sleep(delay)

        # some forms request phone number from second passenger, but not all
        try:
            driver.find_element_by_xpath("//input[@id='phone-number[1]']").send_keys(trav2['pnum'])
            time.sleep(1)
        except Exception as e:
            pass

        if trav2['gen'] == 'male':
            driver.find_element_by_xpath("//input[@id='gender_male[1]']").click()
        else:
            driver.find_element_by_xpath("//input[@id='gender_female[1]']").click()

        time.sleep(delay)

        try:
            driver.find_element_by_xpath("//input[@id='date_of_birth_month[1]']").send_keys(trav2['mdob'])
            time.sleep(delay)
            driver.find_element_by_xpath("//input[@id='date_of_birth_day[1]']").send_keys(trav2['ddob'])
            time.sleep(delay)
            driver.find_element_by_xpath("//input[@id='date_of_birth_year[1]']").send_keys(trav2['ydob'])
            time.sleep(delay)
        except Exception as e:
            Select(driver.find_element_by_xpath("//select[@id='date_of_birth_month1']")).select_by_visible_text(month_dob[ trav2['mdob'] ])
            time.sleep(delay)
            Select(driver.find_element_by_xpath("//select[@id='date_of_birth_day[1]']")).select_by_visible_text(str(trav2['ddob']))
            time.sleep(delay)
            Select(driver.find_element_by_xpath("//select[@id='date_of_birth_year[1]']")).select_by_visible_text(str(trav2['ydob']))
            time.sleep(delay)


        # Enter payment information
        driver.find_element_by_xpath("//input[@class='text billing-cardholder-name cko-field cardholder-above-cardname gb-whitelist']").send_keys(payment['name'])
        time.sleep(delay)
        driver.find_element_by_xpath("//input[@id='creditCardInput']").send_keys(payment['num'])
        time.sleep(delay)
        driver.find_element_by_xpath("//input[@id='new_cc_security_code']").send_keys(payment['code'])
        time.sleep(delay)
        driver.find_element_by_xpath("//input[@class='text billing-address-one cko-field gb-whitelist']").send_keys(payment['add'])
        time.sleep(delay)
        driver.find_element_by_xpath("//input[@class='text billing-city cko-field gb-whitelist']").send_keys(payment['city'])
        time.sleep(delay)
        driver.find_element_by_xpath("//input[@class='text billing-zip-code cko-field gb-whitelist']").send_keys(payment['zip'])
        time.sleep(delay)
        Select(driver.find_element_by_xpath("//select[@class='billing-state-dropdown cko-field billing-state-select gb-whitelist']")).select_by_visible_text(payment['st'])
        time.sleep(delay)
        Select(driver.find_element_by_xpath("//select[@class='cko-field cc-expiry-month gb-whitelist']")).select_by_visible_text(month_cc[ payment['exp_m'] ])
        time.sleep(delay)
        Select(driver.find_element_by_xpath("//select[@class='cko-field cc-expiry-year gb-whitelist']")).select_by_visible_text(str(payment['exp_y']))
        time.sleep(delay)
        driver.find_element_by_xpath("//input[@class='text cko-field always-include gb-whitelist ']").send_keys(trav1['email'])

        try:
            driver.find_element_by_xpath("//input[@id='no_insurance']").click()
        except Exception as e:
            pass

        time.sleep(delay)
        total = driver.find_element_by_xpath("//span[@id='totalPriceForTrip']").text
        msg = 'total purchase: '+total
        print(msg)
        sms_msg(msg, my_number, my_provider)

        time.sleep(delay)
        driver.find_element_by_xpath("//button[@id='complete-booking']").click()

        time.sleep(2*60)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        sys.exit()

    except Exception as e:
        msg = 'error during purchase: '+str(e)
        print(msg)
        sms_msg(msg, my_number, my_provider)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

month_cc = {
    1 : '01-Jan',
    2 : '02-Feb',
    3 : '03-Mar',
    4 : '04-Apr',
    5 : '05-May',
    6 : '06-Jun',
    7 : '07-Jul',
    8 : '08-Aug',
    9 : '09-Sep',
    10: '10-Oct',
    11: '11-Nov',
    12: '12-Dec'
}

month_dob = {
    1 : '01 - Jan',
    2 : '02 - Feb',
    3 : '03 - Mar',
    4 : '04 - Apr',
    5 : '05 - May',
    6 : '06 - Jun',
    7 : '07 - Jul',
    8 : '08 - Aug',
    9 : '09 - Sep',
    10: '10 - Oct',
    11: '11 - Nov',
    12: '12 - Dec'
}