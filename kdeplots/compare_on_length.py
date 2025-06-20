import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse



def plot_kde_from_csvs(buckets, column, labels, metric_name, hyperparam_name):
    sns.set_theme(style="whitegrid")
    sns.set_context("paper", font_scale=1.25)
    sns.set_palette("muted")

    plt.figure(figsize=(5, 3))

    for i, bucket in enumerate(buckets):
        label = labels[i] if labels else f"File {i+1}"
        df = bucket

        sns.kdeplot(df[column], bw_adjust=0.5, label=label, linewidth=2)

    plt.xlabel(metric_name)
    plt.ylabel("Density")
    # plt.title("Overlapping KDE Plots")
    plt.legend(title=hyperparam_name)
    plt.tight_layout()
    plt.show()

df = pd.read_csv('../Metrics Generated/metrics-metjob-15.csv')

with open('../count_stats.json', 'r') as f:
    count_dict = json.load(f)

buckets = [
    df[df['pdb_id'].isin(count_dict['id_bucket']['20'])],
    df[df['pdb_id'].isin(count_dict['id_bucket']['30'])],
    df[df['pdb_id'].isin(count_dict['id_bucket']['40'])],
    df[df['pdb_id'].isin(count_dict['id_bucket']['50'])]
]

labels = [
    '< 20',
    '< 30',
    '< 40',
    '< 50'
]

metric = 'rmsd'
metric_name = 'RMSD'
hyperparam_name = 'Sequence Length'

plot_kde_from_csvs(buckets, metric, labels, metric_name, hyperparam_name)
