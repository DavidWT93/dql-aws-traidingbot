from keras.models import load_model
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
import numpy as np


class Make_ml_predictions:
    def __init__(self, mlModelPath, sqlHandlingObj, balance=100_000, risk=10, data=None):

        if data is None:
            self.data = pd.DataFrame()
        self.model = load_model(mlModelPath)
        self.sh = sqlHandlingObj

        # balance data init
        self.balance = float(balance)
        self.risk = float(risk / 100)
        self.investment = float(self.balance * self.risk)
        self.percentageReturn = float(0)
        self.sellPrice = float(0)
        self.boughtPrice = float(0)
        self.bought = False

    def print_model_params(self):
        print(self.model.summary())
        print(self.model.input_shape)

    def load_new_model(self, mlModelPath):
        self.model = load_model(mlModelPath)

    def update_trade(self):
        self.investment = self.balance * self.risk

    def get_data_from_sql(self, tabelName, columnToOrder, n):
        self.data = self.sh.get_n_laste_entries_from_table_by_order_colum(tabelName, columnToOrder, n)

    def current_data(self):
        self.currentData = pd.DataFrame(self.data.iloc[-1]).T

    def transform_data_to_ml_input(self, columnsToDrop=None):
        """
        data is transformed to the input shape of the model

        :param columnsToDrop:
        :return:
        """


        if columnsToDrop is None:
            columnsToDrop = []
        self.MLInput = self.data.drop(columnsToDrop, axis=1)
        scaler = MinMaxScaler()
        scaledData = scaler.fit_transform(self.MLInput)
        self.MLInput = scaledData.reshape(1, int(self.model.input_shape[1]), int(self.model.input_shape[2]))

    def make_predictions(self):
        self.prediction = self.model.predict(self.MLInput)

    def buy_sell(self):
        """
        Here the buy sell logic is implemented, also the current balance is updated

        :return:
        trading decision
        """

        if np.argmax(self.prediction) == 0 and self.bought is False:
            self.bought = True
            self.boughtPrice = self.currentData["close"].values[0]
            return "buy"
        elif np.argmax(self.prediction) == 1 and self.bought is True:
            self.bought = False
            self.sellPrice = self.currentData["close"].values[0]
            self.percentageReturn = (self.sellPrice - self.boughtPrice) / self.boughtPrice
            self.balance = self.balance + self.investment * self.percentageReturn
            self.update_trade()
            return "sell"
        elif np.argmax(self.prediction) == 0 and self.bought is True:
            return "hold"
        else:
            return "do_nothing"

    def get_decision_as_df(self):
        """
        This function creates a df with the trading decision and the current balance, which can
        be saved to a sql table

        :return:
        """
        self.current_data()
        self.currentData["decision"] = self.buy_sell()
        self.currentData["balance"] = round(self.balance, 2)
        self.currentData["percentage_return"] = round(self.percentageReturn*100, 2)
        self.currentData["investment"] = round(self.investment, 2)
        self.tradingDecision = self.currentData[["balance", "time_stamp", "decision",
                                                 "percentage_return", "investment", "close"]]

    def load_decision_to_sql(self, tableName):
        """
        here the trading decision is saved to a sql table

        :param tableName: table name to save the trading decision
        :return:
        """

        self.sh.create_table_of_df_set_index(self.tradingDecision, tableName, "time_stamp", True)

    def load_last_n_sql_to_ml_predict_save_decision(self, inputTableName, outputTableName, columnToOrder,
                                                    lookBackNo, columnsToDrop=None):
        """
        This function loads the last n entries from a sql table, makes a prediction and saves the trading decision to
        a sql table


        :param inputTableName: sql table name to load the data from, to make a prediction with
        :param outputTableName: table name to save the trading decision
        :param columnToOrder: date column to order the data by and to get the last n entries from
        :param lookBackNo: how many entries to load to the ml model to make a prediction with
        :param columnsToDrop: columns forom the input table to drop before loading the data to the ml model to make
                              a prediction with
        :return: prediction and trading decision saved to a sql table
        """

        self.get_data_from_sql(inputTableName, columnToOrder, lookBackNo)
        self.transform_data_to_ml_input(columnsToDrop)
        self.make_predictions()
        self.get_decision_as_df()
        self.load_decision_to_sql(outputTableName)
