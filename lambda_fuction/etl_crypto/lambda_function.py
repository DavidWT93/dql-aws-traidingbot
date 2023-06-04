from full_etl_pipeline import E_alpaca_last_n_crypto_T_tech_indic_L_rds


def lambda_handler(event, context):
    cryptoSymbol = event["symbol"]
    lookBack = event["lookBack"]
    timeFrame = event["timeFrame"]
    technicalInd = event["technicalInd"]
    columnsOfInterest = event["columnsOfInterest"]
    TableName = event["TableName"]
    createNewTable = event["createNewTable"]
    if createNewTable == "True":
        newTable = True
    else:
        newTable = None

    E_alpaca_last_n_crypto_T_tech_indic_L_rds(cryptoSymbol, lookBack, timeFrame, technicalInd, columnsOfInterest,
                                              TableName,newTable)
    return {
        "status_code":200,

    }



if __name__ == '__main__':
    event = {"symbol":"BTC/USD",
             "lookBack":"20_min",
             "timeFrame":"1min",
             "technicalInd":["VWAP","RSI_2"],
             "columnsOfInterest":["VWAP","RSI_2","close","time_stamp"],
             "TableName":"ta8",
             "createNewTable":"f"}
    lambda_handler(event,None)