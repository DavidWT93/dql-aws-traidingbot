from datetime import datetime, timedelta
import config
from l_df_to_rds import load_data_to_rds
from t_tech_indic import calculate_technical_indicators
from e_t_alpaca_api_data_to_df import extract_btc_bars_from_alpaca_api_transform_to_df
import re


def extract_alpaca_data(symbol, lookBack, timeFrame, extractMethod):
    lookBackParams = lookBack.split("_")
    startTime = datetime.now()

    if lookBackParams[1] == "days":
        delta = timedelta(days=int(lookBackParams[0]))
    elif lookBackParams[1] == "min":
        delta = timedelta(minutes=int(lookBackParams[0]))
    elif lookBackParams[1] == "hour":
        delta = timedelta(hours=int(lookBackParams[0]))

    else:
        return print("Error: lookBack parameter not valid!")

    endTime = startTime - delta
    startTime = startTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    endTime = endTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    dataAsDf = extractMethod(symbol,
                             endTime, startTime,
                             timeFrame=timeFrame)

    return dataAsDf


def find_biggest_number_in_list_of_strings(listOfStrings):
    biggestNumber = 0
    for string in listOfStrings:
        if bool(re.search(r'\d', string)):
            number = int(re.findall(r'\d+', string)[0])
            if number > biggestNumber:
                biggestNumber = number
    return biggestNumber


def convert_no_in_string_to_min(string, time):
    if "min" in string:
        minutes = time
    elif "hour" in string:
        minutes = time * 60
    elif "days" in string:
        minutes = time * 60 * 24
    else:
        minutes = time
        print("found no time string")
    return minutes


def transform_data(stockData, transformMethod, *transformParams,
                   handleNa="fill", replaceNaWith=0):
    # Drop duplicate columns from DataFrame
    stockData = stockData.T.drop_duplicates()
    stockData = stockData.T

    # get new features from stock data
    transformedData = transformMethod(stockData, *transformParams)

    if handleNa == "drop":
        # drops na column
        transformedData = transformedData.dropna()

    elif handleNa == "fill":
        # replace NAN and Null values with replaceNaWith
        transformedData = transformedData.fillna(replaceNaWith)
    else:
        # if handleNa is not "drop" or "fill" do nothing
        pass

    return transformedData


def E_alpaca_last_n_crypto_T_tech_indic_L_rds(cryptoSymbol, lookBack, timeFrame, technicalInd, columnsOfInterest,
                                              TableName,createNewTable=False):
    # since calculating technical indicators makes columns NA, we need to add lookback to the time frame to account for
    # the missing values
    lookBackArg = lookBack.split("_")
    lookBackToCountForNA = find_biggest_number_in_list_of_strings(technicalInd)
    lookBackMin = convert_no_in_string_to_min(lookBack, int(lookBackArg[0]))
    timeFrameMin = convert_no_in_string_to_min(timeFrame, int(re.findall(r'\d+', timeFrame)[0]))
    minToAddToLookback = lookBackToCountForNA * timeFrameMin

    lookBack = str(lookBackMin + minToAddToLookback) + "_min"

    cryptoDataDF = extract_alpaca_data(cryptoSymbol, lookBack, timeFrame,
                                       extract_btc_bars_from_alpaca_api_transform_to_df)
    cryptoDataWithIndicatorsDF = transform_data(cryptoDataDF, calculate_technical_indicators, technicalInd,
                                                handleNa="drop")
    cryptoDataWithIndicatorsDF = cryptoDataWithIndicatorsDF[columnsOfInterest]
    load_data_to_rds(cryptoDataWithIndicatorsDF, TableName, "time_stamp",createTable=createNewTable)
