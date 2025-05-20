import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

@st.cache_data
def load_data():
    df_benin = pd.read_csv('data/benin-malanville_clean.csv')
    df_sierra = pd.read_csv('data/sierraleone-bumbuna_clean.csv')
    df_togo = pd.read_csv('data/togo-bumbuna_clean.csv')

    df_benin["Country"] = "Benin"
    df_sierra["Country"] = "Sierra Leone"
    df_togo["Country"] = "Togo"

    return pd.concat([df_benin, df_sierra, df_togo], ignore_index=True)

def filter_data(df, selected_countries):
    return df[df["Country"].isin(selected_countries)]

def get_summary_table(df):
    return df.groupby("Country")[["GHI", "DNI", "DHI"]].agg(["mean", "median", "std"]).round(2)
