import sqlite3
import pandas as pd

pd.set_option("expand_frame_repr", False)
df = pd.read_csv("currencies.csv")

# Работа с базой данных
con = sqlite3.connect("currencies.db")
df.to_sql("currencies", con, if_exists="replace", index=False)