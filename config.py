import sys


'''
geckodriver must be in project main folder

'''

inputs = {
    'dep' : 'IAH',                      # 3 letter airport code
    'arr' : str(sys.argv[1]),           # 3 letter airport code as entered by the user at the command line
    'flight_type' : 'roundtrip',        # 'one way' or 'roundtrip'
    'fare_type' : 'Business',           # 'Business' or 'Economy/Coach'
    'dep_date' : str(sys.argv[2]),      # 'mm/dd/yyyy'
    'return_date' : str(sys.argv[3]),   # 'mm/dd/yyyy' .. enter xx/xx/xxxx if flight type is 'one way'
    'travelers_count' : 2               # 2 for purchasing fare.
    }

params = {
    'freq' : 1,                         # how frequent to get pricing data (1= daily, 2= every other day, 7= 1/wk
    'length period' : 90,               # how many days beyond initial departure date to do price search
    'email_recipient' : 'diego.a.galindo@gmail.com', # for lowest fair / price drop notifications
    'sms_recipient' : '8137489298',     # for price notification
    'sms_provider' : 'verizon',         # for price notification
    'threshold' : 1000                  # purchase tickets if price below threshold
}

trav1 = {
    'fname' : 'Diego',
    'lname' : 'Galindo',
    'pnum'  ; '8137489298',
    'gen'   : 'male',
    'mdob'  : 11,
    'ddob'  : 19,
    'ydob'  : 1982,
    'email' : 'diego.a.galindo@gmail.com'
}

trav2 = {
    'fname' : 'Maureen',
    'lname' : 'Restauro',
    'pnum'  ; '8137489298',
    'gen'   : 'female',
    'mdob'  : 10,
    'ddob'  : 12,
    'ydob'  : 1982
}

payment = {
    'name'  : str(sys.argv[4]),     # name
    'num'   : str(sys.argv[5]),     # card num
    'exp_m' : 11,
    'exp_y' : 24,
    'code'  : 503,
    'add'   : '2000 Bagby Street 3441',
    'city'  : 'Houston',
    'st'    : 'TX',
    'zip'   : 77002
}


# contact info to send SMS when an Exception is raised
my_number = '8137489298'
my_provider = 'verizon'