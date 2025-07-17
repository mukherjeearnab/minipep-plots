import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os


def plot_violin_from_csv(file, column, metric_name, gen_dir):
    sns.set_theme(style="whitegrid")
    sns.set_context("paper", font_scale=1.25)
    sns.set_palette("muted")

    plt.figure(figsize=(5, 3))

    with open('../count_stats.json', 'r') as f:
        count_dict = json.load(f)

    # === Step 2: Process each file ===
    all_matches = []

    for bucket in ['20', '30', '40', '50']:
        df = pd.read_csv(file)
        df = df[df['pdb_id'].isin(count_dict['id_bucket'][bucket])]
        col = df[column]  # or set explicitly, e.g., 'values'

        sequence = col.dropna().tolist()

        # Add to master list with file identifier
        bucket = int(bucket)
        all_matches.extend([{
            "bucket": f'{bucket-10}-{bucket-1 if bucket < 50 else bucket}',
            "value": v
        } for v in sequence])

    # === Step 3: Create DataFrame for Seaborn ===
    plot_df = pd.DataFrame(all_matches)

    sns.violinplot(data=plot_df, bw_adjust=0.2, x="bucket",
                   # options: 'box', 'quartile', 'point', 'stick', None
                   y="value", inner="box",
                   #    cut=0,              # restrict KDE to the observed range
                   linewidth=1.2)

    plt.xlabel("Sequence Lengths")
    plt.ylabel(metric_name)
    # plt.title("Overlapping KDE Plots")
    # plt.legend(title="Hllo")
    # plt.xticks(rotation=45)
    plt.tight_layout()
    # plt.show()
    # exit()
    plt.savefig(os.path.join(gen_dir, f'bucket_wise-{column}.pdf'))


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

file = '../Metrics Generated/metrics-metjob-35.csv'
file = os.path.abspath(file)

model_name = 'dmp-best'
# END Fill these

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

gen_dir = os.path.join('./gen', model_name)
os.makedirs(gen_dir, exist_ok=True)


for metric in metrics:
    plot_violin_from_csv(
        file, metric['metric'], metric['metric_name'], gen_dir)
