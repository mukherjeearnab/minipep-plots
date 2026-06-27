import pandas as pd

with open("./nonstandard-dbamp.txt") as f:
    remove_list = [line.strip() for line in f if line.strip()]

df = pd.read_csv(
    "../Metrics Generated/metrics-metrics-dbamp3-af2-vs-rf2.csv")
df = df[~df["pdb_id"].isin(remove_list)]
df.to_csv(
    "metrics-metrics-dbamp3-af2-vs-rf2.filtered.csv", index=False)
