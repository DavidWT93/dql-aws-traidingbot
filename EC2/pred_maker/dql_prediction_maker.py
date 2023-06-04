import config
from sql_master import SQLHandling
from dql_ml_agent import Make_ml_predictions
import time
import boto3
import datetime

sh = SQLHandling(host=config.AWS_RDS_HOST,
                 user=config.AWS_RDS_USER,
                 password=config.AWS_RDS_PASSWORD,
                 port=int(config.AWS_RDS_PORT),
                 database=config.AWS_RDS_DB)

s3 = boto3.client('s3',
                  aws_access_key_id=config.AWS_S3_USER_ID,
                  aws_secret_access_key=config.AWS_S3_USER_PASSWORD)

model = "dql_model_v1.h5"
s3.download_file(config.AWS_S3_ML_MODEL_BUCKET_NAME, f'current_model/{model}', model)
tradingAgent = Make_ml_predictions(model, sh)


def predict():
    run = True
    madeDecision = False
    while run:
        now = datetime.datetime.now()
        if now.hour == 1 and 30 == now.minute:
            # updates model every day at 1:30 with a model stored in a s3 bucket
            s3.download_file(config.AWS_S3_ML_MODEL_BUCKET_NAME, f'current_model/{model}', model)
            tradingAgent.load_new_model(model)

        if time.localtime().tm_min % 10 == 0:
            # makes a prediction every 10 minutes
            while not madeDecision:
                tradingAgent.load_last_n_sql_to_ml_predict_save_decision(inputTableName="auto_input1",
                                                                         outputTableName="auto_res6",
                                                                         columnToOrder="time_stamp",
                                                                         lookBackNo=str(30),
                                                                         columnsToDrop=["time_stamp", "close"])
                madeDecision = True
            time.sleep(480)
            madeDecision = False


if __name__ == "__main__":
    predict()
