from statsmodels.stats.multitest import multipletests
from scipy.stats import wilcoxon
from itertools import combinations
from scipy.stats import friedmanchisquare
import pandas as pd
import json

# af2 = pd.read_csv("../Metrics Generated/metrics-metjob-v2-1.csv")
# rf2 = pd.read_csv("../Metrics Generated/metrics-metjob-v2-2.csv")
# esm = pd.read_csv("../Metrics Generated/metrics-metjob-v2-3.csv")
# omf = pd.read_csv("../Metrics Generated/metrics-metjob-v2-4.csv")
# dmp = pd.read_csv("../Metrics Generated/metrics-metjob-v2-5.csv")

# df = af2.merge(esm, on="Peptide", suffixes=("_AF2", "_ESM"))


files = {
    "af2": "../Metrics Generated/metrics-metjob-v2-1.csv",
    "rf2": "../Metrics Generated/metrics-metjob-v2-2.csv",
    "esm": "../Metrics Generated/metrics-metjob-v2-3.csv",
    "omf": "../Metrics Generated/metrics-metjob-v2-4.csv",
    "dmp": "../Metrics Generated/metrics-metjob-v2-5.csv",

}

# Column used to match peptides
id_column = "pdb_id_frame"


# Metrics to compare
metrics = [
    "rmsd",
    "tm_score",
    "gdt_ts",
    "lddt",
    "native_contract"
]


# dfs = {}

# for name, file in files.items():
#     df = pd.read_csv(file)
#     df['pdb_id_frame'] = df['pdb_id'] + '_' + df['nmr_frame']
#     dfs[name] = df


# merged = dfs["AF2"][["pdb_id_frame", "tm_score"]].rename(
#     columns={"tm_score": "AF2"})

# for model in list(files.keys())[1:]:
#     merged = merged.merge(
#         dfs[model][["pdb_id_frame", "tm_score"]].rename(
#             columns={"tm_score": model}),
#         on="pdb_id_frame"
#     )

with open('../ss_clusters-alt.json', 'r') as f:
    count_dict = json.load(f)

    print(count_dict.keys())

for group, ids in count_dict.items():

    for metric in metrics:

        # Merge all models for this metric
        merged = None

        dfs = dict()

        for model, filename in files.items():
            df = pd.read_csv(filename)

            # Sort to ensure identical ordering
            df = df[df['pdb_id'].isin(ids)]

            df['nmr_frame'] = df['nmr_frame'].astype(str)
            df['pdb_id_frame'] = df['pdb_id'] + '_' + df['nmr_frame']
            df = df.sort_values("pdb_id_frame").reset_index(drop=True)

            dfs[model] = df

        for model, df in dfs.items():

            temp = df[[id_column, metric]].rename(columns={metric: model})

            if merged is None:
                merged = temp
            else:
                merged = merged.merge(temp, on=id_column)

        results = []

        models = list(files.keys())

        for model1, model2 in combinations(models, 2):

            x = merged[model1]
            y = merged[model2]

            # Remove missing values pairwise
            mask = ~(x.isna() | y.isna())

            x = x[mask]
            y = y[mask]

            try:
                stat, p = wilcoxon(x, y)

            except ValueError:
                # Happens if every difference is zero
                stat = 0
                p = 1.0

            results.append({
                "Model 1": model1,
                "Model 2": model2,
                "Metric": metric,
                "N": len(x),
                "Wilcoxon W": stat,
                "Raw p-value": p
            })

        # Holm correction
        raw_p = [r["Raw p-value"] for r in results]

        corrected = multipletests(
            raw_p,
            method="holm"
        )[1]

        for r, p_adj in zip(results, corrected):
            r["Holm adjusted p"] = p_adj

        out = pd.DataFrame(results)

        out.to_csv(
            f"./gen/Pairwise_Wilcoxon_{metric}-b{group}.csv", index=False)

        print(f"Saved Pairwise_Wilcoxon_{metric}.csv")

print("\nDone.")
