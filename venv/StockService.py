import LinearRegression.LR as lr
import Services.AlphavantageService as alphavantage
import numpy as np
from sklearn.linear_model import LinearRegression
import Plotting.PlotFunctions as plt
import JsonHandler.StockHandler as sh
import FlatData.FlatDataReader as fdr
import Services.DataManipulate as dm
import time

#Run: Used to set which tickers you want, some Ai Settings, and what type of dataset you want to work with

#Ai settings
iterations = 20000
L = 0.1
errortolerance = 20
trials = 1000 #set a trial limit
Error = []
#END Ai settings

#OK Now lets loop through and find the best Learning rate
not_found = True


def deep_analysis_of_stock(ticker):

    # cut data into many components
    # First lets Analyze longest trend
    stock_service = alphavantage.AlphavantageService(ticker, 10, 1, 3, 0)
    lineReg = lr.LR(stock_service.get_data(), ticker)
    mParts, bParts, xParts, yParts, zParts, prediction = lineReg.view_trend_for_subset(2)

    for i in range(len(xParts)):
        print(xParts[i].shape, " >> ", yParts[i].shape)
        print('ticker: ', ticker, 'm: ', mParts[i], 'b: ', bParts[i])
        plt.plot_all(xParts[i], {1: yParts[i], 2: zParts[i]},
                     mParts, bParts[i], None, ticker, 0)

    return mParts, bParts, xParts, yParts, zParts, prediction


def get_watchlist(min_price, max_price, wait, min_slope):

    tickers = fdr.read("C:\\Path\\To\\ticker.txt")
    ticker_batches = dm.pieces(tickers, 750)
    ticker_batches = list(ticker_batches)
    print('Batches: ', len(ticker_batches))

    in_budget_stocks = []
    for i in ticker_batches:
        print("batchSize: ", len(i))
        batchString = ','.join(i)
        print('batch: ', batchString)

        data = sh.get_quotes(batchString)

        for line in data:
            if max_price > float(line['2. price']) > min_price:
                print("price: ", line['2. price'], "symbol: ", line['1. symbol'])
                in_budget_stocks.append(line)
        time.sleep(wait)  # Throttle API Calls

    stock_data = []
    for stock in in_budget_stocks:
        print('Reviewing Symbol: ', stock['1. symbol'])
        stock_service = None
        try:
            stock_service = alphavantage.AlphavantageService(stock['1. symbol'], iterations, L, 0, 15)
        except:
            stock_service.set_data_switch(False)
            continue
        if stock_service is None or stock_service.get_data() is None:
            print('No Data Available for: ', stock['1. symbol'])
            continue
        lineReg = lr.LR(stock_service.get_data(), stock['1. symbol'] + " From " + stock_service.originalX()[0] + " TO "
                        + stock_service.originalX()[len(stock_service.originalX()) - 1])

        mParts, bParts, xParts, yParts, zParts, prediction = lineReg.view_trend_for_subset(1)

        analysis = {'ticker': stock['1. symbol'], 'mParts': mParts, 'bParts': bParts, 'xParts': xParts, 'yParts': yParts,
                    'zParts': zParts, 'pz': prediction}

        stock_data.append(analysis)
        time.sleep(wait)

    watch_list = []

    for analysis in stock_data:
        for i in range(len(analysis['xParts'])):
            print('ticker: ', analysis['ticker'], 'm: ', analysis['mParts'][i], 'b: ', analysis['bParts'][i])
            if analysis['mParts'][i] > min_slope:
                watch_list.append(analysis)
                plt.plot_all(analysis['xParts'][i], {1: analysis['yParts'][i], 2: analysis['zParts'][i]},
                             analysis['mParts'][i], analysis['bParts'][i], analysis['pz'][i], analysis['ticker'], 0)


    ##print('WatchList: ', watch_list)
    return watch_list
