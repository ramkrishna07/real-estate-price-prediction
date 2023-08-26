import pickle
import json
import numpy as np

__locations = None
__data_columns = None
__model = None
# this function will predict the price based on features
def get_estimated_price(location,sqft,bhk,bath):
    try:
        # accessing the index of the locations
        # lower function is used because in json file all 
        # locations are stored in lowercase letters 
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1
    # creating a numpy array with initial values zero       
    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    # it make the location index as 1 and all the remaining 
    # indexes as 0
    if loc_index>=0:
        x[loc_index] = 1
    #this function will return a 2d array and the array contains 
    # single variable so the estimated price will be the
    #  0th index of the 2d array   
    # price can be float so we are rounding off upto 2 decimal places     

    return round(__model.predict([x])[0],2)

# this function will load the saved artifacts
def load_saved_artifacts():
    print("loading saved artifacts...start")
    global  __data_columns
    global __locations

    #opening the json file and loading and saving into python dictionary
    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    global __model
    if __model is None:
        with open('./artifacts/banglore_home_prices_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")

# this function will read the locations from the json file and return all the locations
def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar',1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2)) # other location
    print(get_estimated_price('Ejipura', 1000, 2, 2))  # other location