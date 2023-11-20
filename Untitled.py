# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
from matplotlib import pyplot as plt
from datetime import datetime
df = pd.read_csv ('crimes-chicago-dataset.csv')
df['Date'] = pd.to_datetime(df['Date'])
def get_season(date):
    month = date.month
    if 3 <= month <= 5:
        return "Frühling"
    elif 6 <= month <= 8:
        return "Sommer"
    elif 9 <= month <= 11:
        return "Herbst"
    else:
        return "Winter"
    
df['Jahreszeit'] = df['Date'].apply(get_season)

grouped_df = df.groupby('Jahreszeit')['Case Number'].size()

plt.bar(grouped_df.index, grouped_df.values, color=['green', 'orange', 'red', 'blue'])
plt.title('Balkendiagramm nach Jahreszeiten')
plt.xlabel('Jahreszeit')
plt.ylabel('Summe der Werte')
plt.show()

# %%
