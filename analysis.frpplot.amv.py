#!/usr/bin/env python
import seaborn as sns,pandas as pd,plot

df = pd.read_csv("results.tsv",sep='\t',nrows=6,skiprows=[1])

print df

sns.set_style(style="whitegrid")
sns.set(font_scale=1.1)
f, ax1 = plot.subplots(nrows=1, ncols=1)

sns.lineplot(x="nprim", y="fopsigma", hue="typ", markers=True, data=df, ax=ax1)
ax1.set_title("Fall-off Retrieval position (FRP)")
ax1.set_ylabel("FRP (mm)")
ax1.set_xlabel("Number of primary protons")
ax1.semilogx()

new_labels = ['Camera', 'MPS', 'KES']
for t, l in zip(ax1.get_legend().texts, new_labels): t.set_text(l)


f.savefig('amv_frp_plot.pdf', bbox_inches='tight')
