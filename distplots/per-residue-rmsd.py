import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# --- Load your data ---
df = pd.read_csv("c:\\Users\\Arnab\\Desktop\\per-residue-rmsd-job-af2-9.csv")

# Replace 'your_column' with the column name you want to plot
data = df['per_res_ca_rmsd_A'].dropna()

# --- Compute statistics ---
mean = data.mean()
median = data.median()
std = data.std()

# --- Plot ---
plt.figure(figsize=(10, 6))
sns.histplot(data, kde=True, color="skyblue",
             # <-- increase this to smooth the KDE)
             stat="density", bins='auto')

# --- Add vertical lines ---
plt.axvline(mean, color='red', linestyle='-',
            linewidth=2, label=f'Mean = {mean:.2f}')
plt.axvline(median, color='green', linestyle='--',
            linewidth=2, label=f'Median = {median:.2f}')

# Standard deviations (1σ, 2σ, 3σ)
for i in range(1, 4):
    plt.axvline(mean + i*std, color='orange', linestyle=':',
                linewidth=1.5, label=f'+{i}σ')
    # plt.axvline(mean - i*std, color='orange', linestyle=':',
    #             linewidth=1.5, label=f'-{i}σ')

plt.xlim(left=0, right=1.2)
plt.title('Distribution with Mean, Median, and Standard Deviations')
plt.xlabel('Value')
plt.ylabel('Density')
plt.legend()
plt.tight_layout()
plt.show()
