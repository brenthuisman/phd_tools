#!/usr/bin/env python
import seaborn as sns,pandas as pd,plot

df = pd.read_csv("resultstable.tsv",sep='\t')

pc_data = df.query("typ=='ipnl-auger-tof-1.root' or typ=='iba-auger-notof-3.root'")

sns.set_style(style="whitegrid")
sns.set(font_scale=1.1)
f, ax1 = plot.subplots(nrows=1, ncols=1)

sns.lineplot(x="nprim", y="fopsigma", hue="typ", markers=True, data=pc_data, ax=ax1)
ax1.set_title("Fall-off Retrieval position (FRP)")
ax1.set_ylabel("FRP (mm)")
ax1.set_xlabel("Number of primary protons")
ax1.semilogx()

new_labels = ['Camera', 'MPS', 'KES']
for t, l in zip(ax1.get_legend().texts, new_labels): t.set_text(l)


f.savefig('pc_frp_plot.pdf', bbox_inches='tight')
