import numpy as np
import matplotlib.pyplot as plt


def plot_function(x, y, w,b, Error, st, iterations):
    if len(Error) == iterations:
        fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(40,10))
        ax[0].plot(x, ((x * w) + b), c='lightgreen', linewidth=3, zorder=0)
        ax[0].plot(x, y)
        ax[0].set_title(st)
        ax[1].scatter(range(iterations), Error)
        ax[1].set_title('Error')
        plt.show()
    else:
        print('Plotting Error: Iterations and Errors are different sizes')

def plot_all(x, set, w,b, vw, st, iterations):

    fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(40,10))
    wb = [((xi * w) + b) for xi in x]
    print(wb.shape, " >> ", x.shape)
    wb = np.array(wb).reshape(len(x), 1)
    print(wb.shape, " >> ", x.shape)
    ax[0].plot(x, wb, c='lightgreen', linewidth=3, zorder=0)
    ax[0].plot(x, set[1])
    ax[0].set_title(st)
    try:
        ax[1].plot(x, set[2])
        ax[1].set_title('Volume')
        ax[1].plot(x, vw)
    except:
        ''
    plt.show()
