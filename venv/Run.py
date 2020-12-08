import StockService as ss

wl = ss.get_watchlist(100, 105, 15, 0.1)
print(wl)
# Now, once we get are watch list, we can Do further analysis.
for analysis in wl:
    print('Deep Analysis', ss.deep_analysis_of_stock(analysis['ticker']))