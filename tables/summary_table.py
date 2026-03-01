import json
import pandas as pd

file = '../Metrics Generated/metrics-metjob-v2-5.csv'


def summarize(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    return {
        "mean": f"{series.mean():.3f} ± {series.std():.3f}",
        "median": f"{series.median():.3f} ({q1:.3f}–{q3:.3f})",
    }


with open('../count_stats.json', 'r') as f:
    count_dict = json.load(f)

metrics = [
    # {
    #     'metric': 'lddt',
    #     'metric_name': 'LDDT',
    # },
    {
        'metric': 'native_contract',
        'metric_name': 'Native Contract',
        'm_type': 'max',
        'limits': (0.2, 1.0)
    },
    {
        'metric': 'tm_score',
        'metric_name': 'TM-score',
        'm_type': 'max',
        'limits': (0.0, 1.0)
    },
    {
        'metric': 'gdt_ts',
        'metric_name': 'GDT TS',
        'm_type': 'max',
        'limits': (0, 100)
    }


]


print(r'''
\begin{table}
\centering
\caption{Summary statistics of TM-score distributions across proteins.}
\label{tab:stat_summary}
\begin{tabular}{llccccccccccc}
\multirow{2}{*}{Metric} & \multirow{2}{*}{Statistic} & \multicolumn{2}{c}{10-19} & & \multicolumn{2}{c}{20-29} & & \multicolumn{2}{c}{30-39} & & \multicolumn{2}{c}{40-49} \\
\cline{3-4} \cline{6-7} \cline{9-10} \cline{12-13}
& & Median & Max & & Median & Max & & Median & Max & & Median & Max \\ \hline 
      ''')

for metric in metrics:
    line1 = f'\multirow{{2}}{{*}}{{{metric["metric_name"]}}} & ' +\
        f'Mean $\\pm$ SD & '
    line2 = ' & Median (IQR) & '
    for bucket in ['20', '30', '40', '50']:
        df = pd.read_csv(file)
        df = df[df['pdb_id'].isin(count_dict['id_bucket'][bucket])]

        # Add to master list with file identifier
        bucket = int(bucket)

        per_protein = df.groupby("serial")[metric['metric']].agg(
            median="median",
            max="max"
        )

        median_aggergation = summarize(per_protein["median"])
        line1 += median_aggergation['mean'] + ' & '
        line2 += median_aggergation['median'] + ' & '

        max_aggergation = summarize(per_protein["max"])
        line1 += max_aggergation['mean'] + ' & & '
        line2 += max_aggergation['median'] + ' & & '

        # print(f'METRIC: {metric["metric_name"]} | BUCKET {bucket}')
        # print(table)
        # print()
    line1 = line1[:-4] + ' \\\\'
    line2 = line2[:-4] + ' \\\\'
    print(line1)
    print(line2)

print('''\\hline
\\end{tabular}
\\end{table}
''')
