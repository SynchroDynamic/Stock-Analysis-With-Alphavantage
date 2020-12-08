import numpy as np
import scipy.linalg

def gradient_descent(X, Y, w, c, it, L):
    n = len(X)
    Y_pred = w * X + c  # The current predicted value of Y
    D_m = (-2 / n) * sum(X * (Y - Y_pred))  # Derivative wrt m
    D_c = (-2 / n) * sum(Y - Y_pred)  # Derivative wrt c
    m = w - L * D_m  # Update m
    c = c - L * D_c  # Update c

    return m, c


def batch_gradient_descent(x, y, w, eta):
    derivative = np.sum([-(y[d]-np.dot(w.T.copy(),x[d,:]))*(x[d,:]).reshape(np.shape(w)) for d in range(len(x))],axis=0)
    return eta*(1/len(x))*derivative


def mini_batch_gradient_descent(x, y, w, eta, batch):
    gradient_sum = np.zeros(shape=np.shape(w))
    for b in range(batch):
        choice = np.random.choice(list(range(len(x))))
        gradient_sum += -(y[choice]-np.dot(w.T,x[choice,:]))*x[choice,:].reshape(np.shape(w))
        return eta*(1/batch)*gradient_sum


# initialize variables
def trend_for(data, it, L, m, b):
    x = data['x']
    y = data['y']
    w = np.random.normal(size=(np.shape(x)[1], 1))
    c = 0.0
    # Update w
    w_s = []
    Error = []

    for i in range(it):
        # Calculate error
        error = (1 / 2) * np.sum([(y[i] - (b + np.dot(w.T, x[i, :]))) ** 2 for i in range(len(x))])
        #print(error)
        Error.append(error)
        if error == float('inf'):
            print('INFINITY')
            return x, y, m, b, Error

        m, b = gradient_descent(x, y, w, c, it, L)
        w = m
        c = b

        w_s.append(w.copy())

    return x, y, m, b, Error



