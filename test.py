import pickle


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

my_df = unpickle_data('data/TEST_df_IAH_NRT_roundtrip_Business_03_01_2020_03_07_2020_.pickle')
