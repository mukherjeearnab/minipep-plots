import json
import pandas as pd

############################
file = '../Metrics Generated/metrics-metrics-dbamp3-rf2-vs-esm.filtered.csv'
rmsd_file = '../Metrics Generated/per-residue-rmsd-per-residue-rmsd-dbamp3-rf2-vs-esm.filtered.csv'
ModelName = 'RoseTTAFold2 vs. ESMFold'
###########################


def summarize(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    return {
        "mean": f"{series.mean():.2f} ± {series.std():.2f}",
        "median": f"{series.median():.2f} ({q1:.2f}–{q3:.2f})",
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
        'metric_name': '\\textbf{Q}',
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
\footnotesize
\caption{Summary statistics of '''+ModelName+r''' for distributions of Native Contract, TM-score and GDT TS across dbAMP3 dataset.}
\label{tab:stat_summary_'''+ModelName+r'''}
\begin{tabular}{llcccc}
\hline
\multirow{2}{*}{Metric} & \multirow{2}{*}{Statistic} & \multicolumn{4}{c}{Bucket} \\
\cline{3-6}
 & & 10-19 & 20-29 & 30-39 & 40-49 \\ \hline''')

##########
# DO IT FOR RMSD
with open('../dbamp3-lengthwise-cluster.json', 'r') as f:
    count_dict = json.load(f)
line1 = f'\multirow{{2}}{{*}}{{RMSD}} & ' +\
        f'Mean $\\pm$ SD '
line2 = ' & Median (IQR) '
for bucket in ['20', '30', '40', '50']:
    df = pd.read_csv(rmsd_file)

    # df = df.dropna()

    df = df[df['pdb_id'].isin(count_dict[bucket])]

    # --- Compute statistics ---

    # Add to master list with file identifier
    bucket = int(bucket)

    data = df['per_res_ca_rmsd_A'].dropna()
    summary = summarize(data)
    line1 += '& ' + summary['mean']
    line2 += '& ' + summary['median']

line1 += ' \\\\'
line2 += ' \\\\'
# line3 += ' \\\\'
# line4 += ' \\\\'
print(line1)
print(line2, '\\hline')


####################
# DO IT FOR REST OF THE METRICS
for metric in metrics:
    line1 = f'\multirow{{2}}{{*}}{{{metric["metric_name"]}}} & ' +\
        f'Mean $\\pm$ SD '
    line2 = ' & Median (IQR) '
    # line3 = r' & \multirow{2}{*}{Max} & ' + 'Mean $\\pm$ SD '
    # line4 = ' & & Median (IQR) '
    for bucket in ['20', '30', '40', '50']:
        df = pd.read_csv(file)
        df = df[df['pdb_id'].isin(count_dict[bucket])]

        # Add to master list with file identifier
        bucket = int(bucket)

        # per_protein = df.groupby("serial")[metric['metric']]

        median_aggergation = summarize(df[metric['metric']])
        line1 += '& ' + median_aggergation['mean']
        line2 += '& ' + median_aggergation['median']

        # max_aggergation = summarize(per_protein["max"])
        # line3 += '& ' + max_aggergation['mean']
        # line4 += '& ' + max_aggergation['median']

        # print(f'METRIC: {metric["metric_name"]} | BUCKET {bucket}')
        # print(table)
        # print()
    line1 += ' \\\\'
    line2 += ' \\\\'
    # line3 += ' \\\\'
    # line4 += ' \\\\'
    print(line1)
    print(line2, '\\hline')
    # print(line3)
    # print(line4)

print('\\hline')

######################################
# DO IT FOR SECONDARY STRUCTURE WISE
print(r'''\multirow{2}{*}{Metric} & \multirow{2}{*}{Statistic} & \multicolumn{4}{c}{Secondary Structure} \\
\cline{3-6}
 & & $\alpha$-helix Rich & $\beta$-sheet Rich & Disordered & Mixed \\ \hline''')

buckets = ['alpha-helix-rich', 'beta-sheet-rich', 'disordered', 'mixed']

names = {
    'alpha-helix-rich': r'$\alpha$-helix Rich',
    'beta-sheet-rich': r'$\beta$-sheet Rich',
    'disordered': 'Disordered',
    'mixed': 'Mixed'
}

##############################
# SS RMSD
with open('../ss_clusters-alt.json', 'r') as f:
    count_dict = json.load(f)
line1 = f'\multirow{{2}}{{*}}{{RMSD}} & ' +\
        f'Mean $\\pm$ SD '
line2 = ' & Median (IQR) '
for bucket in buckets:
    df = pd.read_csv(rmsd_file)

    df = df[df['pdb_id'].isin(count_dict[bucket])]

    # --- Compute statistics ---

    # Add to master list with file identifier
    # bucket = int(bucket)

    data = df['per_res_ca_rmsd_A'].dropna()
    summary = summarize(data)
    line1 += '& ' + summary['mean']
    line2 += '& ' + summary['median']

line1 += ' \\\\'
line2 += ' \\\\'
# line3 += ' \\\\'
# line4 += ' \\\\'
print(line1)
print(line2, '\\hline')


####################
# SS REST OF THE METRICS
for metric in metrics:
    line1 = f'\multirow{{2}}{{*}}{{{metric["metric_name"]}}} & ' +\
        f'Mean $\\pm$ SD '
    line2 = ' & Median (IQR) '
    # line3 = r' & \multirow{2}{*}{Max} & ' + 'Mean $\\pm$ SD '
    # line4 = ' & & Median (IQR) '
    for bucket in buckets:
        df = pd.read_csv(file)
        df = df[df['pdb_id'].isin(count_dict[bucket])]

        # Add to master list with file identifier
        # bucket = int(bucket)

        # per_protein = df.groupby("serial")[metric['metric']]

        median_aggergation = summarize(df[metric['metric']])
        line1 += '& ' + median_aggergation['mean']
        line2 += '& ' + median_aggergation['median']

        # max_aggergation = summarize(per_protein["max"])
        # line3 += '& ' + max_aggergation['mean']
        # line4 += '& ' + max_aggergation['median']

        # print(f'METRIC: {metric["metric_name"]} | BUCKET {bucket}')
        # print(table)
        # print()
    line1 += ' \\\\'
    line2 += ' \\\\'
    # line3 += ' \\\\'
    # line4 += ' \\\\'
    print(line1)
    print(line2, '\\hline')
    # print(line3)
    # print(line4)


print('''\\end{tabular}
\\end{table}
''')
