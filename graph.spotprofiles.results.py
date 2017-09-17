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

yield_av = auger.plot_all_ranges_2(ax1, auger.getctset(1e9,'fromclus-sorted/spots-iba/run.k0Zs','fromclus-sorted/spots-iba/run.Y1My',typ,manualshift=volume_offset) )
ax1.set_title('KES, Spot A,\nyield: '+plot.sn(yield_av), fontsize=8)
ax1.set_ylabel('PG detected [counts]')

yield_av = auger.plot_all_ranges_2(ax2, auger.getctset(1e9,'fromclus-sorted/spots-iba/run.tsUO','fromclus-sorted/spots-iba/run.TUEA',typ,manualshift=volume_offset) )
ax2.set_title('KES, Spot B,\nyield: '+plot.sn(yield_av), fontsize=8)
ax2.set_xlabel('Position [mm]')

yield_av = auger.plot_all_ranges_2(ax3, auger.getctset(1e9,'fromclus-sorted/spots-iba/run.tf1u','fromclus-sorted/spots-iba/run.cDeA',typ,manualshift=volume_offset) )
ax3.set_title('KES, Spot C,\nyield: '+plot.sn(yield_av), fontsize=8)

######## TopRow IPNL

typ = 'ipnl-auger-tof-1.root'

#shift = 13.76-19.44
yield_av = auger.plot_all_ranges_2(ax4,auger.getctset(1e9,'fromclus-sorted/spots-ipnl/run.pMSA','fromclus-sorted/spots-ipnl/run.gwKk',typ,manualshift=volume_offset))
ax4.set_xlim(-80,60)
ax4.set_ylabel('PG detected [counts]')
ax4.set_title('MPS, Spot A,\nyield: '+plot.sn(yield_av), fontsize=8)

#shift = 4.89-8.53
yield_av = auger.plot_all_ranges_2(ax5,auger.getctset(1e9,'fromclus-sorted/spots-ipnl/run.TtIT','fromclus-sorted/spots-ipnl/run.SmHn',typ,manualshift=volume_offset) )
ax5.set_xlabel('Position [mm]')
ax5.set_title('MPS, Spot A,\nyield: '+plot.sn(yield_av), fontsize=8)

#shift = 22.20-29.04
yield_av = auger.plot_all_ranges_2(ax6, auger.getctset(1e9,'fromclus-sorted/spots-ipnl/run.EYBe','fromclus-sorted/spots-ipnl/run.6HvZ',typ,manualshift=volume_offset) )
ax6.set_title('MPS, Spot A,\nyield: '+plot.sn(yield_av), fontsize=8)

ax4.xaxis.set_visible(False)
ax5.xaxis.set_visible(False)
ax6.xaxis.set_visible(False)
ax5.yaxis.set_visible(False)
ax6.yaxis.set_visible(False)

ax2.yaxis.set_visible(False)
ax3.yaxis.set_visible(False)

f.subplots_adjust(hspace=0.3)

f.savefig('spotprofiles.results.pdf', bbox_inches='tight')
plot.close('all')


