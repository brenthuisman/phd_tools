#!/usr/bin/env python
import numpy as np,plot,auger

#OPT: quickly get sorted rundirs
# zb autogen | sort -k1.13 -r

#OPT: fix seed
#np.random.seed(65983247)

#we dont know what the added or reduced noise level is when changing energy windows, so we cant compare performance for ipnl3 and iba1.
typs=['ipnl-auger-tof-1.root','iba-auger-notof-3.root']

#typs+=['ipnl-auger-notof-1.root','iba-auger-tof-3.root','ipnl-auger-tof-3.root','iba-auger-tof-1.root','ipnl-auger-notof-3.root','iba-auger-notof-1.root']

#ipnl FFFF'spot61'
#typs=['ipnlf-auger-tof-1.root','ipnlf-auger-notof-1.root']

def megaplot(ctsets,studyname,emisfops=None,labels=["$10^9$","$10^8$","$10^7$","$10^6$"],axlabel='Primaries [nr]'):
	if emisfops is not None:
		for emisfop in emisfops:
			emisfop[0]+=15.863
			emisfop[1]+=15.863
	print 'FOP shift all overlaid'

	if len(ctsets) == 4:
		f, ((ax1,ax2),(ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

		auger.plot_all_ranges(ax1,ctsets[0])
		auger.plot_all_ranges(ax2,ctsets[1])
		auger.plot_all_ranges(ax3,ctsets[2])
		auger.plot_all_ranges(ax4,ctsets[3])
		if not 'Primaries' in axlabel:
			ax1.set_title(labels[0])
			ax2.set_title(labels[1])
			ax3.set_title(labels[2])
			ax4.set_title(labels[3])
		f.subplots_adjust(hspace=.5)
		ax1.set_xlabel('')
		ax2.set_xlabel('')
		ax2.set_ylabel('')
		ax4.set_ylabel('')
		f.savefig(studyname+'-'+typ+'-FOP.pdf', bbox_inches='tight')
		plot.close('all')

	#############################################################################################

	print 'FOP shift distributions'

	from mpl_toolkits.mplot3d import Axes3D
	import matplotlib.pyplot as plt

	fig = plt.figure()
	ax1 = plt.axes(projection='3d')
	ax1.view_init(30, -50)

	for i,ctset in enumerate(ctsets):
		auger.plotfodiffdist(ax1,ctset,i,emisfops,labels,axlabel)
		if not emisfops == None:
			fopshifts=[]
			for fopset in emisfops:
				fopshifts.append( fopset[-1]-fopset[0] )
			ax1.set_xlim3d(np.mean(fopshifts)-20,np.mean(fopshifts)+20)
	if emisfops is not None and len(emisfops) == 1:
		ax1.set_title(studyname+', $Shift_{em}$ = '+str(emisfops[0][-1]-emisfops[0][0]), y=1.08)
	
	#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
	fig.savefig(studyname+'-'+typ+'-FOP-shift.pdf')#, bbox_inches='tight')
	plt.close('all')

	#############################################################################################

	print 'FOP distributions'

	fig = plt.figure()
	ax1 = plt.axes(projection='3d')
	ax1.view_init(30, -50)

	for i,ctset in enumerate(ctsets):
		auger.plotfodist(ax1,ctset,i,emisfops,labels,axlabel)
	if emisfops is not None and len(emisfops) == 1:
		ax1.set_title(studyname+', $CT_{FOP_{em}}$ = '+str(emisfops[0][0])[:5]+', $RPCT_{FOP_{em}}$ = '+str(emisfops[0][1])[:5], y=1.08)

	#plt.legend()#shadow = True,frameon = True,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'lower right')

	#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
	plt.savefig(studyname+'-'+typ+'-FOP-dist.pdf')#, bbox_inches='tight')
	plt.close('all')
	
	#############################################################################################
	# TODO add pgemissions plots.


for typ in typs:
	ctsetsets = []
	
	#ctsetsets.append( auger.getctset(1e9,'run.A3vG','run.9950',typ) )# 7 , 10 # E0OX , KVWm	:omdat E0OX lang duurt, relaunced als wzVw
	#ctsetsets.append( auger.getctset(1e8,'run.lNkm','run.ztcV',typ) )# 0 , 4  #  , i7Oz 		:done
	#ctsetsets.append( auger.getctset(1e7,'run.AE5G','run.gK11',typ) )# 2 , 0  # ZbiH , 		:done
	#ctsetsets.append( auger.getctset(1e6,'run.rFN5','run.jUPf',typ) )# 5 , 0  # AGJb ,  		:done
	#megaplot(ctsetsets,'spot61',[[6.715,20.58]])

	#ctsetsets.append( auger.getctset(1e9,'run.9WZ0','run.xEMN',typ) )#
	#ctsetsets.append( auger.getctset(1e8,'run.E3So','run.okUi',typ) )#
	#ctsetsets.append( auger.getctset(1e7,'run.aNrj','run.GERe',typ) )# , 1 # , w9gm 			:done
	#ctsetsets.append( auger.getctset(1e6,'run.7OvR','run.ykAn',typ) )#
	#megaplot(ctsetsets,'spot29',[[-1.75,0.291]])
	
	#ctsetsets.append( auger.getctset(1e9,'run.AuZu','run.ECUY',typ) )# 2 , 1 # vWKg , wS3i	:done
	#ctsetsets.append( auger.getctset(1e8,'run.XkoP','run.cLDV',typ) )#  , 6 #  , kDxT		:done
	#ctsetsets.append( auger.getctset(1e7,'run.V4ER','run.Hhup',typ) )#
	#ctsetsets.append( auger.getctset(1e6,'run.zE43','run.MUoq',typ) )# 7 ,  # EdQf , 		:done
	#megaplot(ctsetsets,'spot40',[[-10.6,-7.59]])

	ctsetsets.append( auger.getctset(1e9,'run.kVk7','run.iias',typ) )
	ctsetsets.append( auger.getctset(1e8,'run.cj4U','run.RWsd',typ) )
	ctsetsets.append( auger.getctset(1e7,'run.ngMk','run.Ho8b',typ) )
	ctsetsets.append( auger.getctset(1e6,'run.WbDj','run.f9cL',typ) )
	megaplot(ctsetsets,'waterbox')
	
	#ctsetsets.append( auger.getctset(1e9,'run.1vRP','run.KvuV',typ) )#  , 11 #  ,  g4RC		:done
	#ctsetsets.append( auger.getctset(1e8,'run.SwIj','run.XYSQ',typ) )# 50 ,  # SwIj ,  		:done
	#ctsetsets.append( auger.getctset(1e7,'run.UAJZ','run.ebjM',typ) )
	#ctsetsets.append( auger.getctset(1e6,'run.BPnu','run.q7Vn',typ) )
	#megaplot(ctsetsets,'waterboxshifted')
	
	#compare 144MeV against shifted 139mev
	#ctsetsets.append( auger.getctset(1e9,'run.LswJ','run.KvuV',typ) )
	#ctsetsets.append( auger.getctset(1e8,'run.IdLD','run.XYSQ',typ) )
	#ctsetsets.append( auger.getctset(1e7,'run.pDRM','run.ebjM',typ) )
	#ctsetsets.append( auger.getctset(1e6,'run.pSBH','run.q7Vn',typ) )
	#megaplot(ctsetsets,'waterboxfakeshift')
	
	#ctsetsets.append( auger.getctset(27500000,'run.LUBP','run.hRZn',typ) )#spot29#
	#ctsetsets.append( auger.getctset(47300000,'run.7WZC','run.3Zs9',typ) )#spot61# 3 , 11 # s3aB, 4gLD+TWZQ		:done
	#megaplot(ctsetsets,'realspots',[[-1.75,0.291],[6.715,20.58]],['Spot 29','Spot 61'],'Spot Nr')
	
	#elay fopshift 4.3359375, geolay fopshift 6.359375
	#ctsetsets.append( auger.getctset(513093255,'run.Gi7J','run.aSej',typ) )#elay	# 0,6 # , F3gZ # +UROr 7x (4x)
	#ctsetsets.append( auger.getctset(537825202,'run.WfRk','run.F4bu',typ) )#geolay# 0,2 # , bvJG # +XJ8V 3x
	#megaplot(ctsetsets,'laygroup',[[0,4.33],[0,6.35]],['Energy Layer','Geometric Layer'],'Grouping Method')
	
	print 'Mean detection yield in',typ,'study over',sum([ctset['totnprim'] for ctset in ctsetsets]),'primaries in',sum([ctset['nreal'] for ctset in ctsetsets]),'realisations:',sum([ctset['detyieldmu'] for ctset in ctsetsets])
