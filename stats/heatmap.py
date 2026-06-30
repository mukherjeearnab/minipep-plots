import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

###############################################################################
# CONFIGURATION
###############################################################################

metric = "RMSD"

idxm = 20
csv_file = f"./gen/Pairwise_Wilcoxon_rmsd-b{idxm}.csv"

# Choose either:
# "Raw p-value"
# "Holm adjusted p"

value_column = "Holm adjusted p"

###############################################################################
# LOAD
###############################################################################

df = pd.read_csv(csv_file)

models = sorted(
    list(set(df["Model 1"]).union(set(df["Model 2"])))
)

heatmap = pd.DataFrame(
    np.ones((len(models), len(models))),
    index=models,
    columns=models
)

###############################################################################
# FILL MATRIX
###############################################################################

for _, row in df.iterrows():

    m1 = row["Model 1"]
    m2 = row["Model 2"]

    p = row[value_column]

    # heatmap.loc[m1, m2] = p
    # heatmap.loc[m2, m1] = p

    heatmap.loc[m1, m2] = -np.log10(max(p, 1e-320))
    heatmap.loc[m2, m1] = -np.log10(max(p, 1e-320))

###############################################################################
# PLOT
###############################################################################

plt.figure(figsize=(8, 7))

sns.heatmap(
    heatmap,
    annot=True,
    fmt=".3g",
    cmap="viridis_r",
    linewidths=0.5,
    square=True,
    cbar_kws={"label": "Adjusted p-value"}
)


plt.title(f"{metric} Pairwise Wilcoxon Test for bucket {idxm}")

plt.tight_layout()

plt.savefig(f"./gen/{metric}_Wilcoxon_heatmap_b{idxm}.png", dpi=300)

# plt.show()
