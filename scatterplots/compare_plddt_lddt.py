import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os


def plot_scatter_from_csv(file, model_name, gen_dir):

    with open('../count_stats.json', 'r') as f:
        count_dict = json.load(f)

    for bucket in ['20', '30', '40', '50']:
        df = pd.read_csv(file)

        df = df[df['pdb_id'].isin(count_dict['id_bucket'][bucket])]
        sns.set_theme(style="whitegrid")
        sns.set_context("paper", font_scale=1.25)
        sns.set_palette("muted")
        plt.figure(figsize=(5, 3))

        ax = sns.regplot(data=df, x='lddt', y='plddt', lowess=True, scatter_kws={
            'alpha': 0.6}, line_kws={'color': 'orange'})

        # Compute Pearson correlation
        r, p = pearsonr(df['lddt'], df['plddt'])

        # Annotate correlation coefficient
        ax.text(
            # position (in data coordinates by default)
            0.02, 0.96,
            f"Pearson Coef.: {r:.2f}",    # text to display
            transform=ax.transAxes,          # use axes fraction instead of data coords
            fontsize=12,
            verticalalignment='top',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.5)
        )

        plt.xlabel("LDDT")
        plt.ylabel('Confidence')

        # plt.title("Overlapping KDE Plots")
        # plt.legend(title="Hllo")
        # plt.xticks(rotation=45)
        plt.tight_layout()
        # plt.show()
        # exit()
        plt.savefig(os.path.join(
            gen_dir, f'{model_name}-plddt-vs-lddt-b{bucket}.pdf'))

# Start Fill these


file = '../Metrics Generated/plddt-5.csv'
file = os.path.abspath(file)

model_name = 'dmp'
# END Fill these

gen_dir = os.path.join('./gen')
os.makedirs(gen_dir, exist_ok=True)


plot_scatter_from_csv(
    file, model_name, gen_dir)
