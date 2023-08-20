from datetime import date, timedelta
import pandas as pd
from xbbg import blp
import joblib

class Backtest:

    def __init__(self,start_date:date, end_date:date,delta:timedelta, init_NAV:float = 1):
        self.start_date = start_date
        self.end_date = end_date
        self._init_NAV = init_NAV
        self._delta = delta
        self._df_performance = pd.DataFrame()
        _new_row = {"Date":start_date, "NAV":self._init_NAV}
        self._df_performance=self._df_performance.append(_new_row, ignore_index=True)
        self.lista_modelos = None
        self.lista_scalers = None

    def new_year(self):
        pass
    
    def new_month(self):
        pass

    def new_week(self):
        pass

    def new_day(self):
        pass

    def make_predictions(self,model_path:str, df_sample:pd.DataFrame):
        model = tf.keras.models.load_model(model_path)
        predictions = model.predict(df_sample[:,1:])
        df_predictions = pd.DataFrame(predictions)
        df_predictions.insert(0,'BBGTicker', df_sample['BBGTicker'])
        df_predictions.rename(columns={0:'probability', 'BBGTicker':'BBGTicker'}, inplace=True)
        df_predictions = df_predictions.reindex(columns=['BBGTicker','probability'])
        df_predictions = df_predictions.sort_values(by='probability', ascending=False)
        df_predictions = df_predictions.reset_index(drop=True)
        return df_predictions
    
    def get_data(self) -> pd.DataFrame:
        #Implement here your data getter
        return None

    def allocation(self, df_input:pd.DataFrame) -> pd.DataFrame:
        df_aloc = simple_allocation(df_input)
        return df_aloc

    def simple_allocation(self, df_input:pd.DataFrame) -> pd.DataFrame:
        df_aloc = pd.DataFrame()
        df_aloc['BBGTicker'] = df_input.head(10)['BBGTicker']
        df_aloc['%AUM'] = 0.1
        return df_aloc

    def performance_portfolio_period(self):
        pass

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

            self._df_sample = self.get_data()
            self._df_predictions = self.make_predictions(self._model, self._df_sample) #predict
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