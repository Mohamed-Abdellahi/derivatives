# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
## i will defintely put each class in a file.. 
## but i guess for now, i will try to make a first viable product 


import numpy as np
from scipy.stats import norm

class Option:
    def __init__(self, option_type, strike, spot, volatility, risk_free_rate, expiry, dividend=0, position=1):
        self.option_type = option_type
        self.strike = strike
        self.spot = spot
        self.volatility = volatility
        self.risk_free_rate = risk_free_rate
        self.expiry = expiry
        self.dividend = dividend
        self.position = position  # 1 pour long, -1 pour short

    def _calculate_d1_d2(self, spot, volatility, expiry):
        d1 = (np.log(spot / self.strike) + (self.risk_free_rate - self.dividend + 0.5 * volatility ** 2) * expiry) / (volatility * np.sqrt(expiry))
        d2 = d1 - volatility * np.sqrt(expiry)
        return d1, d2

    def black_scholes_price(self, spot=None, volatility=None, expiry=None):
        spot = spot if spot is not None else self.spot
        volatility = volatility if volatility is not None else self.volatility
        expiry = expiry if expiry is not None else self.expiry
        d1, d2 = self._calculate_d1_d2(spot, volatility, expiry)
        if self.option_type == 'call':
            price = spot * np.exp(-self.dividend * expiry) * norm.cdf(d1) - self.strike * np.exp(-self.risk_free_rate * expiry) * norm.cdf(d2)
        elif self.option_type == 'put':
            price = self.strike * np.exp(-self.risk_free_rate * expiry) * norm.cdf(-d2) - spot * np.exp(-self.dividend * expiry) * norm.cdf(-d1)
        else:
            raise ValueError("Option type must be 'call' or 'put'")
        return price * self.position

    def delta(self, spot=None, volatility=None, expiry=None):
        spot = spot if spot is not None else self.spot
        volatility = volatility if volatility is not None else self.volatility
        expiry = expiry if expiry is not None else self.expiry
        d1, _ = self._calculate_d1_d2(spot, volatility, expiry)
        if self.option_type == 'call':
            return np.exp(-self.dividend * expiry) * norm.cdf(d1) * self.position
        elif self.option_type == 'put':
            return np.exp(-self.dividend * expiry) * (norm.cdf(d1) - 1) * self.position

    def gamma(self, spot=None, volatility=None, expiry=None):
        spot = spot if spot is not None else self.spot
        volatility = volatility if volatility is not None else self.volatility
        expiry = expiry if expiry is not None else self.expiry
        d1, _ = self._calculate_d1_d2(spot, volatility, expiry)
        return np.exp(-self.dividend * expiry) * norm.pdf(d1) / (spot * volatility * np.sqrt(expiry)) * self.position

    def vega(self, spot=None, volatility=None, expiry=None):
        spot = spot if spot is not None else self.spot
        volatility = volatility if volatility is not None else self.volatility
        expiry = expiry if expiry is not None else self.expiry
        d1, _ = self._calculate_d1_d2(spot, volatility, expiry)
        return spot * np.exp(-self.dividend * expiry) * norm.pdf(d1) * np.sqrt(expiry) * self.position

    def theta(self, spot=None, volatility=None, expiry=None):
        spot = spot if spot is not None else self.spot
        volatility = volatility if volatility is not None else self.volatility
        expiry = expiry if expiry is not None else self.expiry
        d1, d2 = self._calculate_d1_d2(spot, volatility, expiry)
        if self.option_type == 'call':
            theta = -(spot * norm.pdf(d1) * volatility / (2 * np.sqrt(expiry))) - self.risk_free_rate * self.strike * np.exp(-self.risk_free_rate * expiry) * norm.cdf(d2) + self.dividend * spot * np.exp(-self.dividend * expiry) * norm.cdf(d1)
        elif self.option_type == 'put':
            theta = -(spot * norm.pdf(d1) * volatility / (2 * np.sqrt(expiry))) + self.risk_free_rate * self.strike * np.exp(-self.risk_free_rate * expiry) * norm.cdf(-d2) - self.dividend * spot * np.exp(-self.dividend * expiry) * norm.cdf(-d1)
        return theta * self.position

    def rho(self, spot=None, volatility=None, expiry=None):
        spot = spot if spot is not None else self.spot
        volatility = volatility if volatility is not None else self.volatility
        expiry = expiry if expiry is not None else self.expiry
        d1, d2 = self._calculate_d1_d2(spot, volatility, expiry)
        if self.option_type == 'call':
            return self.strike * expiry * np.exp(-self.risk_free_rate * expiry) * norm.cdf(d2) * self.position
        elif self.option_type == 'put':
            return -self.strike * expiry * np.exp(-self.risk_free_rate * expiry) * norm.cdf(-d2) * self.position

    def vanna(self, spot=None, volatility=None, expiry=None):
        spot = spot if spot is not None else self.spot
        volatility = volatility if volatility is not None else self.volatility
        expiry = expiry if expiry is not None else self.expiry
        d1, d2 = self._calculate_d1_d2(spot, volatility, expiry)
        return -np.exp(-self.dividend * expiry) * norm.pdf(d1) * d2 / volatility * self.position

    def volga(self, spot=None, volatility=None, expiry=None):
        spot = spot if spot is not None else self.spot
        volatility = volatility if volatility is not None else self.volatility
        expiry = expiry if expiry is not None else self.expiry
        d1, d2 = self._calculate_d1_d2(spot, volatility, expiry)
        return spot * np.exp(-self.dividend * expiry) * norm.pdf(d1) * np.sqrt(expiry) * d1 * d2 / volatility * self.position
