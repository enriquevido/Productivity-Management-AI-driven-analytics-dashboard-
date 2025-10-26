
import pandas as pd
from pathlib import Path
import numpy as np

DATA = Path(__file__).resolve().parent / "data"

def load_data():
    sessions = pd.read_csv(DATA / "sessions.csv")
    employees = pd.read_csv(DATA / "employees.csv")
    sites = pd.read_csv(DATA / "sites.csv")
    versions = pd.read_csv(DATA / "model_versions.csv")
    users = pd.read_csv(DATA / "users.csv")
    return sessions, employees, sites, versions, users

PRIMARY = "#000164"
WHITE = "#FFFFFF"

def efficiency(df):
    return (df["EBT_min"] / df["ABT_min"]).mean()

def accuracy(df):
    return (df.assign(err=(df["ABT_min"]-df["EBT_min"]).abs())["err"] <= 0.5).mean()

def bias_seconds(df):
    return (df["ABT_min"] - df["EBT_min"]).mean() * 60.0

def learning_trend(versions):
    return versions["accuracy"].iloc[-1] - versions["accuracy"].iloc[0]

def kpi_table(df):
    return pd.DataFrame({
        "Accuracy (%)":[round(accuracy(df)*100,1)],
        "Efficiency Score":[round(efficiency(df),2)],
        "MAE (s)":[round((df['ABT_min']-df['EBT_min']).abs().mean()*60.0,1)],
        "Benchmark Index":[round(df['EBT_min'].mean()/df['ABT_min'].mean(),2)],
        "Bias (s)":[round(bias_seconds(df),1)]
    })
