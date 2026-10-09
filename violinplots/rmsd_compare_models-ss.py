import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os


def plot_violin_from_csvs(files: list, models: list, gen_dir):

    with open('../ss_clusters-alt.json', 'r') as f:
        count_dict = json.load(f)

    # === Step 2: Process each file ===

    for bucket in ['alpha-helix-rich', 'beta-sheet-rich', 'disordered', 'mixed']:
        sns.set_theme(style="whitegrid")
        sns.set_context("paper", font_scale=1.25)
        sns.set_palette("muted")

        plt.figure(figsize=(5, 3))

        bucket_match = []
        for file, model in zip(files, models):
            df = pd.read_csv(file)
            df = df[df['pdb_id'].isin(count_dict[bucket])]
            # col = df[column]  # or set explicitly, e.g., 'values'

            # sequence = col.dropna().tolist()

            # Add to master list with file identifier
            # bucket_ = int(bucket)
            # bucket_match.extend([{
            #     "model": model,
            #     "value": v
            # } for v in sequence])

            # Compute summary stats for each type
            # summary = df.groupby("serial")[column].agg(
            #     median="median", min="min", max="max")
            # summary = summary.reset_index()

            # Reshape into long format so seaborn can plot a split violin
            # long = pd.melt(summary,
            #                id_vars="serial",
            #                value_vars=["median", m_type],
            #                var_name="statistic",
            #                value_name=column)

            for _, row in df.iterrows():
                bucket_match.append({
                    "model": model,
                    "value": row['per_res_ca_rmsd_A'],
                    # "Statistic": row['statistic']
                })

        # === Step 3: Create DataFrame for Seaborn ===
        plot_df = pd.DataFrame(bucket_match)

        # sns.violinplot(data=plot_df, x="model",
        #                # options: 'box', 'quartile', 'point', 'stick', None
        #                y="value", hue="model", inner="box",
        #                #    cut=0,              # restrict KDE to the observed range
        #                linewidth=1.2)

        sns.violinplot(data=plot_df, x="model",
                       # options: 'box', 'quartile', 'point', 'stick', None
                       y="value", inner="quartile",  hue='model',  # hue='Statistic',  # split=True,
                       gap=0.1,  # density_norm='width',
                       #    cut=0,              # restrict KDE to the observed range
                       linewidth=1.2,
                       #    palette={
                       #        "median": "#A6CEE3",   # blue
                       #        m_type: "#FDBE85"   # coral
                       #    }
                       )

        plt.xlabel("Prediction Model")
        plt.ylabel(r"Per Residue c$\alpha$ RMSD (Å)")
        # plt.title("Overlapping KDE Plots")
        # plt.legend(title="Hllo")
        plt.xticks(rotation=15)
        plt.ylim(0, 1.5)
        plt.tight_layout()
        # plt.show()
        # exit()
        bucket_range = f'{bucket}'
        plt.savefig(os.path.join(
            gen_dir, f'ss_wise_{bucket_range}-rmsd.pdf'), bbox_inches="tight")


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
    '../Metrics Generated/per-residue-rmsd-job-af2-9.csv',
    '../Metrics Generated/per-residue-rmsd-job-rf2-7.csv',
    '../Metrics Generated/per-residue-rmsd-job-esm-4.csv',
    '../Metrics Generated/per-residue-rmsd-job-omf-6.csv',
    '../Metrics Generated/per-residue-rmsd-job-dmp-5.csv'
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


gen_dir = os.path.join('./gen', metricplot)
os.makedirs(gen_dir, exist_ok=True)

plot_violin_from_csvs(
    files, models, gen_dir)
