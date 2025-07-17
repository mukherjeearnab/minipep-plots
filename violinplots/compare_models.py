import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os


def plot_violin_from_csvs(files: list, models: list, column, metric_name, gen_dir):

    with open('../count_stats.json', 'r') as f:
        count_dict = json.load(f)

    # === Step 2: Process each file ===

    for bucket in ['20', '30', '40', '50']:
        sns.set_theme(style="whitegrid")
        sns.set_context("paper", font_scale=1.25)
        sns.set_palette("muted")

        plt.figure(figsize=(5, 3))

        bucket_match = []
        for file, model in zip(files, models):
            df = pd.read_csv(file)
            df = df[df['pdb_id'].isin(
                count_dict['id_bucket'][bucket]
            )]
            col = df[column]  # or set explicitly, e.g., 'values'

            sequence = col.dropna().tolist()

            # Add to master list with file identifier
            bucket_ = int(bucket)
            bucket_match.extend([{
                "model": model,
                "value": v
            } for v in sequence])

        # === Step 3: Create DataFrame for Seaborn ===
        plot_df = pd.DataFrame(bucket_match)

        sns.violinplot(data=plot_df, bw_adjust=0.2, x="model",
                       # options: 'box', 'quartile', 'point', 'stick', None
                       y="value", inner="box",
                       #    cut=0,              # restrict KDE to the observed range
                       linewidth=1.2)

        plt.xlabel("Prediction Model")
        plt.ylabel(metric_name)
        # plt.title("Overlapping KDE Plots")
        # plt.legend(title="Hllo")
        plt.xticks(rotation=15)
        plt.tight_layout()
        # plt.show()
        # exit()
        bucket_range = f'{bucket_-10}-{bucket_-1 if bucket_ < 50 else bucket_}'
        plt.savefig(os.path.join(
            gen_dir, f'bucket_wise_{bucket_range}-{column}.pdf'))


# # === Step 4: Plot Violin Plot ===
# # Set styles
# sns.set_theme(style="whitegrid")
# sns.set_context("paper", font_scale=1.4)
# sns.set_palette("pastel")

# plt.figure(figsize=(10, 6))
# plt.title("Value Distributions Across Files")
# plt.xlabel("CSV File")
# plt.ylabel("Value")
# plt.tight_layout()
# plt.savefig("violin_plot_single_column.png")
# plt.show()


# Start Fill these

files = [
    '../Metrics Generated/metrics-metjob-33.csv',
    '../Metrics Generated/metrics-metjob-20.csv',
    '../Metrics Generated/metrics-metjob-14.csv',
    '../Metrics Generated/metrics-metjob-26.csv',
    '../Metrics Generated/metrics-metjob-35.csv'
]

models = [
    'AlphaFold2',
    'RoseTTAFold2',
    'ESM-Fold',
    'OmegaFold',
    'DMPfold2'
]

metricplot = 'inter-model'
# END Fill these

files = [os.path.abspath(file) for file in files]


metrics = [
    # {
    #     'metric': 'lddt',
    #     'metric_name': 'LDDT',
    # },
    # {
    #     'metric': 'rmsd',
    #     'metric_name': 'RMSD',
    # },
    {
        'metric': 'tm_score',
        'metric_name': 'TM-score',
    },
    {
        'metric': 'gdt_ts',
        'metric_name': 'GDT TS',
    }
]

gen_dir = os.path.join('./gen', metricplot)
os.makedirs(gen_dir, exist_ok=True)


for metric in metrics:
    plot_violin_from_csvs(
        files, models, metric['metric'], metric['metric_name'], gen_dir)
