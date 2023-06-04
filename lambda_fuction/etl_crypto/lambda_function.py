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



