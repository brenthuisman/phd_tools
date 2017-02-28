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
	#if emisfops is not None:
		#for emisfop in emisfops:
			#emisfop[0]+=15.863
			#emisfop[1]+=15.863
	print 'FOP shift all overlaid'

	#if len(ctsets) == 4:
	if True:
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
	
	#################### DOOS WATER
	
	#ctsetsets.append( auger.getctset(1e9,'run.8ZQJ','run.ahDK',typ) )
	#ctsetsets.append( auger.getctset(1e8,'run.fhf7','run.XKeV',typ) )
	#ctsetsets.append( auger.getctset(1e7,'run.aNz9','run.NnKH',typ) )
	#ctsetsets.append( auger.getctset(1e6,'run.CZxT','run.4Sv1',typ) )
	#megaplot(ctsetsets,'waterbox')
	
	ctsetsets.append( auger.getctset(1e9,'run.8ZQJ','run.DeJf',typ) )
	ctsetsets.append( auger.getctset(1e8,'run.fhf7','run.yS7a',typ) )
	ctsetsets.append( auger.getctset(1e7,'run.aNz9','run.gKIX',typ) )
	ctsetsets.append( auger.getctset(1e6,'run.CZxT','run.PHKG',typ) )
	megaplot(ctsetsets,'waterboxshifted')
	
	###################### SPOTS TO SHIFT OR NOT TO SHIFT
	
	#ctsetsets.append( auger.getctset(1e9,'run.pMSA','run.gwKk',typ) )
	#ctsetsets.append( auger.getctset(1e9,'run.pMSA','run.Ogb8',typ) )
	#ctsetsets.append( auger.getctset(27500000,'run.aZp5','run.13px',typ) )
	#ctsetsets.append( auger.getctset(27500000,'run.aZp5','run.RKsb',typ) )
	#megaplot(ctsetsets,'spot29-shiftcomp',emisfops=None,labels=["Unaligned $4.7\cdot10^7$","Aligned $4.7\cdot10^7$","Unaligned $10^9$","Aligned $10^9$"])
	
	#ctsetsets.append( auger.getctset(1e9,'run.TtIT','run.',typ) )
	#ctsetsets.append( auger.getctset(1e8,'run.t4Fb','run.',typ) )
	#ctsetsets.append( auger.getctset(27200000,'run.YtND','run.',typ) )
	#ctsetsets.append( auger.getctset(1e7,'run.WQUJ','run.',typ) )
	#ctsetsets.append( auger.getctset(1e6,'run.ktme','run.',typ) )
	#megaplot(ctsetsets,'spot40',emisfops=None,labels=["$10^9$","$10^8$","$2.7\cdot10^7$","$10^7$","$10^6$"])
	
	#ctsetsets.append( auger.getctset(47300000,'run.R9KU','run.rTUp',typ) )
	#ctsetsets.append( auger.getctset(47300000,'run.R9KU','run.TOku',typ) )
	#ctsetsets.append( auger.getctset(1e9,'run.EYBe','run.6HvZ',typ) )
	#ctsetsets.append( auger.getctset(1e9,'run.EYBe','run.9fc1',typ) )
	#megaplot(ctsetsets,'spot61-shiftcomp',emisfops=None,labels=["Unaligned $4.7\cdot10^7$","Aligned $4.7\cdot10^7$","Unaligned $10^9$","Aligned $10^9$"])
	
	##################### SPOTS ZONDER RPCT SHIFT
	
	#ctsetsets.append( auger.getctset(1e9,'run.pMSA','run.gwKk',typ) )
	#ctsetsets.append( auger.getctset(1e8,'run.GJHJ','run.9BY9',typ) )
	#ctsetsets.append( auger.getctset(27500000,'run.aZp5','run.13px',typ) )
	#ctsetsets.append( auger.getctset(1e7,'run.EPjL','run.jNjK',typ) )
	#ctsetsets.append( auger.getctset(1e6,'run.yUVZ','run.qFFa',typ) )
	#megaplot(ctsetsets,'spot29',emisfops=None,labels=["$10^9$","$10^8$","$2.7\cdot10^7$","$10^7$","$10^6$"])
	
	#ctsetsets.append( auger.getctset(1e9,'run.TtIT','run.SmHn',typ) )
	#ctsetsets.append( auger.getctset(1e8,'run.t4Fb','run.w9Te',typ) )
	#ctsetsets.append( auger.getctset(27200000,'run.YtND','run.SQy4',typ) )
	#ctsetsets.append( auger.getctset(1e7,'run.WQUJ','run.JJQQ',typ) )
	#ctsetsets.append( auger.getctset(1e6,'run.ktme','run.uvCa',typ) )
	#megaplot(ctsetsets,'spot40',emisfops=None,labels=["$10^9$","$10^8$","$2.7\cdot10^7$","$10^7$","$10^6$"])
	
	#ctsetsets.append( auger.getctset(1e9,'run.EYBe','run.6HvZ',typ) )
	#ctsetsets.append( auger.getctset(1e8,'run.W3sR','run.q7v2',typ) )
	#ctsetsets.append( auger.getctset(47300000,'run.R9KU','run.rTUp',typ) )
	#ctsetsets.append( auger.getctset(1e7,'run.1jXf','run.8NDz',typ) )
	#ctsetsets.append( auger.getctset(1e6,'run.FvO2','run.05U8',typ) )
	#megaplot(ctsetsets,'spot61',emisfops=None,labels=["$10^9$","$10^8$","$4.7\cdot10^7$","$10^7$","$10^6$"])
	
	############ LAGEN
	
	#ctsetsets.append( auger.getctset(27500000,'run.LUBP','run.hRZn',typ) )#spot29#
	#ctsetsets.append( auger.getctset(47300000,'run.7WZC','run.3Zs9',typ) )#spot61# 3 , 11 # s3aB, 4gLD+TWZQ		:done
	#megaplot(ctsetsets,'realspots',[[-1.75,0.291],[6.715,20.58]],['Spot 29','Spot 61'],'Spot Nr')
	
	#elay fopshift 4.3359375, geolay fopshift 6.359375
	#ctsetsets.append( auger.getctset(513093255,'run.Gi7J','run.aSej',typ) )#elay	# 0,6 # , F3gZ # +UROr 7x (4x)
	#ctsetsets.append( auger.getctset(537825202,'run.WfRk','run.F4bu',typ) )#geolay# 0,2 # , bvJG # +XJ8V 3x
	#megaplot(ctsetsets,'laygroup',[[0,4.33],[0,6.35]],['Energy Layer','Geometric Layer'],'Grouping Method')
	
	print 'Mean detection yield in',typ,'study over',sum([ctset['totnprim'] for ctset in ctsetsets]),'primaries in',sum([ctset['nreal'] for ctset in ctsetsets]),'realisations:',sum([ctset['meandetyield'] for ctset in ctsetsets])
