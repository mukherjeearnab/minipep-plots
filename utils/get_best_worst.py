import json
import pandas as pd

with open('../ss_clusters-alt.json', 'r') as f:
    ss_clusters = json.load(f)

af2 = pd.read_csv('../Metrics Generated/per-residue-rmsd-job-af2-9.csv')
rf2 = pd.read_csv('../Metrics Generated/per-residue-rmsd-job-rf2-7.csv')
esm = pd.read_csv('../Metrics Generated/per-residue-rmsd-job-esm-4.csv')
omf = pd.read_csv('../Metrics Generated/per-residue-rmsd-job-omf-6.csv')
dmp = pd.read_csv('../Metrics Generated/per-residue-rmsd-job-dmp-5.csv')


for cluster, target_strings in ss_clusters.items():

    csv_files = [
        '../Metrics Generated/per-residue-rmsd-job-af2-9.csv',
        '../Metrics Generated/per-residue-rmsd-job-rf2-7.csv',
        '../Metrics Generated/per-residue-rmsd-job-esm-4.csv',
        '../Metrics Generated/per-residue-rmsd-job-omf-6.csv',
        '../Metrics Generated/per-residue-rmsd-job-dmp-5.csv'
    ]

    top10_sets = []

    for file in csv_files:
        df = pd.read_csv(file)

        df = df[df['per_res_ca_rmsd_A'] < 0.5]

        # print(df.head()``)

        top10 = (
            df[df["pdb_id"].isin(target_strings)]
            .sort_values("per_res_ca_rmsd_A", ascending=False)  # or True
            .head(250)
        )

        # print(top10)

        top10_sets.append(set(top10["pdb_id"]))

    # Common values present in top 10 of every CSV
    common_values = set.intersection(*top10_sets)

    print(cluster)
    print(common_values)
