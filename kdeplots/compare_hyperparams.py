import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse


def plot_kde_from_csvs(files, column, labels, metric_name, hyperparam_name, gen_dir, plot_name, bucket):
    sns.set_theme(style="whitegrid")
    sns.set_context("paper", font_scale=1.25)
    sns.set_palette("muted")

    # Define your colors and configs
    palette = sns.color_palette("muted", len(files))

    plt.figure(figsize=(5, 3))

    with open('../count_stats.json', 'r') as f:
        count_dict = json.load(f)

    for i, file in enumerate(files):
        label = labels[i] if labels else f"File {i+1}"
        df = pd.read_csv(file)

        df = df[df['pdb_id'].isin(count_dict['id_bucket'][bucket])]

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in {file}")

        sns.kdeplot(df[column], bw_adjust=0.5, label=label,
                    linewidth=2, color=palette[i])
        plt.axvline(df[column].mean(), linestyle='--',
                    label=f'Mean of {label}', color=palette[i])
    plt.xlabel(metric_name)
    plt.ylabel("Density")
    # plt.title("Overlapping KDE Plots")
    plt.legend(title=hyperparam_name)
    plt.tight_layout()
    # plt.show()
    plt.savefig(os.path.join(gen_dir, f'{plot_name}-{column}-b{bucket}.pdf'))


files = [
    '../Metrics Generated/metrics-metjob-3.csv',
    '../Metrics Generated/metrics-metjob-11.csv',
    '../Metrics Generated/metrics-metjob-17.csv'
]

for i, file in enumerate(files):
    files[i] = os.path.abspath(file)

labels = [
    '6',
    '24',
    '48'
]

model_name = 'rf2'
plot_name = 'num_rec'
hyperparam_name = 'No. of Recycles'

metrics = [
    {
        'metric': 'lddt',
        'metric_name': 'LDDT',
        'hyperparam_name': hyperparam_name
    },
    {
        'metric': 'rmsd',
        'metric_name': 'RMSD',
        'hyperparam_name': hyperparam_name
    },
    {
        'metric': 'tm_score',
        'metric_name': 'TM-score',
        'hyperparam_name': hyperparam_name
    }
]

gen_dir = os.path.join('./gen', model_name)
os.makedirs(gen_dir, exist_ok=True)


for metric in metrics:
    for bucket in ['20', '30', '40', '50']:
        plot_kde_from_csvs(
            files, metric['metric'], labels, metric['metric_name'], hyperparam_name, gen_dir, plot_name, bucket)
