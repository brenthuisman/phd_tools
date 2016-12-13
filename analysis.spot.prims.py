#!/usr/bin/env python
import numpy as np,plot,auger
from scipy.stats import chisquare

#np.random.seed(659873247)

###################################

#############gate_run_submit_cluster_nomove.sh mac/main-int9ct.mac 10
#############gate_run_submit_cluster_nomove.sh mac/main-int9rpct.mac 10
#############gate_run_submit_cluster_nomove.sh mac/main-int8ct.mac 10
#############gate_run_submit_cluster_nomove.sh mac/main-int8rpct.mac 10
#############gate_run_submit_cluster_nomove.sh mac/main-int7ct.mac 10
#############gate_run_submit_cluster_nomove.sh mac/main-int7rpct.mac 10
#############gate_run_submit_cluster_nomove.sh mac/main-int6ct.mac 10
#############gate_run_submit_cluster_nomove.sh mac/main-int6rpct.mac 10
#############xTcG
#############b2Aj
#############bfrX
#############rOx1
#############41VE
#############NE7B
#############yjzw
#############wfmx

#typ='ipnl'
typ='iba'

ctset_int_6 = auger.getctset(1e6,'run.yjzw','run.wfmx',typ)
ctset_int_7 = auger.getctset(1e7,'run.41VE','run.NE7B',typ)
ctset_int_8 = auger.getctset(1e8,'run.bfrX','run.rOx1',typ)
ctset_int_9 = auger.getctset(1e9,'run.xTcG','run.b2Aj',typ)

f, ((ax1,ax2),(ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

auger.plotrange(ax1,ctset_int_9)
auger.plotrange(ax2,ctset_int_8)
auger.plotrange(ax3,ctset_int_7)
auger.plotrange(ax4,ctset_int_6)
f.subplots_adjust(hspace=.5)

ax1.set_xlim(-40,40)
ax2.set_xlim(-40,40)
ax3.set_xlim(-40,40)
ax4.set_xlim(-40,40)

ax1.set_xlabel('')
ax2.set_xlabel('')
ax2.set_ylabel('')
ax4.set_ylabel('')
f.savefig(typ+'-spot-nprims.pdf', bbox_inches='tight')
plot.close('all')

#print '====== chisq CT w RPCT ====='
#print '9,9', chisquare(ctset_int_9['ct']['av'],f_exp=ctset_int_9['rpct']['av'])
#print '8,8', chisquare(ctset_int_8['ct']['av'],f_exp=ctset_int_8['rpct']['av'])
#print '7,7', chisquare(ctset_int_7['ct']['av'],f_exp=ctset_int_7['rpct']['av'])
#print '6,6', chisquare(ctset_int_6['ct']['av'],f_exp=ctset_int_6['rpct']['av'])
	
#print '====== chisq CT w CT ====='
#print '9,9', chisquare(ctset_int_9['ct']['av'],f_exp=ctset_int_9['ct']['av'])
#print '9,8', chisquare(ctset_int_8['ct']['av'],f_exp=ctset_int_9['ct']['av'])
#print '9,7', chisquare(ctset_int_7['ct']['av'],f_exp=ctset_int_9['ct']['av'])
#print '9,6', chisquare(ctset_int_6['ct']['av'],f_exp=ctset_int_9['ct']['av'])

#print '====== chisq RPCT w RPCT ====='
#print '9,9', chisquare(ctset_int_9['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
#print '9,8', chisquare(ctset_int_8['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
#print '9,7', chisquare(ctset_int_7['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
#print '9,6', chisquare(ctset_int_6['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
