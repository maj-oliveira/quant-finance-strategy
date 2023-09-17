"""
    @author: Matheus José Oliveira dos Santos
    Last Edit: 03/09/2023
"""

from abc import ABC, abstractmethod
from datetime import date, timedelta
#from typing import List

import pandas as pd
import joblib
import tensorflow as tf
import numpy as np

class Backtest(ABC):

    def __init__(self,start_date:date, end_date:date, delta:timedelta, init_NAV:float = 1):
        #get initial parameters
        self.start_date = start_date
        self.end_date = end_date
        self._init_NAV = init_NAV
        self._delta = delta

        #create df_performance
        self._df_performance = pd.DataFrame(columns=['Date','NAV'])
        _new_row = {"Date":self.start_date, "NAV":self._init_NAV}
        self._df_performance = pd.concat([self._df_performance, pd.DataFrame([_new_row])], ignore_index=True)

        #set models and scalers to None
        self.lista_modelos = None
        self.lista_scalers = None

        #save the order of the securities
        self._order_BBGTicker = None

    @abstractmethod
    def new_year(self):
        pass
    
    def new_month(self):
        pass

    def new_week(self):
        pass

    def new_day(self):
        pass

    def make_predictions(self,model_path:str, ar_sample:pd.DataFrame) -> pd.DataFrame:
        model = tf.keras.models.load_model(model_path)
        predictions = model.predict(ar_sample)
        df_predictions = pd.DataFrame(predictions)
        df_predictions.insert(0,'BBGTicker', self._order_BBGTicker)
        df_predictions.rename(columns={0:'probability', 'BBGTicker':'BBGTicker'}, inplace=True)
        df_predictions = df_predictions.reindex(columns=['BBGTicker','probability'])
        df_predictions = df_predictions.sort_values(by='probability', ascending=False)
        df_predictions = df_predictions.reset_index(drop=True)
        return df_predictions
    
    @abstractmethod
    def get_data(self) -> np.array:
        #Implement here your data getter
        #The function has no input and must return a numpy array of the data sample scaled
        #This numpy array will be the input for the make_prediction function

        return None

    @abstractmethod
    def allocation(self, df_input:pd.DataFrame) -> pd.DataFrame:
        #Implement here your allocation function
        #
        return None

    def simple_allocation(self, df_input:pd.DataFrame) -> pd.DataFrame:
        df_aloc = pd.DataFrame()
        df_aloc['BBGTicker'] = df_input.head(10)['BBGTicker']
        df_aloc['%AUM'] = 0.1
        return df_aloc

    @abstractmethod
    def return_securities(df_securities: pd.DataFrame, week_start:date, week_end:date) -> pd.DataFrame:
        #implement here your return of securities function
        #
        pass

    def performance_portfolio_period(self) -> pd.DataFrame:
        ret = returns_stocks(df_aloc['BBGTicker'], week_start,week_end)
        ret=ret.transpose()
        ret = ret.reset_index(drop=True)
        df_aloc['returns'] = ret.iloc[:,0]+1
        df_aloc['returns'] = df_aloc['returns'].fillna(1)
        print(df_aloc)
        return_week = np.dot(df_aloc['returns'],df_aloc['%AUM'])
        print(return_week)
        NAV = df_performance.iloc[-1,1]*return_week
    
        new_row = {"Date":week_end, "NAV":NAV}
        df_performance = df_performance.append(new_row, ignore_index=True)
        
        return df_performance

    def executar(self):
        
        if self.lista_modelos == None:
            raise ValueError("Sorry, you must give a list of NN models to the variable self.lista_modelos")

        if self.lista_scalers == None:
            raise ValueError("Sorry, you must give a list of NN scalers to the variable self.lista_scalers")

        self._prev_year = None
        self._date_indicator = self.start_date
        self._model = self.lista_modelos[0]
        self._sc = self.lista_scalers[0]

        
        self._df_portfolio_over_time = pd.DataFrame()
        _new_row = {"Date":self.start_date, "BBGTicker":None}

        self._df_portfolio_over_time=self._df_portfolio_over_time.append(_new_row, ignore_index=True)

        

        while self._date_indicator < self.end_date:

            #somar delta para data final
            week_end = self._date_indicator - timedelta(days=7) + self._delta - timedelta(days=1)

            self._ar_sample = self.get_data()
            self._df_predictions = self.make_predictions(self._model, self._ar_sample) #predict
            self._df_aloc = allocation(self._df_predictions) #allocation

            self._df_portfolio_over_time = pd.concat([self._df_portfolio_over_time, self._df_aloc], ignore_index=True)
            self._df_performance = performance_portfolio_period(self._df_aloc, self.df_performance, week_start, week_end) #calculate performance

            #eventos de datas

            if self._prev_year != self._date_indicator.year:
                self.new_year()
        
        #somar delta para data inicial
        self._date_indicator += self._delta
    
    def get_performance(self) -> pd.DataFrame:
        return self._df_performance

    def get_portfolio_over_time(self) -> pd.DataFrame:
        return self._df_portfolio_over_time
    
    def set_date_indicator(self, date_set:date) -> None:
        self._date_indicator = date_set
    
    def set_model(self, model_name:str) -> None:
        self._model = model_name
    
    def set_scaler(self,scaler_name:str) -> None:
        self._sc = scaler_name