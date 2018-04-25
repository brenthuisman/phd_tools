#!/usr/bin/env python
import numpy as np,plot,auger

#OPT: quickly get sorted rundirs
# zb autogen | sort -k1.13 -r

#OPT: fix seed
#np.random.seed(65983247)

#we dont know what the added or reduced noise level is when changing energy windows, so we cant compare performance for ipnl3 and iba1.
typs=['ipnl-auger-tof-1.root','iba-auger-tof-1.root']

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
	
	ctsetsets.append( auger.getctset(1e9,'1e9','1e9',typ) )
	ctsetsets.append( auger.getctset(1e8,'1e8','1e8',typ) )
	ctsetsets.append( auger.getctset(1e7,'1e7','1e7',typ) )
	ctsetsets.append( auger.getctset(1e6,'1e6','1e6',typ) )
	#ctsetsets.append( auger.getctset(1e9,'run.3poV','run.wucX',typ) )
	#ctsetsets.append( auger.getctset(1e8,'run.1XRe','run.lTdI',typ) )
	#ctsetsets.append( auger.getctset(1e7,'run.oPE7','run.RWkp',typ) )
	#ctsetsets.append( auger.getctset(1e6,'run.7bG6','run.pijb',typ) )
	megaplot(ctsetsets,'waterbox')
	
	print 'Mean detection yield in',typ,'study over',sum([ctset['totnprim'] for ctset in ctsetsets]),'primaries in',sum([ctset['nreal'] for ctset in ctsetsets]),'realisations:',sum([ctset['meandetyield'] for ctset in ctsetsets])
