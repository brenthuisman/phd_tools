#!/usr/bin/env python
# -*- coding: utf-8 -*-
import plot,numpy as np
import matplotlib as mpl

def git(ax,res,yerr):
    #res = [3.13,2.18]
    #yerr = [1.16,0.89]
    labels = ["Iso-energy","Iso-depth"]
    ind = np.arange(len(res))
    margin = 0.2
    width = (1.-2.*margin)
    xdata = ind-width/2.
    ax.bar(xdata, res, width, yerr=yerr,color='k',ecolor='k',lw=0,fill=False)#,capsize=5)#, markeredgewidth=1)
    #ax.bar(xdata, res, width, yerr=yerr, xerr=0.03,color='k',ecolor='k',lw=0,fill=False)
    ax.errorbar(xdata+width/2.,res,yerr=yerr,color='black',fmt='.',lw=1,capsize=5, markeredgewidth=1)
    ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(range(len(res))))
    #ax.set_xticklabels(['']+labels, fontsize=8, rotation=15, ha='center')
    ax.set_xticklabels(labels, fontsize=8, rotation=15, ha='center')

# MPS, KES, (ABC)
f, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plot.subplots(nrows=2, ncols=3, sharex=True, sharey=True)

#Dose & 2.47 & 1.60 & 6.40 & 4.07 & 6.40 & 6.40
ax1.axhline(2.47, xmin= 0, xmax=0.5 , color='indianred', ls='-',lw=1)#, alpha=0.5)
ax1.axhline(1.60, xmin= 0.5, xmax=1 , color='indianred', ls='-',lw=1)#, alpha=0.5)

ax2.axhline(6.40, xmin= 0, xmax=0.5 , color='indianred', ls='-',lw=1)#, alpha=0.5)
ax2.axhline(4.07, xmin= 0.5, xmax=1 , color='indianred', ls='-',lw=1)#, alpha=0.5)

ax3.axhline(6.40, xmin= 0, xmax=0.5 , color='indianred', ls='-',lw=1)#, alpha=0.5)
ax3.axhline(6.40, xmin= 0.5, xmax=1 , color='indianred', ls='-',lw=1)#, alpha=0.5)

ax4.axhline(2.47, xmin= 0, xmax=0.5 , color='indianred', ls='-',lw=1)#, alpha=0.5)
ax4.axhline(1.60, xmin= 0.5, xmax=1 , color='indianred', ls='-',lw=1)#, alpha=0.5)

ax5.axhline(6.40, xmin= 0, xmax=0.5 , color='indianred', ls='-',lw=1)#, alpha=0.5)
ax5.axhline(4.07, xmin= 0.5, xmax=1 , color='indianred', ls='-',lw=1)#, alpha=0.5)

ax6.axhline(6.40, xmin= 0, xmax=0.5 , color='indianred', ls='-',lw=1)#, alpha=0.5)
ax6.axhline(6.40, xmin= 0.5, xmax=1 , color='indianred', ls='-',lw=1)#, alpha=0.5)

git(ax1, [3.13,2.18], [1.16,0.89])
ax1.set_title('MPS Spot A')

git(ax2, [4.82,3.67], [1.00,0.96])
ax2.set_title('MPS Spot B')

git(ax3, [4.72,5.57], [1.17,1.05])
ax3.set_title('MPS Spot C')

git(ax4, [4.20,1.80], [3.61,2.55])
ax4.set_title('KES Spot A')

git(ax5, [4.90, 3.75], [3.38,2.71])
ax5.set_title('KES Spot B')

git(ax6, [4.15,5.15], [3.82,2.87])
ax6.set_title('KES Spot C')


f.savefig('layerresults.pdf', bbox_inches='tight')
plot.close('all')

