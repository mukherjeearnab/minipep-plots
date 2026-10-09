import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

###############################################################################
# CONFIGURATION
###############################################################################

metrics = ["gdt_ts", 'tm_score', 'rmsd']

idx_ll = []
idx_ms = ['20', '30', '40', '50',
          'alpha-helix-rich', 'beta-sheet-rich', 'disordered', 'mixed']
for metric in metrics:
    for idxm in idx_ms:

        csv_file = f"./gen/Pairwise_Wilcoxon_{metric}-b{idxm}.csv"

        # Choose either:
        # "Raw p-value"
        # "Holm adjusted p"

        value_column = "Holm adjusted p"

        ###############################################################################
        # LOAD
        ###############################################################################

        df = pd.read_csv(csv_file)

        df['Model 1'] = df['Model 1'].str.upper()
        df['Model 2'] = df['Model 2'].str.upper()

        models = sorted(
            list(set(df["Model 1"]).union(set(df["Model 2"])))
        )

        # models = [model.upper() for model in models]

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

        plt.figure(figsize=(4, 3))

        sns.heatmap(
            heatmap,
            annot=True,
            fmt=".3g",
            cmap="viridis_r",
            linewidths=0.5,
            square=True,
            cbar_kws={"label":
                      r'$-\log_{10}(p\mathrm{-value})$'}
        )

        # plt.title(f"{metric} Pairwise Wilcoxon Test for bucket {idxm}")

        plt.tight_layout()

        plt.savefig(f"./gen/{metric}_Wilcoxon_heatmap_b{idxm}.png", dpi=300)
        plt.close()

        # plt.show()
