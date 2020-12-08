import GradientDescent.GD as gd
import Plotting.PlotFunctions as plt
import JsonHandler.StockHandler as sh
import Services.DataManipulate as dm
import LinearRegression.LR as lr

class AlphavantageService:
    data = None
    originalData = None
    ticker = None
    iterations = None
    L = None
    x = None
    y = None
    m = 0.0
    b = 0.0
    Error = None
    DataSet = True

    def __init__(self, t, i, l, stype, mins):
        self.ticker = t
        self.iterations = i
        self.L = l
        if stype == 0:
            self.data, self.originalData = sh.load_data(sh.function['daily'], t, sh.interval['daily'], sh.i_type['none'])
        elif stype == 1:
            try:
                self.data, self.originalData = sh.load_data(sh.function['intra'], t, sh.interval[mins],
                                                        sh.i_type['intra'])
            except:
                self.DataSet = False
        elif stype == 2:
            self.data, self.originalData = sh.load_data(sh.function['month'], t, sh.interval['month'],
                                                        sh.i_type['none'])
        elif stype == 3:
            self.data, self.originalData = sh.load_data('VWAP', t, 'Technical Analysis: VWAP',
                                                        2)

    def get_data(self):
        return self.data

    def set_data_switch(self, val):
        self.DataSet = val

    def originalX(self):
        return self.originalData['ox']


    def view_trend_for(self, l):
        self.L = l
        # Data is deviation, and originalData is true timeseries
        # (data.x = 0,1,2,...,n | originalData.x = 01-01-2020, ..., 02-01-2020, ..., n
        self.x, self.y, self.m, self.b, self.Error = gd.trend_for(self.data, self.iterations, self.L, self.m, self.b)
        return self.m, self.b, self.Error[len(self.Error) - 1] / len(self.x)

    def gradient_descent(self, l, sets, ticker):
        self.L = l
        # Data is deviation, and originalData is true timeseries
        # (data.x = 0,1,2,...,n | originalData.x = 01-01-2020, ..., 02-01-2020, ..., n
        xPieces = dm.pieces(self.data['x'], int(len(self.data['x']) / sets))
        yPieces = dm.pieces(self.data['y'], int(len(self.data['y']) / sets))

        xPieces = list(xPieces)
        yPieces = list(yPieces)
        xParts = []
        yParts = []
        mParts = []
        bParts = []
        # print(xPieces[3], yPieces[3], "\n",  xPieces[4], yPieces[4])
        for sub in range(sets):
            subdata = {'x': xPieces[sub], 'y': yPieces[sub]}
            xPart, yPart, mPart, bPart, ErrorPart = gd.trend_for(subdata, self.iterations, self.L, 0.0, 0.0)
            xParts.append(xPart)
            yParts.append(yPart)
            mParts.append(mPart)
            bParts.append(bPart)

            plt.plot_function(self.originalData['ox'], yPart, mPart, bPart, ErrorPart, self.ticker, self.iterations)

        return mParts, bParts, 0

    def linear_regression(self, sets):
        return lr.view_trend_for_subset(sets)

    def plot_trend(self, acceptedError, error):
        # Plot the predicted function and the Error
        if error < acceptedError:
            plt.plot_function(self.x, self.y, self.m, self.b, self.Error, self.ticker, self.iterations)

    def get_daily_trend_for(ticker, iterations, L):
        data, originalData = sh.load_data(sh.function['daily'], ticker, sh.interval['daily'], sh.i_type['none'])
        x, y, m, b, self.Error = gd.trend_for(data, iterations, L)
        return m, b, Error[len(Error) - 1]

    def get_trendline_for(ticker, iterations, L):
        data, originalData = sh.load_data(sh.function['intra'], ticker, sh.interval[60], sh.i_type['intra'])
        x, y, m, b, Error = gd.trend_for(data, iterations, L)
        return m, b, Error[len(Error) - 1]
