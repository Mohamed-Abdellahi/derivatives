# %%
from option import Option
from book import BookEurostoxx50
import matplotlib.pyplot as plt

# Création des options
option_type_call = "call"
option_type_put = "put"
strike_call = 90
strike_put = 90  # ATM
spot_price = 100
volatility = 0.2
risk_free_rate = 0.05
expiry = 0.25  # 3 mois

dividend = 0.02

# Straddle Strategy
call_option = Option(option_type=option_type_call, strike=strike_call, spot=spot_price, volatility=volatility, risk_free_rate=risk_free_rate, expiry=expiry, dividend=dividend, position=1)
put_option = Option(option_type=option_type_put, strike=strike_put, spot=spot_price, volatility=volatility, risk_free_rate=risk_free_rate, expiry=expiry, dividend=dividend)

# Création du portefeuille
book = BookEurostoxx50()
book.add_option(call_option)
book.add_option(put_option)

# S
#stock_simulation_df = book.simulate_stock(spot_price=spot_price, volatility=volatility, risk_free_rate=risk_free_rate, dividend=dividend, num_steps=252, total_time=0.25)

stock_simulation_df = book.simulate_stock_brownian(spot_price=spot_price, volatility=volatility, risk_free_rate=risk_free_rate, dividend=dividend, num_steps=252, total_time=0.25)

# %%
# Simulation des options
call_simulation_df = book.simulate_option(call_option, stock_simulation_df)
put_simulation_df = book.simulate_option(put_option, stock_simulation_df)
aggregated_df = book.aggregate_portfolio_results()
# %%
call_simulation_df
# %%
def plot_all_greeks(df, axis):
    columns_to_plot = ['Stock Price','Delta', 'Gamma', 'Vega', 'Theta', 'Rho', 'Volga', 'Vanna', 'Theoretical Price']
    num_plots = len(columns_to_plot)

    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(16, 8))  # 2 lignes, 4 colonnes
    axes = axes.flatten()

    for i, col in enumerate(columns_to_plot):
        axes[i].plot(df[axis], df[col], label=col, color="blue")
        axes[i].set_xlabel(axis)
        axes[i].set_ylabel(col)
        axes[i].set_title(f"Evolution of the {col}")
        axes[i].legend()
        axes[i].grid()

        # Ajuster dynamiquement les limites de l'axe X
        axes[i].set_xlim([df[axis].min(), df[axis].max()])
        
        # Ajuster les ticks de l'axe X pour plus de lisibilité
        axes[i].tick_params(axis='x', rotation=45)
    plt.tight_layout()
    plt.show()

# Affichage des résultats
plot_all_greeks(aggregated_df, "Date")


# %%
