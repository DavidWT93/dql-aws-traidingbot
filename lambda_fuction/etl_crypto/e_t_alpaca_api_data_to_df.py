import json
import pandas as pd
import requests
import config

def extract_btc_bars_from_alpaca_api_transform_to_df(symbol, startDate, endDate, timeFrame="1Hour",
                                                     apiKey=config.ALPACA_API_KEY,
                                                     apiSecret=config.ALPACA_SECRET_KEY):
    # extracting data from alpaca api

    url = f'https://data.alpaca.markets/v1beta3/crypto/us/bars?symbols={symbol}&start={startDate}&end={endDate}&timeframe={timeFrame}&limit=10000'
    headers = {'APCA-API-KEY-ID': apiKey, 'APCA-API-SECRET-KEY': apiSecret}
    response = requests.get(url, headers=headers)
    responseDict = json.loads(response.text)
    listWithNewsData = []
    barsData = responseDict["bars"][symbol]
    for i in range(len(barsData)):
        timeStamp = barsData[i]["t"]
        close = barsData[i]["c"]
        volume = barsData[i]["v"]
        numberOfTrades = barsData[i]["n"]
        listWithNewsData.append([timeStamp, close,
                                 volume, numberOfTrades])
        df = pd.DataFrame(listWithNewsData, columns=["time_stamp", "close",
                                                     "volume", "number_of_trades"])

    return df