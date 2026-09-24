"""Assignment 1: Market Basket Analysis (Apriori) on real-world data.
Dataset: UCI 'Online Retail' (https://archive.ics.uci.edu/dataset/352/online+retail)
  or any transactions CSV with columns InvoiceNo, Description, Quantity.
Install: pip install pandas mlxtend openpyxl
Usage:   python assignment1_market_basket.py Online_Retail.xlsx
"""
import sys
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

path = sys.argv[1] if len(sys.argv) > 1 else "Online_Retail.xlsx"
df = pd.read_excel(path) if path.endswith(("xlsx", "xls")) else pd.read_csv(path)

# ---- clean ----
df["Description"] = df["Description"].str.strip()
df = df.dropna(subset=["InvoiceNo", "Description"])
df["InvoiceNo"] = df["InvoiceNo"].astype(str)
df = df[~df["InvoiceNo"].str.startswith("C")]      # remove cancellations
df = df[df["Quantity"] > 0]
df = df[df["Country"] == "France"] if "Country" in df else df  # smaller subset

# ---- basket matrix (invoice x product, True/False) ----
basket = (df.groupby(["InvoiceNo", "Description"])["Quantity"].sum()
            .unstack(fill_value=0) > 0)

# ---- frequent itemsets + rules ----
itemsets = apriori(basket, min_support=0.07, use_colnames=True)
rules = association_rules(itemsets, metric="lift", min_threshold=1)
rules = rules[(rules["confidence"] >= 0.5) & (rules["lift"] >= 1.5)]
rules = rules.sort_values("lift", ascending=False)

pd.set_option("display.width", 200)
print(rules[["antecedents", "consequents", "support", "confidence", "lift"]].head(15))
rules.to_csv("association_rules.csv", index=False)
