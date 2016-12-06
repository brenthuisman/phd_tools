#!/usr/bin/env python
import numpy as np,plot,auger
from scipy.stats import chisquare

#np.random.seed(65983247)

################################################################################

#oude sums.

#typ='ipnl'
#ctset_61 = auger.getctset(68442219,'outputct61','outputrpct61',typ)
#ctset_99 = auger.getctset(113485124,'outputct99','outputrpct99',typ)
#ctset_101 = auger.getctset(107739042,'outputct101','outputrpct101',typ)

#f, ((ax1,ax2),(ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

#auger.plotrange(ax1,ctset_61)
#auger.plotrange(ax2,ctset_99)
#auger.plotrange(ax3,ctset_101)

#ctset_sum = auger.sumctset('sum',ctset_61,ctset_99,ctset_101) #we appear to modift ctset_61 if unc = 1
#auger.plotrange(ax4,ctset_sum)

##print '====== chisq CT w RPCT ====='
##print '9,9', chisquare(ctset_int_9['ct']['av'],f_exp=ctset_int_9['rpct']['av'])
##print '8,8', chisquare(ctset_int_8['ct']['av'],f_exp=ctset_int_8['rpct']['av'])
##print '7,7', chisquare(ctset_int_7['ct']['av'],f_exp=ctset_int_7['rpct']['av'])
##print '6,6', chisquare(ctset_int_6['ct']['av'],f_exp=ctset_int_6['rpct']['av'])
	
##print '====== chisq CT w CT ====='
##print '9,9', chisquare(ctset_int_9['ct']['av'],f_exp=ctset_int_9['ct']['av'])
##print '9,8', chisquare(ctset_int_8['ct']['av'],f_exp=ctset_int_9['ct']['av'])
##print '9,7', chisquare(ctset_int_7['ct']['av'],f_exp=ctset_int_9['ct']['av'])
##print '9,6', chisquare(ctset_int_6['ct']['av'],f_exp=ctset_int_9['ct']['av'])

##print '====== chisq RPCT w RPCT ====='
##print '9,9', chisquare(ctset_int_9['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
##print '9,8', chisquare(ctset_int_8['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
##print '9,7', chisquare(ctset_int_7['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
##print '9,6', chisquare(ctset_int_6['rpct']['av'],f_exp=ctset_int_9['rpct']['av'])
	
#f.savefig('spotplot-sums.pdf', bbox_inches='tight')
#plot.close('all')

################################################################################

typ='ipnl'
typ='iba'
#nieuwe sums. distal layer
#22 , 4 ,
#4 : 65802598.6018 , 7 : 88235302.6706 , 10 : 67298112.2064 , 43 : 64073566.2641 , 

ctset_4 = auger.getctset(65802598,'run.BkDH','run.hNOp',typ)
ctset_7 = auger.getctset(88235302,'run.DK0Q','run.bxO2',typ)
ctset_10 = auger.getctset(67298112,'run.eV6D','run.r4I6',typ)
ctset_43 = auger.getctset(64073566,'run.JOWZ','run.Lmkh',typ)

ctset_sum_0 = auger.sumctset('sum',ctset_4,ctset_7,ctset_10,ctset_43)

f, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plot.subplots(nrows=2, ncols=3, sharex=False, sharey=False)

auger.plotrange(ax1,ctset_4)
auger.plotrange(ax2,ctset_7)
auger.plotrange(ax3,ctset_10)
auger.plotrange(ax4,ctset_43)
ax5.axis('off')
auger.plotrange(ax6,ctset_sum_0)

f.savefig(typ+'-spotsums-0.pdf', bbox_inches='tight')
plot.close('all')

#nieuwe sums. distal-1 layer
#18 , 5 , 
#6 : 58325030.5789 , 9 : 65802598.6018 , 28 : 54600663.4 , 32 : 66406212.2432 , 39 : 42230305.0377 , 

ctset_6 = auger.getctset(58325030,'run.nkdn','run.xOvz',typ)
ctset_9 = auger.getctset(65802598,'run.9yQu','run.zqWi',typ)
ctset_28 = auger.getctset(54600663,'run.Tla5','run.bAMz',typ)
ctset_32 = auger.getctset(66406212,'run.EDis','run.jBIS',typ)
ctset_39 = auger.getctset(42230305,'run.YkSQ','run.xBqm',typ)

ctset_sum_1 = auger.sumctset('sum',ctset_6,ctset_9,ctset_28,ctset_32,ctset_39)

f, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plot.subplots(nrows=2, ncols=3, sharex=False, sharey=False)

auger.plotrange(ax1,ctset_6)
auger.plotrange(ax2,ctset_9)
auger.plotrange(ax3,ctset_28)
auger.plotrange(ax4,ctset_32)
auger.plotrange(ax5,ctset_39)
auger.plotrange(ax6,ctset_sum_1)

f.savefig(typ+'-spotsums-1.pdf', bbox_inches='tight')
plot.close('all')
