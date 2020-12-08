

def read(file):
    tickers = []
    with open(file) as f:
        for line in f:
            line = line.replace("\n", "")
            tickers.append(line)

    return tickers
