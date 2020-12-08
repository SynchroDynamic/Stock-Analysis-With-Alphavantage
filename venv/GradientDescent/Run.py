#PUT IN RUN FILE TO TEST

import Services.AlphavantageService as alphavantage

#Run: Used to set which tickers you want, some Ai Settings, and what type of dataset you want to work with

#Data settings
ticker = 'CRC'
#End settings

#Ai settings
iterations = 20000
L = 0.1
errortolerance = 90
trials = 1000 #set a trial limit
Error = []
#END Ai settings

def getAddend(place, num):

    Lmultiplier = num
    for p in range(place):
        Lmultiplier = Lmultiplier / 10

    return Lmultiplier

#OK Now lets loop through and find the best Learning rate
not_found = True

#The stock service holds everything including the current dataset.
stock_service = alphavantage.AlphavantageService(ticker, iterations, L)

ranTwice = False #After a solid line is found. This switch will cause the sequence to run the identical sequence again
                 #To ensure the best fit.
close = False #This switch ensures that the learning rate does not reconstitute a smaller learning rate when close to the best fit.
lastL = None #In the event the next sequence breaks while close, this will store the last "good" fit learning rate.

def init():
    while not_found: #Get the General Trend

        w, b, error = stock_service.view_trend_for(L)
        Error.append(error)
        lastL = L
        if error < errortolerance:
            if ranTwice:
                not_found = False
                stock_service.plot_trend(errortolerance, error)
            else:
                print("Ensuring Best fit")
                ranTwice = True
                continue
            print('NEW L : ', L, 'ERROR: ', error)
        else:
            lStr = str(L)
            lStr = lStr[2:]
            print(lStr)
            place = len(lStr)

            if error < errortolerance:
                close = True
                L = L + getAddend(place)
                print(place)
                L = round(L, place)

            else:
                if close:
                    L = L + getAddend(place, 1)
                else:
                    L = getAddend(place + 1, 1)
                #print(place)
                L = round(L, place + 1)

            print('NEW L : ', L, 'ERROR: ', error)

mParts, bParts, error = stock_service.view_trend_for_subset(0.00025, 4)

print("M: ", mParts)
print("B: ", bParts)


#Now lets just get a
#w, b, error = alphavantage.get_trendline_for(ticker, iterations, L)

#print(ticker, "'s current trend is: ", w, "X + ", b, "= Yprediction  with Error: +/-", error)
