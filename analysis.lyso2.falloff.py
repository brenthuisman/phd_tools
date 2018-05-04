#!/usr/bin/env python
import numpy as np,plot,auger,subprocess

#OPT: quickly get sorted rundirs
# zb autogen | sort -k1.13 -r

#OPT: fix seed
#np.random.seed(65983247)


def megaplot(ctsets,studyname,emisfops=None,labels=["$10^9$","$10^8$","$10^7$","$10^6$"],axlabel='Primaries [nr]'):

	if len(ctsets) == 4:
		f, ((ax1,ax2),(ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

		auger.plot_all_ranges_CTONLY(ax1,ctsets[0])
		auger.plot_all_ranges_CTONLY(ax2,ctsets[1])
		auger.plot_all_ranges_CTONLY(ax3,ctsets[2])
		auger.plot_all_ranges_CTONLY(ax4,ctsets[3])
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

	# print 'FOP shift distributions'

	# from mpl_toolkits.mplot3d import Axes3D
	# import matplotlib.pyplot as plt

	# fig = plt.figure()
	# ax1 = plt.axes(projection='3d')
	# ax1.view_init(30, -50)

	# for i,ctset in enumerate(ctsets):
	# 	auger.plotfodiffdist(ax1,ctset,i,emisfops,labels,axlabel)
	# 	if not emisfops == None:
	# 		fopshifts=[]
	# 		for fopset in emisfops:
	# 			fopshifts.append( fopset[-1]-fopset[0] )
	# 		ax1.set_xlim3d(np.mean(fopshifts)-20,np.mean(fopshifts)+20)
	# if emisfops is not None and len(emisfops) == 1:
	# 	ax1.set_title(studyname+', $Shift_{em}$ = '+str(emisfops[0][-1]-emisfops[0][0]), y=1.08)

	# #plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
	# fig.savefig(studyname+'-'+typ+'-FOP-shift.pdf')#, bbox_inches='tight')
	# plt.close('all')


	f, (ax1,ax2,ax3) = plot.subplots(nrows=3, ncols=1, sharex=False, sharey=False)

	x=ctsets[0]['rpct']['x']
	y=ctsets[0]['ct']['av']
	auger.get_fow(x,y,plot='wut',ax=ax1,ax2=ax2,ax3=ax3)
    # ax1.set_title('FOP = '+str(falloff_pos), fontsize=8)
	f.savefig(studyname+'-'+typ+'-FOW.pdf', bbox_inches='tight')
	plot.close('all')

	#############################################################################################

	from mpl_toolkits.mplot3d import Axes3D
	import matplotlib.pyplot as plt

	print 'FOP distributions'

	fig = plt.figure()
	ax1 = plt.axes(projection='3d')
	ax1.view_init(30, -50)

	for i,ctset in enumerate(ctsets):
		auger.plotfodist_CTONLY(ax1,ctset,i,emisfops,labels,axlabel)
	if emisfops is not None and len(emisfops) == 1:
		ax1.set_title(studyname+', $CT_{FOP_{em}}$ = '+str(emisfops[0][0])[:5]+', $RPCT_{FOP_{em}}$ = '+str(emisfops[0][1])[:5], y=1.08)

	#plt.legend()#shadow = True,frameon = True,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'lower right')

	#plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
	plt.savefig(studyname+'-'+typ+'-FOP-dist.pdf')#, bbox_inches='tight')
	plt.close('all')

typs=['ipnl-auger-tof-1.root','iba-auger-tof-1.root','ipnl-auger-notof-1.root','iba-auger-notof-1.root','ipnl-auger-tof-3.root','iba-auger-tof-3.root','ipnl-auger-notof-3.root','iba-auger-notof-3.root']

# typs=['ipnl-auger-tof-1.root','iba-auger-tof-1.root','ipnl-auger-notof-3.root','iba-auger-notof-3.root']
dirs = subprocess.check_output(['find . -iname *autogen* | sort -k1.13'],shell=True).split('\n')[:-1]

numprots = [1e9,1e8,1e7,1e6]

for typ in typs:
    ctsetsets = []
    for line,numprot in zip(dirs,[item for item in numprots for i in range(2)]):
        for haha in ['iba','ipnl']:
            if haha in line and haha in typ:
                ctsetsets.append( auger.getctset(numprot,line[2:10],line[2:10],typ) )
    assert(len(ctsetsets)==4)
    megaplot(ctsetsets,'PMMA_phantom')
    print 'Mean detection yield in',typ,'study over',sum([ctset['totnprim'] for ctset in ctsetsets]),'primaries in',sum([ctset['nreal'] for ctset in ctsetsets]),'realisations:',sum([ctset['meandetyield'] for ctset in ctsetsets])
