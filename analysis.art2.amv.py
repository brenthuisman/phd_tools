#!/usr/bin/env python

############################################################################################################
################################# DEZE FILE IS VOOR AMV. ENKEL 1MEV dus
############################################################################################################

import numpy as np,plot,auger,subprocess,tableio,dump,math
from matplotlib.ticker import AutoMinorLocator

#OPT: quickly get sorted rundirs
# zb autogen | sort -k1.13 -r

#OPT: fix seed
#np.random.seed(65983247)
#np.random.seed(9832324)
addnoise=False #false for all AMV
precolli=False #gaan we niet meer doen
pgexit = False #idem



print 'Computing pgprod ratios...'

pgprod_1mev_ipnl = 0.07547789 #obatined with image.sum on source image with first mev taken out
pgprod_1mev_iba = 0.029948339 #idem, but iba_source image where up to -5cm from fop voxels were zeroed

print 'done.'

resultstable=[["typ","nprim","fopmu","fopsigma","fow","contrast","detyieldmu","detyieldsigma","detcount","detcount/prod"]]
if precolli:
	resultstable[0].extend(["collieffmu","collieffsigma"])

def megaplot(ctsets,studyname,emisfops=None,labels=["$10^9$","$10^8$","$10^7$","$10^6$"],axlabel='Primaries [nr]'):

	# print 'FOP FOW Contrast DE averages over 10e9 ctset'
	# removed 2nd deriv from plot

	f, (ax1,ax2) = plot.subplots(nrows=2, ncols=1, sharex=False, sharey=False)
	x=ctsets[0]['ct']['x']
	y=ctsets[0]['ct']['av']
	if 'iba' in ctsets[0]['name']: # ctset['name'] == typ
		mm=4/0.8
	if 'ipnl' in ctsets[0]['name']:
		mm=8
	falloff_pos,g_fwhm,contrast = auger.get_fop_fow_contrast(x,y,plot='wut',ax=ax1,ax2=ax2,smooth=0.2,filename=ctsets[0]['ct']['path'],contrast_divisor=ctsets[0]['nprim']*len(ctsets[0]['ct']['files'])*mm,fitlines=False)

	# some cosmetics
	maxyrounded = int(math.ceil(max(y) / 100.0)) * 100
	ticks = np.arange(0, maxyrounded, 100)
	if len(ticks)>10:
		ticks = np.arange(0, maxyrounded+100, 200)
	if len(ticks)>10:
		ticks = np.arange(0, maxyrounded+200, 400)
	ax1.set_yticks(ticks)

	minor_locator = AutoMinorLocator(2)
	minor_locator1 = AutoMinorLocator(2)
	ax1.xaxis.set_minor_locator(minor_locator)
	ax2.xaxis.set_minor_locator(minor_locator)
	ax2.yaxis.set_minor_locator(minor_locator1)


	print "NPRIM", ctsets[0]['nprim'],"NJOBS",len(ctsets[0]['ct']['files']),"MM",mm

	#gebruiken deze falloff_pos niet. we doen contrast en fow over de average van 50 batches wegens smoothe curve. daardoor geen sigma

	f.savefig(studyname+'-'+typ+str(ctsets[0]['nprim'])+'-FOW.pdf', bbox_inches='tight')
	plot.close('all')

	#############################################################################################

	# results table

	for ctset in ctsets:
		res=[typ,ctset['nprim'],ctset['ct']['fopmu'],ctset['ct']['fopsigma'],g_fwhm,contrast,ctset['detyieldmu'],ctset['detyieldsigma'],ctset['detcount'],ctset['detcount']]

		if ctset['nprim'] == 10**9:
			if 'iba' in typ:
				#res.append(pgprod_1mev_iba*ctset['nprim'])
				res[-1]=res[-1]/(pgprod_1mev_iba*ctset['nprim'])
			if 'ipnl' in typ:
				#res.append(pgprod_1mev_ipnl*ctset['nprim'])
				res[-1]=res[-1]/(pgprod_1mev_ipnl*ctset['nprim'])
		else:
			res[-1]=''

		if precolli:
			res.extend([ctset['precollidetyieldmu'],ctset['precollidetyieldsigma']])

		resultstable.append(res)

	#############################################################################################

	from mpl_toolkits.mplot3d import Axes3D
	import matplotlib.pyplot as plt

	print 'FOP distributions'

	fig = plt.figure()
	ax1 = plt.axes(projection='3d')
	ax1.view_init(30, -50)

	for i,ctset in enumerate(ctsets):
		auger.plotfodist_CTONLY(ax1,ctset,i,emisfops,labels,axlabel)

	# plt.legend()#shadow = True,frameon = True,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'lower right')

	# plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
	plt.savefig(studyname+'-'+typ+'-FOP-dist.pdf')#, bbox_inches='tight')
	plt.close('all')

# nu gaan we drie studies doen!
# 1: perabsorber en perfect colli. typ=*-perdet, dirs: kill
# 2: perabsorber en physical colli. typ=*-perdet, dirs: zonder kill
# 3: physical absorber en perfect colli. typ=*-auger-notof-1.root, dirs: kill

print("######################### 111111111111111111111111111111111111111111111111111")

resultstable.append(["perabs-percolli"]*len(resultstable[-1]))

dirs = subprocess.check_output(['find . -iname "*autogen*kill*" | sort -k1.13'],shell=True).split('\n')[:-1]
dirs = dirs[0:2] #only 10e9

print(dirs)
numprots = [1e9,1e9,1e8,1e8,1e7,1e7]

typ=None
for dirr,numprot in zip(dirs,numprots):
	#if numprot != 1e9:
		#continue
	ctsetsets = []
	if 'iba' in dirr:
		typ='iba-perdet.root'
		ctsetsets.append( auger.getctset(numprot,dirr[2:10],None,typ,addnoise=addnoise) )

	if 'ipnl' in dirr:
		typ='ipnl-perdet.root'
		ctsetsets.append( auger.getctset(numprot,dirr[2:10],None,typ,addnoise=addnoise) )

	megaplot(ctsetsets,'perdet-percolli')
	print 'Mean detection yield in',typ,'study over',sum([ctset['totnprim'] for ctset in ctsetsets]),'primaries in',sum([ctset['nreal'] for ctset in ctsetsets]),'realisations:',sum([ctset['detyieldmu'] for ctset in ctsetsets])

#tableio.print2d(resultstable)
#tableio.write(resultstable,'perabs-percolli.tsv')

print("######################### 2222222222222222222222222222222222222222222222222222222222")

resultstable.append(["perabs-physcolli"]*len(resultstable[-1]))

dirs = subprocess.check_output(['find . -iname "*autogen*ibazinv.mac" | sort -k1.13'],shell=True).split('\n')[:-1]
dirs += subprocess.check_output(['find . -iname "*autogen*ipnllyso.mac" | sort -k1.13'],shell=True).split('\n')[:-1]

print(dirs)
numprots = [1e9,1e9]

typ=None
for dirr,numprot in zip(dirs,numprots):
	if numprot != 1e9:
		continue
	ctsetsets = []
	if 'iba' in dirr:
		typ='iba-perdet.root'
		ctsetsets.append( auger.getctset(numprot,dirr[2:10],None,typ,addnoise=addnoise) )

	if 'ipnl' in dirr:
		typ='ipnl-perdet.root'
		ctsetsets.append( auger.getctset(numprot,dirr[2:10],None,typ,addnoise=addnoise) )

	megaplot(ctsetsets,'perdet-physcolli')
	print 'Mean detection yield in',typ,'study over',sum([ctset['totnprim'] for ctset in ctsetsets]),'primaries in',sum([ctset['nreal'] for ctset in ctsetsets]),'realisations:',sum([ctset['detyieldmu'] for ctset in ctsetsets])

#tableio.print2d(resultstable)
#tableio.write(resultstable,'perabs-physcolli.tsv')


print("############################ 333333333333333333333333333333333333333333333")

resultstable.append(["physabs-percolli"]*len(resultstable[-1]))

typs=['ipnl-auger-notof-1.root','iba-auger-notof-1.root']

dirs = subprocess.check_output(['find . -iname "*autogen*NPRIM-1000000000*kill*" | sort -k1.13'],shell=True).split('\n')[:-1]

print(dirs)
numprots = [1e9,1e9]

for typ in typs:
    ctsetsets = []
    for line,numprot in zip(dirs,[item for item in numprots for i in range(len(typs)/len(numprots))]):
        for haha in ['iba','ipnl']:
            if (haha+'lyso' in line or haha+'bgo' in line) and haha+'-' in typ:
                print (haha,line,typ,numprot)
                ctsetsets.append( auger.getctset(numprot,line[2:10],None,typ,addnoise=addnoise,precolli=precolli) )
            if haha+'zinv' in line and haha+'-' in typ:
                print (haha,line,typ,numprot)
                ctsetsets.append( auger.getctset(numprot,line[2:10],None,typ,addnoise=addnoise,precolli=precolli) )
    #assert(len(ctsetsets)==3)
    megaplot(ctsetsets,'physabs-percolli')
    print 'Mean detection yield in',typ,'study over',sum([ctset['totnprim'] for ctset in ctsetsets]),'primaries in',sum([ctset['nreal'] for ctset in ctsetsets]),'realisations:',sum([ctset['detyieldmu'] for ctset in ctsetsets])

print("############################ 44444444444444444444444444444444")

resultstable.append(["physabs-physcolli"]*len(resultstable[-1]))

typs=['ipnl-auger-notof-1.root','iba-auger-notof-1.root']

dirs = [x for x in subprocess.check_output(['find . -iname "*autogen*NPRIM-1000000000*" | sort -k1.13'],shell=True).split('\n')[:-1] if '.kill.' not in x]

print(dirs)
numprots = [1e9,1e9]

for typ in typs:
    ctsetsets = []
    for line,numprot in zip(dirs,[item for item in numprots for i in range(len(typs)/len(numprots))]):
        for haha in ['iba','ipnl']:
            if (haha+'lyso' in line or haha+'bgo' in line) and haha+'-' in typ:
                print (haha,line,typ,numprot)
                ctsetsets.append( auger.getctset(numprot,line[2:10],None,typ,addnoise=addnoise,precolli=precolli) )
            if haha+'zinv' in line and haha+'-' in typ:
                print (haha,line,typ,numprot)
                ctsetsets.append( auger.getctset(numprot,line[2:10],None,typ,addnoise=addnoise,precolli=precolli) )
    #assert(len(ctsetsets)==3)
    megaplot(ctsetsets,'physabs-physcolli')
    print 'Mean detection yield in',typ,'study over',sum([ctset['totnprim'] for ctset in ctsetsets]),'primaries in',sum([ctset['nreal'] for ctset in ctsetsets]),'realisations:',sum([ctset['detyieldmu'] for ctset in ctsetsets])


tableio.print2d(resultstable)
tableio.write(resultstable,'results.tsv')
