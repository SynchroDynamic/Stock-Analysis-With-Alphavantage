import numpy as np
import json
import requests


key = 'your key here'
#Alphavantage specific variables
interval = {1:'1min', 5:'5min', 15:'15min', 30:'30min', 60:'60min', 'daily':'Daily', 'month': 'Monthly Time Series'} #min allowed: 1, 5, 15, 30, 60 > Daily: 'Daily'
function = {'intra' :'TIME_SERIES_INTRADAY', 'daily': 'TIME_SERIES_DAILY', 'month': 'TIME_SERIES_MONTHLY'}
i_type = {'intra': 0, 'none': 1}
#END Alphavantage specific variables

# A simple function that allows for easier transition between AlphaVantage's "intraday" 1,5,15,30,60 minute time series,
# and their "Daily" series
def alphavantage_time_series_url(function, ticker, interval, i_type):

    url = 'https://www.alphavantage.co/query?function=' + function

    switcher = {
        0: url + '&symbol=' + ticker + '&interval=' + interval + '&outputsize=full&apikey=' + key,
        1: url + '&symbol=' + ticker + '&apikey=' + key,
        2: url + '&symbol=' + ticker + '&interval=1min&apikey=' + key
    }
    return switcher.get(i_type, "Invalid type")

def load_data(function, ticker, interval, i_type):
    url = alphavantage_time_series_url(function, ticker,  interval, i_type)
    params = {"retina_name": "en_associative","start_index": 0, "max_results": 1, "sparsity": 1.0, "get_fingerprint": False}
    r = requests.get(url=url, params=params)
    data_str = r.json()

    ds = json.dumps(data_str)
    json_obj = json.loads(ds)
    try:
        if interval == 'Monthly Time Series' or interval == 'Technical Analysis: VWAP':
            dataset = json_obj[interval]
        else:
            dataset = json_obj["Time Series (" + interval + ")"]
    except:
        return None, None

    x = []
    ox = []
    y = []
    z = []
    count = 0
    for key in dataset:
        x.append(count)
        count += 1
        ox.append(key)
        try:
            y.append(average([float(dataset[key]["2. high"]), float(dataset[key]["3. low"])]))
            z.append(float(dataset[key]["5. volume"]))
        except:
            y.append(float(dataset[key]["VWAP"]))

    if len(y) % 2 != 0:
        y.pop(0)
        x.pop(0)
        try:
            z.pop(0)
        except:
            z = None

    #deviation = Reverse(cut_mean_from_elements(y))
    #zdev = Reverse(cut_mean_from_elements(z))

    deviation = Reverse(y)
    try:
        zdev = Reverse(z)
        np_z = np.array(zdev).reshape(len(z), 1)
    except:
        np_z = None

    np_x = np.array(x).reshape(len(x), 1)
    np_y = np.array(deviation).reshape(len(y), 1)

    #print(ox)
    return {'x': np_x, 'y': np_y, 'z': np_z}, {'ox': Reverse(ox), 'y': y}

def get_quotes(symbols):
    url = 'https://www.alphavantage.co/query?function=BATCH_STOCK_QUOTES&apikey=' + key + '&symbols=' + symbols
    params = {"retina_name": "en_associative", "start_index": 0, "max_results": 1, "sparsity": 1.0,
              "get_fingerprint": False}
    r = requests.get(url=url, params=params)
    print(r)
    data_str = r.json()

    ds = json.dumps(data_str)
    json_obj = json.loads(ds)

    dataset = json_obj["Stock Quotes"]

    return dataset

def Reverse(lst):
    return [ele for ele in reversed(lst)]


def average(set):
    count = len(set)
    total = 0
    for part in set:
        total += part

    return total / count


def cut_mean_from_elements(set):
    mean = average(set)
    deviation = []
    for element in set:
        deviation.append(element - mean)

    return deviation
