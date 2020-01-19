import pickle
from config import inputs
from communicate import sms_msg

# contact info to send SMS when an Exception is raised
my_number = '8137489298'
my_provider = 'verizon'

def pickle_data(df):
    '''
    df = panda DataFrame object to save
    returns the name of the file for the pickled data
    '''
    file_name = 'df_'

    try:
        for i in inputs.keys():
            file_name = file_name + str(inputs[i]) + '_'

        file_name = file_name.replace('/', '_')
        file_name = './data/' + file_name + '.pickle'

        with open(file_name, 'wb') as f:
            pickle.dump(df, f)
            f.close()
    except Exception as e:
        msg = 'An error occurred in pickle_all_data_df function\n' + str(e)
        print(msg)
        sms_msg(msg, my_number, my_provider)
    finally:
        return file_name


def unpickle_data(file_name):
    df = 0
    try:
        with open(file_name, 'rb') as f:
            df = pickle.load(f)
            f.close()
    except Exception as e:
        msg = 'An error occurred in trying to unpickle data\n' + str(e)
        print(msg)
    finally:
        return df
