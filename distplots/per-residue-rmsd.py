import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def plot_violin_from_csv(file, gen_dir):

    with open('../count_stats.json', 'r') as f:
        count_dict = json.load(f)

    for bucket in ['20', '30', '40', '50']:
        sns.set_theme(style="whitegrid")
        sns.set_context("paper", font_scale=1.25)
        sns.set_palette("muted")

        plt.figure(figsize=(5, 3))

        df = pd.read_csv(file)

        df = df[df['pdb_id'].isin(count_dict['id_bucket'][bucket])]

        # --- Compute statistics ---

        # Add to master list with file identifier
        bucket = int(bucket)

        data = df['per_res_ca_rmsd_A'].dropna()

        mean = data.mean()
        median = data.median()
        std = data.std()

        ax = sns.histplot(data, kde=True,
                          # <-- increase this to smooth the KDE)
                          stat="count", bins='auto', kde_kws={'bw_adjust': 1.0})

        # --- Add vertical lines ---
        plt.axvline(mean, color='red', linestyle='-',
                    linewidth=1.2, label=f'Mean = {mean:.2f}')
        plt.axvline(median, color='green', linestyle='--',
                    linewidth=1.2, label=f'Median = {median:.2f}')

        # Standard deviations (1σ, 2σ, 3σ)
        for i in range(1, 4):
            plt.axvline(mean + i*std, color='orange', linestyle=':',
                        linewidth=1.2, label=f'+{i}σ = {(mean + i*std):.2f}')
            # plt.axvline(mean - i*std, color='orange', linestyle=':',
            #             linewidth=1.5, label=f'-{i}σ')

        ax.set_yticklabels([])

        plt.xlim(left=0, right=mean + i*std + 0.1)
        # plt.title('Distribution with Mean, Median, and Standard Deviations')
        plt.ylabel('Number of Comparisons')
        plt.xlabel('Per-residue cα RMSD (Å)')
        plt.legend(loc='upper right')
        plt.tight_layout()

        # plt.xlabel("Sequence Lengths")
        # plt.ylabel(metric_name)
        # plt.title("Overlapping KDE Plots")
        # plt.legend(title="Hllo")
        # plt.xticks(rotation=45)
        plt.tight_layout()
        # plt.show()
        # exit()
        plt.savefig(os.path.join(
            gen_dir, f'per-residue-rmsd-bucket-{bucket}.pdf'))


# Start Fill these

file = "c:\\Users\\Arnab\\Desktop\\per-residue-rmsd-job-af2-9.csv"
file = os.path.abspath(file)

model_name = 'af2-best'
# END Fill these

gen_dir = os.path.join('./gen-rmsd', model_name)
os.makedirs(gen_dir, exist_ok=True)


plot_violin_from_csv(file, gen_dir)
