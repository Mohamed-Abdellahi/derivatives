# author: MOHAMED-ABDELLAHI, Mohamed-Abdellahi
# date: 2022-02-12
# description: The main idea is to model a trading book of derivative

import numpy as np
import pandas as pd
from option import Option  

class BookEurostoxx50:
    def __init__(self):
        self.options = []
        self.stock_position = 0  # Position sur le sous-jacent 
        self.stock_simulation_data = None  # Données de simulation du stock
        self.book = {}  # Dictionnaire pour stocker les résultats de simulation pour chaque option

    def add_option(self, option):
        self.options.append(option)

    def add_stock_position(self, quantity):
        self.stock_position += quantity

    def simulate_stock_brownian(self, spot_price, volatility, risk_free_rate, dividend, num_steps, total_time, seed= None):
       
        """
        Simulates stock price using Geometric Brownian Motion.

        Parameters:
        - spot_price (float): Initial stock price.
        - volatility (float): Annualized volatility.
        - risk_free_rate (float): Risk-free interest rate.
        - dividend (float): Dividend yield.
        - num_steps (int): Number of simulation steps.
        - total_time (float): Total simulation time (in years).
        - seed (int, optional): Random seed for reproducibility.

        Returns:
        - DataFrame with simulated stock prices over time.
        """
        if seed is not None:
            np.random.seed(seed)  # Set the random seed

        dt = total_time / num_steps
        prices = [spot_price]
        times = [0]
        

        for t in range(1, num_steps):
            dW = np.random.normal(0, np.sqrt(dt))
            next_price = prices[-1] * np.exp((risk_free_rate - dividend - 0.5 * volatility ** 2) * dt + volatility * dW)
            prices.append(next_price)
            times.append(times[-1] + dt)

        # Création de la table de simulation du stock
        stock_simulation_df = pd.DataFrame({
            'Date': times,
            'Stock Price': prices,
            'Volatility': volatility,
            'Rate': risk_free_rate,
            'Dividend': dividend
        })

        self.stock_simulation_data = stock_simulation_df
        return stock_simulation_df


    def simulate_spot(self, spot_price, volatility, risk_free_rate, dividend, num_steps, total_time):
        prices = np.arange(0, 201, 1)  # Prix de 0 à 200
        times = np.zeros_like(prices)  # Temps fixe
        
        stock_simulation_df = pd.DataFrame({
            'Date': times,
            'Stock Price': prices,
            'Volatility': volatility,
            'Rate': risk_free_rate,
            'Dividend': dividend
        })
        
        self.stock_simulation_data = stock_simulation_df
        return stock_simulation_df

    def simulate_option(self, option, stock_simulation_df):
        option_simulation_data = []

        for index, row in stock_simulation_df.iterrows():
            time_to_maturity = option.expiry - row['Date']
            if time_to_maturity > 0:
                option_data = {
                    'Date': row['Date'],
                    'Time to Maturity': time_to_maturity,
                    'Stock Price': row['Stock Price'],
                    'Volatility': row['Volatility'],
                    'Rate': row['Rate'],
                    'Delta': option.delta(spot=row['Stock Price'], volatility=row['Volatility'], expiry=time_to_maturity),
                    'Gamma': option.gamma(spot=row['Stock Price'], volatility=row['Volatility'], expiry=time_to_maturity),
                    'Vega': option.vega(spot=row['Stock Price'], volatility=row['Volatility'], expiry=time_to_maturity),
                    'Theta': option.theta(spot=row['Stock Price'], volatility=row['Volatility'], expiry=time_to_maturity),
                    'Rho': option.rho(spot=row['Stock Price'], volatility=row['Volatility'], expiry=time_to_maturity),
                    'Volga': option.volga(spot=row['Stock Price'], volatility=row['Volatility'], expiry=time_to_maturity),
                    'Vanna': option.vanna(spot=row['Stock Price'], volatility=row['Volatility'], expiry=time_to_maturity),
                    'Theoretical Price': option.black_scholes_price(spot=row['Stock Price'], volatility=row['Volatility'], expiry=time_to_maturity)
                }
                option_simulation_data.append(option_data)

        option_simulation_df = pd.DataFrame(option_simulation_data)
        self.book[option] = option_simulation_df
        return option_simulation_df

    def aggregate_portfolio_results(self):
        if not self.book:
            return pd.DataFrame()

        first_option = next(iter(self.book))
        aggregated_df = self.book[first_option].copy()
        aggregated_df.iloc[:, 4:] = 0

        for option, df in self.book.items():
            for col in df.columns[4:]:
                aggregated_df[col] += df[col]

        self.book['Aggregated'] = aggregated_df
        return aggregated_df
