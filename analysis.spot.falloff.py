#!/usr/bin/env python
import numpy as np,plot,auger

#OPT: quickly get sorted rundirs
# zb autogen | sort -k1.13 -r

#OPT: fix seed
#np.random.seed(65983247)

#we dont know what the added or reduced noise level is when changing energy windows, so we cant compare performance for ipnl3 and iba1.
typs=['ipnl-auger-tof-1.root','iba-auger-notof-3.root']

#typs+=['ipnl-auger-notof-1.root','iba-auger-tof-3.root','ipnl-auger-tof-3.root','iba-auger-tof-1.root','ipnl-auger-notof-3.root','iba-auger-notof-1.root']

#ipnl FFFF
#typs=['ipnlf-auger-tof-1.root','ipnlf-auger-notof-1.root']

for typ in typs:

	#loc = 'spot61'
	#ctset_int_6 = auger.getctset(1e6,'run.rFN5','run.jUPf',typ)# 5 , 0  # AGJb , 
	#ctset_int_7 = auger.getctset(1e7,'run.AE5G','run.gK11',typ)# 2 , 0  # ZbiH , 		:done
	#ctset_int_8 = auger.getctset(1e8,'run.lNkm','run.ztcV',typ)# 0 , 4  #  , i7Oz
	#ctset_int_9 = auger.getctset(1e9,'run.A3vG','run.9950',typ)# 7 , 10 # PB2P , KVWm

	#loc = 'spot29'
	#ctset_int_6 = auger.getctset(1e6,'run.7OvR','run.ykAn',typ)#
	#ctset_int_7 = auger.getctset(1e7,'run.aNrj','run.GERe',typ)# , 1 # , w9gm 			:done
	#ctset_int_8 = auger.getctset(1e8,'run.E3So','run.okUi',typ)#
	#ctset_int_9 = auger.getctset(1e9,'run.9WZ0','run.xEMN',typ)#

	#loc = 'spot40'
	#ctset_int_6 = auger.getctset(1e6,'run.zE43','run.MUoq',typ)# 7 ,  # EdQf , 		:done
	#ctset_int_7 = auger.getctset(1e7,'run.V4ER','run.Hhup',typ)#  ,  #  ,  
	#ctset_int_8 = auger.getctset(1e8,'run.XkoP','run.cLDV',typ)#  , 6 #  , kDxT		:done
	#ctset_int_9 = auger.getctset(1e9,'run.AuZu','run.ECUY',typ)# 2 , 1 # vWKg , wS3i

	#loc = 'waterbox'
	#ctset_int_6 = auger.getctset(1e6,'run.WbDj','run.f9cL',typ)
	#ctset_int_7 = auger.getctset(1e7,'run.ngMk','run.Ho8b',typ)
	#ctset_int_8 = auger.getctset(1e8,'run.cj4U','run.RWsd',typ)
	#ctset_int_9 = auger.getctset(1e9,'run.kVk7','run.iias',typ)
	
	#loc = 'waterboxshifted'
	#ctset_int_6 = auger.getctset(1e6,'run.BPnu','run.q7Vn',typ)
	#ctset_int_7 = auger.getctset(1e7,'run.UAJZ','run.ebjM',typ)
	#ctset_int_8 = auger.getctset(1e8,'run.SwIj','run.XYSQ',typ)# 50 ,  # SwIj ,  
	#ctset_int_9 = auger.getctset(1e9,'run.1vRP','run.KvuV',typ)#  , 11 #  ,  g4RC
	
	loc = 'waterboxfakeshift' #compare 144MeV against shifted 139mev
	ctset_int_6 = auger.getctset(1e6,'run.pSBH','run.q7Vn',typ)
	ctset_int_7 = auger.getctset(1e7,'run.pDRM','run.ebjM',typ)
	ctset_int_8 = auger.getctset(1e8,'run.IdLD','run.XYSQ',typ)
	ctset_int_9 = auger.getctset(1e9,'run.LswJ','run.KvuV',typ)
	
	#loc = 'realspots' ############################################################################TODO!!!!!!!
	#ctset_int_6 = auger.getctset(27500000,'run.LUBP','run.hRZn',typ)# ,  # , 
	#ctset_int_7 = auger.getctset(47300000,'run.7WZC','run.3Zs9',typ)# 3 , 11 # s3aB, 4gLD
	
	#ctset_int_8 = auger.getctset(1e8,'run.cj4U','run.RWsd',typ)
	#ctset_int_9 = auger.getctset(1e9,'run.kVk7','run.iias',typ)
	############################################################################################

	f, ((ax1,ax2),(ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

	auger.plot_all_ranges(ax1,ctset_int_9)
	auger.plot_all_ranges(ax2,ctset_int_8)
	auger.plot_all_ranges(ax3,ctset_int_7)
	auger.plot_all_ranges(ax4,ctset_int_6)
	f.subplots_adjust(hspace=.5)
	ax1.set_xlabel('')
	ax2.set_xlabel('')
	ax2.set_ylabel('')
	ax4.set_ylabel('')
	f.savefig(loc+'-'+typ+'-FOP.pdf', bbox_inches='tight')
	plot.close('all')

	#############################################################################################

	from mpl_toolkits.mplot3d import Axes3D
	import matplotlib.pyplot as plt

	fig = plt.figure()
	ax1 = plt.axes(projection='3d')
	ax1.view_init(30, -50)

	auger.plotfodiffdist(ax1,ctset_int_9,0)
	auger.plotfodiffdist(ax1,ctset_int_8,1)
	auger.plotfodiffdist(ax1,ctset_int_7,2)
	auger.plotfodiffdist(ax1,ctset_int_6,3)
	#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
	fig.savefig(loc+'-'+typ+'-FOP-shift.pdf')#, bbox_inches='tight')
	plt.close('all')

	#############################################################################################

	fig = plt.figure()
	ax1 = plt.axes(projection='3d')
	ax1.view_init(30, -50)

	auger.plotfodist(ax1,ctset_int_9,0)
	auger.plotfodist(ax1,ctset_int_8,1)
	auger.plotfodist(ax1,ctset_int_7,2)
	auger.plotfodist(ax1,ctset_int_6,3)

	#plt.legend()#shadow = True,frameon = True,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'lower right')

	#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
	plt.savefig(loc+'-'+typ+'-FOP-diff.pdf')#, bbox_inches='tight')
	plt.close('all')
