import numpy as np
from sklearn.linear_model import LinearRegression
import Plotting.PlotFunctions as plt
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
import sklearn.metrics as metrics

class LR:

    model = None
    vmodel = None
    x = None
    y = None
    z = None
    accuracies = []


    def __init__(self, data, t):
        self.x = np.array(data['x']).reshape((-1, 1))
        self.y = np.array(data['y'])
        self.z = np.array(data['z'])
        self.ticker = t

        self.model = LinearRegression()
        self.vmodel = LinearRegression()
        self.model.fit(self.x, self.y)
        try:
            self.vmodel.fit(self.x, self.z)
        except:
            self.vmodel = None

    def get_trend(self):
        return self.model.coef_, self.model.intercept_


    def predict(self, x):
        return self.model.predict(x)

    def pieces(self, l, n):
        n = max(1, n)
        return (l[i:i + n] for i in range(0, len(l), n))

    def regressorOp(self, x, y):
        """
        This will optimize the parameters for the algo
        """
        regr_rbf = SVR(kernel="rbf", verbose=True, cache_size=1024)
        C = [10000, 6000, 5000, 1000, 10, 1]
        gamma = [0.005, 0.004, 0.003, 0.002, 0.001, 1, 2, 3, 4]
        epsilon = [0.1, 0.01, 0.05, 1]
        parameters = {"C": C, "gamma": gamma, "epsilon": epsilon}

        gs = GridSearchCV(regr_rbf, parameters, scoring="neg_mean_squared_error", cv=2, iid=True)
        gs.fit(x, y)

        #print("Best Estimator:\n", gs.best_estimator_)
        #print("Type: ", type(gs.best_estimator_))
        return gs.best_estimator_

    def view_trend_for_subset(self, sets):
        # Data is deviation, and originalData is true timeseries
        # (data.x = 0,1,2,...,n | originalData.x = 01-01-2020, ..., 02-01-2020, ..., n
        xPieces = self.pieces(self.x, int(len(self.x) / sets))
        yPieces = self.pieces(self.y, int(len(self.y) / sets))
        try:
            zPieces = self.pieces(self.z, int(len(self.z) / sets))
        except:
            zPieces = []
        xPieces = list(xPieces)
        yPieces = list(yPieces)
        zPieces = list(zPieces)

        xParts = []
        yParts = []
        zParts = []
        mParts = []
        bParts = []
        predictions = []
        # print(xPieces[3], yPieces[3], "\n",  xPieces[4], yPieces[4])
        for sub in range(sets):
            try:
                z = zPieces[sub]
            except:
                z = -1
            subdata = {'x': xPieces[sub], 'y': yPieces[sub], 'z': z}
            #print(subdata)
            self.model = LinearRegression()
            self.model.fit(subdata['x'], subdata['y'])
            #self.vmodel = SVR(kernel='poly', gamma='auto')
            #self.vmodel.fit(subdata['x'], subdata['z'].ravel())

            if z != -1:
                clf = self.regressorOp(subdata['x'], subdata['z'].ravel())
                clf.fit(subdata['x'], subdata['z'].ravel())

                y_pred = clf.predict(subdata['x'])

                accuracy = clf.score(subdata['x'], subdata['z'].ravel())
                variance = metrics.explained_variance_score(subdata['z'], y_pred)
                self.accuracies.append(accuracy)
                prediction = (clf.predict(subdata['x']))
                predictions.append(prediction)

            #print("prediction: ", prediction)

            xParts.append(subdata['x'])
            yParts.append(subdata['y'])
            zParts.append(subdata['z'])
            mParts.append(self.model.coef_)
            bParts.append(self.model.intercept_)

            #plt.plot_all(subdata['x'], {1: subdata['y'], 2: subdata['z']}, self.model.coef_, self.model.intercept_, prediction, self.ticker, 0)

            #print("PARAMS: ", clf.get_params(True))
        return mParts, bParts, xParts, yParts, zParts, predictions


