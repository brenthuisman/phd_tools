#!/usr/bin/env python
import plot, numpy as np,auger,image,rtplan
from scipy.ndimage.filters import gaussian_filter


###########################################################################################################

#volume_offset=-141.59+7.96#spot sources
volume_offset=150-141.59+7.96#spot sources

###########################################################################################################

# BOTTOM ROW IBA

f, ((ax4,ax5,ax6),(ax1,ax2,ax3)) = plot.subplots(nrows=2, ncols=3, sharex=True, sharey=False)

typ = 'iba-auger-notof-3.root'

yield_av = auger.plot_all_ranges_2(ax1,auger.getctset(840964615,'fromclus-sorted/layers-beide/run.e8ai','fromclus-sorted/layers-beide/run.96ra',typ,manualshift=volume_offset),firstcolor='steelblue',secondcolor=None)
yield_av = auger.plot_all_ranges_2(ax1,auger.getctset(848710335,'fromclus-sorted/layers-beide/run.m4RU','fromclus-sorted/layers-beide/run.tLiY',typ,manualshift=volume_offset),firstcolor='seagreen',secondcolor=None)
ax1.set_title('KES, Spot A,\nyield: '+plot.sn(yield_av), fontsize=8)
ax1.set_ylabel('PG detected [counts]')

yield_av = auger.plot_all_ranges_2(ax2,auger.getctset(1068263318,'fromclus-sorted/layers-beide/run.E2tF','fromclus-sorted/layers-beide/run.qE8o',typ,manualshift=volume_offset),firstcolor='steelblue',secondcolor=None)
yield_av = auger.plot_all_ranges_2(ax2,auger.getctset(1071596684,'fromclus-sorted/layers-beide/run.r48i','fromclus-sorted/layers-beide/run.c0rg',typ,manualshift=volume_offset),firstcolor='seagreen',secondcolor=None)
ax2.set_title('KES, Spot B,\nyield: '+plot.sn(yield_av), fontsize=8)
ax2.set_xlabel('Position [mm]')

yield_av = auger.plot_all_ranges_2(ax3,auger.getctset(1068263318,'fromclus-sorted/layers-beide/run.E2tF','fromclus-sorted/layers-beide/run.qE8o',typ,manualshift=volume_offset),firstcolor='steelblue',secondcolor=None)
yield_av = auger.plot_all_ranges_2(ax3,auger.getctset(979533764,'fromclus-sorted/layers-beide/run.c4UF','fromclus-sorted/layers-beide/run.bj2R',typ,manualshift=volume_offset),firstcolor='seagreen',secondcolor=None)
ax3.set_title('KES, Spot C,\nyield: '+plot.sn(yield_av), fontsize=8)

######## TopRow IPNL

typ = 'ipnl-auger-tof-1.root'

yield_av = auger.plot_all_ranges_2(ax4,auger.getctset(840964615,'fromclus-sorted/layers-beide/run.CKCH','fromclus-sorted/layers-beide/run.lrnj',typ,manualshift=volume_offset),firstcolor='steelblue',secondcolor=None)
yield_av = auger.plot_all_ranges_2(ax4,auger.getctset(848710335,'fromclus-sorted/layers-beide/run.3At2','fromclus-sorted/layers-beide/run.Ydep',typ,manualshift=volume_offset),firstcolor='seagreen',secondcolor=None)
ax4.set_xlim(-80,60)
ax4.set_ylabel('PG detected [counts]')
ax4.set_title('MPS, Spot A,\nyield: '+plot.sn(yield_av), fontsize=8)

yield_av = auger.plot_all_ranges_2(ax5,auger.getctset(1068263318,'fromclus-sorted/layers-beide/run.7coj','fromclus-sorted/layers-beide/run.ptEe',typ,manualshift=volume_offset),firstcolor='steelblue',secondcolor=None)
yield_av = auger.plot_all_ranges_2(ax5,auger.getctset(1071596684,'fromclus-sorted/layers-beide/run.KXRm','fromclus-sorted/layers-beide/run.jTj9',typ,manualshift=volume_offset),firstcolor='seagreen',secondcolor=None)
ax5.set_xlabel('Position [mm]')
ax5.set_title('MPS, Spot B,\nyield: '+plot.sn(yield_av), fontsize=8)

yield_av = auger.plot_all_ranges_2(ax6,auger.getctset(1068263318,'fromclus-sorted/layers-beide/run.7coj','fromclus-sorted/layers-beide/run.ptEe',typ,manualshift=volume_offset),firstcolor='steelblue',secondcolor=None)
yield_av = auger.plot_all_ranges_2(ax6,auger.getctset(979533764,'fromclus-sorted/layers-beide/run.8aMd','fromclus-sorted/layers-beide/run.wM5z',typ,manualshift=volume_offset),firstcolor='seagreen',secondcolor=None)
ax6.set_title('MPS, Spot C,\nyield: '+plot.sn(yield_av), fontsize=8)








ax4.xaxis.set_visible(False)
ax5.xaxis.set_visible(False)
ax6.xaxis.set_visible(False)
ax5.yaxis.set_visible(False)
ax6.yaxis.set_visible(False)

ax2.yaxis.set_visible(False)
ax3.yaxis.set_visible(False)

f.subplots_adjust(hspace=0.3)

f.savefig('layerprofiles.results.pdf', bbox_inches='tight')
plot.close('all')


