"""
    @author: Matheus José Oliveira dos Santos
    Last Edit: 20/06/2023 by Matheus José Oliveira dos Santos
"""

import pandas as pd
import numpy as np

def calculate_drawdown_hist(df:pd.DataFrame) -> pd.DataFrame: #funcionando conforme esperado
    df_drawdown = df.copy()
    df_cummax = df.iloc[:, 1:].cummax()
    df_drawdown.iloc[:,1:] = df.iloc[:, 1:] / df_cummax - 1

    return df_drawdown

def calculate_max_drawdown(df: pd.DataFrame) -> float: #funcionando conforme esperado
    df_drawdown = calculate_drawdown_hist(df)
    max_drawdown = np.min(df_drawdown.iloc[:, 1:])

    return max_drawdown

def calculate_annualized_return(df: pd.DataFrame, period:int = 252) -> float: #funcionando conforme esperado (um ativo de cada vez)
    total_return = df.iloc[-1, 1:].prod() - 1
    num_years = len(df) / period
    annualized_return = (1 + total_return) ** (1 / num_years) - 1

    return annualized_return

def calculate_annual_returns(df:pd.DataFrame) -> pd.DataFrame: #funcionando conforme esperado
    df=df.copy()
    # Extract year from the date column
    df['year'] = pd.to_datetime(df.iloc[:,0]).dt.year
    df_aux = df['year'].unique().copy()

    # Create a new dataframe to store the annual returns
    df_annual_returns = pd.DataFrame(columns=['year'])
    unique_tickers = df.columns[1:-1]  # Exclude the 'Date' and 'Year' columns
    
    # Calculate annual returns for each ticker
    for ticker in unique_tickers:
        yearly_returns = []
        for year in df['year'].unique():
            year_data = df[df['year'] == year]
            annual_return = (year_data[ticker].iloc[-1] - year_data[ticker].iloc[0]) / year_data[ticker].iloc[0]
            yearly_returns.append(annual_return)
        df_annual_returns[ticker] = yearly_returns
    
    df_annual_returns['year'] = df_aux
    
    return df_annual_returns

def calculate_moving_volatility(df:pd.DataFrame, period:int = 252, window_size:int = 20) -> pd.DataFrame():

    df = df.copy()
    df_returns = df.iloc[:, 1:] / df.iloc[:, 1:].shift(1)-1
    df_volatility = df_returns.rolling(window=window_size).std() * np.sqrt(period)
    df_volatility = df_volatility.dropna()
    df_volatility.insert(0, "Date", df.iloc[:, 0])

    return df_volatility

def calculate_volatility(df:pd.DataFrame, period:int = 252) -> pd.DataFrame():
    df = df.copy()
    df_returns = df.iloc[:, 1:] / df.iloc[:, 1:].shift(1)-1
    df_volatility = df_returns.std() * np.sqrt(period)

    return df_volatility

def calculate_sharpe_ratio(df:pd.DataFrame, risk_free_rate_annualized:float = 0, period:int = 252) -> pd.DataFrame(): #testar com diferentes tickers
    df = df.copy()
    df_returns = df.iloc[:, 1:] / df.iloc[:, 1:].shift(1)-1
    annualized_returns = df_returns.mean() * period

    excess_returns = annualized_returns - risk_free_rate_annualized
    volatility = df_returns.std() * np.sqrt(period)

    sharpe_ratio = excess_returns / volatility

    df_sharpe = pd.DataFrame({'Ticker': df.columns[1:], 'Sharpe Ratio': sharpe_ratio}).reset_index(drop=True)

    return df_sharpe

def calculate_calmar_ratio(df:pd.DataFrame, risk_free_rate_annualized:float = 0, period:int = 252) -> pd.DataFrame(): #testar com diferentes tickers
    df = df.copy()
    df_returns = df.iloc[:, 1:] / df.iloc[:, 1:].shift(1)-1
    annualized_returns = df_returns.mean() * period
    excess_returns = annualized_returns - risk_free_rate_annualized
    max_drawdown = calculate_max_drawdown(df)
    calmar_ratio = -excess_returns / max_drawdown

    df_calmar = pd.DataFrame({'Ticker': df.columns[1:], 'Calmar Ratio': calmar_ratio}).reset_index(drop=True)

    return df_calmar

def calculate_skewness(df:pd.DataFrame) -> pd.DataFrame():
    df = df.copy()
    df_returns = df.iloc[:, 1:] / df.iloc[:, 1:].shift(1)-1 # lim x->0 log (x) = x-1
    df_skewness = df_returns.skew()

    return df_skewness

def calculate_kurtosis():
    return

def calculate_beta():
    return

def calculate_alpha():
    return

def calculate_value_at_risk():
    return