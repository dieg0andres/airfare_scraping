
'''
geckodriver must be in project main folder

'''

inputs = {
    'dep' : 'IAH',                  # 3 letter airport code
    'arr' : 'LHR',                  # 3 letter airport code
    'flight_type' : 'roundtrip',      # 'one way' or 'roundtrip'
    'fare_type' : 'Business',       # 'Business' or 'Economy/Coach'
    'dep_date' : '04/01/2020',      # 'mm/dd/yyyy'
    'return_date' : '04/07/2020'   # 'mm/dd/yyyy' .. enter xx/xx/xxxx if flight type is 'one way'
    }

params = {
    'freq' : 1,    # how frequent to get pricing data (1= daily, 2= every other day, 7= 1/wk
    'length period' : 2,  # how many days beyond initial departure date to do price search
    'email_recipient' : 'diego.a.galindo@gmail.com', # for lowest fair / price drop notifications
    'sms_recipient' : '8137489298',     # for price notification
    'sms_provider' : 'verizon',          # for price notification
    'price_drop_threshold' : 0.8        # if current price minimum is < avg price minimum * threshold --> price drop
}

# contact info to send SMS when an Exception is raised
my_number = '8137489298'
my_provider = 'verizon'