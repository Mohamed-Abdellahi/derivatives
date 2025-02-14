# Simulation d'un Portefeuille d'Options

Ce projet implémente une **simulation de trading d'options** en utilisant le modèle de **Black-Scholes**.  
Il permet de :
- **Créer des options** (`Option`).
- **Ajouter ces options dans un portefeuille** (`BookEurostoxx50`).
- **Simuler l'évolution du sous-jacent** et des options.
- **Agréger et afficher les Greeks** d'une stratégie.

## 📌 Utilisation du Code

### 1️⃣ Créer une option
```python
from option import Option

call_option = Option("call", strike=100, spot=100, volatility=0.2, 
                     risk_free_rate=0.05, expiry=0.25, dividend=0)
```

### 2️⃣ Ajouter les options à un book
```python
from book import BookEurostoxx50

book = BookEurostoxx50()
book.add_option(call_option)
```

### 3️⃣ Simuler l'évolution du sous-jacent et des options
```python
stock_simulation_df = book.simulate_stock(spot_price=100, volatility=0.2, 
                                          risk_free_rate=0.05, dividend=0, 
                                          num_steps=252, total_time=0.25)

call_simulation_df = book.simulate_option(call_option, stock_simulation_df)
```

### 4️⃣ Agréger et visualiser les Greeks
```python
aggregated_df = book.aggregate_portfolio_results()
plot_all_greeks(aggregated_df, "Date")
```

## 📊 Résultats et Visualisation
Une fois exécuté, le code génère :
- Un **tableau de simulation** des options au fil du temps.
- Des **graphes des Greeks** pour analyser la sensibilité du portefeuille.

---

✍ **Auteur:** Mohamed-Abdellahi Mohamed-Abdellahi  
🚀 **Dernière mise à jour:** `2025-02-14`
