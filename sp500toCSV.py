import yfinance as yfy
import pandas as pd
import time

constituents_symbols = open('constituents_symbols.txt', 'r')

spy = yf.Ticker('SPY')
spyDF = spy.history(period='max')
for col in spyDF.columns:
    if not (col == 'Date' or col == 'Close' or col == 'Volume'):
      spyDF.pop(col)

spyDF['Last Close'] = spyDF.Close.shift(1)
spyDF['Last Volume'] = spyDF.Volume.shift(1)
spyDF.pop('Volume')


symbols = []
for s in constituents_symbols.readlines():
  symbol = s.strip()
  symbols.append(symbol)


fullDF = spyDF.copy()
num = len(symbols)
for i, symbol in enumerate(symbols):
  print(f'Getting data for {symbol}...... {i}/{num}')
  stock = yf.Ticker(symbol)
  df = stock.history(period='max')
  for col in df.columns:
    if not (col == 'Date' or col == 'Close'):
      df.pop(col)
  df[symbol+" Last"] = df.Close.shift(1)
  df.pop('Close')
  # fullDF = pd.concat([fullDF, df], axis=1)
  try:
    fullDF = pd.concat([fullDF, df], axis=1)
  except:
    print(f'Unable to fetch data for {symbol}.')  
  # fullDF.to_csv('SP500_prog.csv')
  time.sleep(1)

fullDF.to_csv('SP500.csv')
