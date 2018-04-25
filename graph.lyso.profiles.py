#!/usr/bin/env python
import plot, numpy as np,re,auger,image,rtplan
from scipy.ndimage.filters import gaussian_filter

###########################################################################################################

#volume_offset=-141.59+7.96#spot sources
volume_offset=0
addnoise = False
#addnoise = 'onlynoise'

###########################################################################################################

# BOTTOM ROW IBA

f, ((ax4,ax5,ax6),(ax1,ax2,ax3)) = plot.subplots(nrows=2, ncols=3, sharex=True, sharey=False)

typ = 'iba-auger-tof-1.root'
typ = 'iba-auger-notof-3.root'

yield_av = auger.plot_all_ranges_2(ax1, auger.getctset(1e9,'run.o5zC','run.o5zC',typ,manualshift=volume_offset,addnoise=addnoise) )
ax1.set_title('KES, 1e9,\nyield: '+plot.sn(yield_av), fontsize=8)
ax1.set_ylabel('PG detected [counts]')

yield_av = auger.plot_all_ranges_2(ax2, auger.getctset(1e8,'run.fFpk','run.fFpk',typ,manualshift=volume_offset,addnoise=addnoise) )
ax2.set_title('KES, 1e8,\nyield: '+plot.sn(yield_av), fontsize=8)
ax2.set_xlabel('Position [mm]')

yield_av = auger.plot_all_ranges_2(ax3, auger.getctset(1e7,'run.Gfu4','run.Gfu4',typ,manualshift=volume_offset,addnoise=addnoise) )
ax3.set_title('KES, 1e7\nyield: '+plot.sn(yield_av), fontsize=8)

######## TopRow IPNL

typ = 'ipnl-auger-tof-1.root'
typ = 'ipnl-auger-notof-3.root'

#shift = 13.76-19.44
yield_av = auger.plot_all_ranges_2(ax4,auger.getctset(1e9,'run.MmAx','run.MmAx',typ,manualshift=volume_offset,addnoise=addnoise))
ax4.set_xlim(-80,60)
ax4.set_ylabel('PG detected [counts]')
ax4.set_title('MPS, 1e9,\nyield: '+plot.sn(yield_av), fontsize=8)

#shift = 4.89-8.53
yield_av = auger.plot_all_ranges_2(ax5,auger.getctset(1e8,'run.pwut','run.pwut',typ,manualshift=volume_offset,addnoise=addnoise) )
ax5.set_xlabel('Position [mm]')
ax5.set_title('MPS, 1e8,\nyield: '+plot.sn(yield_av), fontsize=8)

#shift = 22.20-29.04
yield_av = auger.plot_all_ranges_2(ax6, auger.getctset(1e7,'run.DUPZ','run.DUPZ',typ,manualshift=volume_offset,addnoise=addnoise) )
ax6.set_title('MPS, 1e7,\nyield: '+plot.sn(yield_av), fontsize=8)

ax4.xaxis.set_visible(False)
ax5.xaxis.set_visible(False)
ax6.xaxis.set_visible(False)
ax5.yaxis.set_visible(False)
ax6.yaxis.set_visible(False)

ax2.yaxis.set_visible(False)
ax3.yaxis.set_visible(False)

f.subplots_adjust(hspace=0.3)

suffix = re.findall(r'\d+', typ)[0] #extract numbers and take first one

f.savefig('lysoprofiles.results'+suffix+str(addnoise)+'.pdf', bbox_inches='tight')
plot.close('all')


