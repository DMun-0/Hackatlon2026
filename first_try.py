__author__ = "Cache Me if You Can"

"""
I terminalen, kjør requirements.txt for å installere nødvendige biblioteker:
pip install -r requirements.txt

For å kjøre brukermenyen med eksempler på AI prediksjoner, kjør fra main.py


"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split


class politics_predict:

    def __init__(self, df_politics):
        
    pass



class DirectoratePredict:
    
    def __init__(self, emissions: list[240], gases: list[240], years: list[240], emission_sources: list[240]):
        """Initializing"""
        self.emissions: 3 = emissions
        self.gases: 2 = gases
        self.year: 0 = years
        self.year_sorted = sorted(set(years))
        self.emission_sources: 1 = emission_sources
        self.prepare_data()

    def prepare_data(self) -> None:
        plt.figure(figsize=(10, 5))
        for source in sorted(set(self.emission_sources)):
            emissions_per_source: list = []
            for year in self.years_sorted:
                total_emission = sum(
                    self.emissions[i] for i in range(len(self.years)) if self.years[i] == year and self.emission_sources[i] == source
                )
                emissions_per_source.append(total_emission)

            y = [float(i) for i in emissions_per_source]
            x = [int(i) for i in self.years_sorted]
            x = np.array(x).reshape(-1, 1)
            y = np.array(y).reshape(-1, 1)
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=False)
            regressor = LinearRegression().fit(x_train, y_train)
            y_pred = regressor.predict(x_test)

            plt.plot(x_train, y_train, marker="o", linestyle="-", label=f"Train data: {source}")
            plt.plot(x_test, y_pred, marker="x", linestyle="--", label=f"Model predictions: {source}")

        plt.xlabel("Year")
        plt.ylabel("Total emissions (tons CO2-equivalents)")
        plt.title("Predictive analysis: Model and data")
        plt.legend()
        plt.grid(True)
        plt.show()

"""Inspiration from:
- '#27: Scikit-learn 24:Supervised Learning 2: Ordinary Least Squares, LinearRegression' av learndata på YouTube
- Relevant læring fra emnet
- https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html#sphx-glr-auto-examples-linear-model-plot-ols-py
"""
class Met_no_API_predict:
    """Hensikten er å prediktere temperaturen for morgendagen"""
    def __init__(self, df_weather):
        self.df_weather = df_weather
        self.prepare_and_predict_data()
        self.shirt_or_hoodie_tomorrow()
        
    def prepare_and_predict_data(self) -> None:
        self.df_weather['datetime'] = pd.to_datetime(
            '2025-' + self.df_weather['time_formatted'],
            format='%Y-%m-%d %H:%M:%S'
        )

        start_time = self.df_weather['datetime'].min()
        self.df_weather['hours_since_start'] = (
            (self.df_weather['datetime'] - start_time).dt.total_seconds() / 3600
        )
        
        x, y = self.df_weather['hours_since_start'], self.df_weather['air_temperature']
        x = x.values.reshape(-1, 1)
        y = y.values.reshape(-1, 1)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=False)

        regressor = LinearRegression().fit(x_train, y_train)

        y_pred = regressor.predict(x_test)

        fig, ax = plt.subplots(ncols=2, figsize=(10, 5), sharex=True, sharey=True)

        ax[0].scatter(self.df_weather['hours_since_start'][:len(x_train)], y_train, label="Train data points")
        ax[0].plot(self.df_weather['hours_since_start'][:len(x_train)], regressor.predict(x_train),
               linewidth=3, color="tab:orange", label="Model predictions")
        ax[0].set(xlabel="Time", ylabel="Air temperature", title="Train set")
        ax[0].legend()

        ax[1].scatter(self.df_weather['hours_since_start'][len(x_train):], y_test, label="Test data points")
        ax[1].plot(self.df_weather['hours_since_start'][len(x_train):], y_pred,
               linewidth=3, color="tab:orange", label="Model predictions")
        ax[1].set(xlabel="Feature", ylabel="Target", title="Test set")
        ax[1].legend()

        fig.suptitle("Linear Regression")

        plt.show()
        start_next_day = x_test.flatten().min()
        end_next_day = start_next_day + 24

        mask = (x_test.flatten() >= start_next_day) & (x_test.flatten() < end_next_day)
        next_day_predictions = y_pred[mask]
        if next_day_predictions.size == 0:
            print("Error in the code, unfortunately")

        else:
            self.prediction_tomorrow: float = np.mean(next_day_predictions)

    def shirt_or_hoodie_tomorrow(self):
        temperature: float = self.prediction_tomorrow
        threshold: float = float(input("What do you consider warm enough for a t-shirt? "))
        if temperature >= threshold:
            return print("You should wear a t-shirt tomorrow")
        else:
            return print("You should wear extra clothes tomorrow. "
                         "The average will be:", round(temperature, 1), "degrees Celsius")
