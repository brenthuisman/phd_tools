#!/usr/bin/env python
import os,sys,matplotlib as mpl,matplotlib.pyplot as plt,numpy as np
from scipy.stats import norm

sources = glob.glob("./**/*.mhd")#,recursive=True
if len(sources) < 2:
	print "None or one file found, exiting..."
	sys.exit()

nr = len(sources)

print nr, "files found:", sources[:3], '...', sources[-3:]

data_singleton = {}

# Load up

for fp in sources:
	if 'gatesim50' not in fp:
		continue #skip

	if 'source.mhd' in fp:
		row['imtype'] = 'pg'
	elif 'dosedist-Dose.mhd' in fp:
		row['imtype'] = 'dose'
	elif 'dosedist-Dose-Squared.mhd' in fp:
		row['imtype'] = 'dosevar'
	else:
		continue #skip

	dn,fn=os.path.split(fp)

	row = {}
	row['image'] = image.image(fp)

	dn,fn=os.path.split(fp)

	if 'RPCT' in fp:
		row['ct'] = 'replan'
	else:
		row['ct'] = 'orig'

	if 'layer' in fp:
		row['loc'] = 'layer'
	elif 'spot' in fp:
		row['loc'] = 'spot'
	else:
		row['loc'] = 'full'

	#if 'source.mhd' in fp and 'result' in dn:
		#the PG images have been added, need to be scaled.
		#row['image'].imdata = 0.1*row['image'].imdata

	#axes TODO add X,Y?
	if 'Z.' in fn:
		row['axis'] = 'Z'
	if 'Y.' in fn:
		row['axis'] = 'Y'
	if 'E.' in fn:
		row['axis'] = 'E'
	if 'X.' in fn:
		row['axis'] = 'X'

	#masks
	if 'nofilter' in fn:
		row['mask'] = 'nofilter'
	if 'beam' in fn:
		row['mask'] = 'beam'
	if 'std' in fn:
		row['mask'] = 'std'
	if 'box2' in fn:
		row['mask'] = 'box2'
	if 'box8' in fn:
		row['mask'] = 'box8'

	row['plotgroup'] = row['type']+row['axis']+row['mask']+str(row['nprim'])
	
	if row['plotgroup'] not in data_singleton.keys():
		data_singleton[row['plotgroup']] = row
	else:
		data_singleton[row['plotgroup']]['data'].extend(row['data'])

crush = [0,1,1,1]
infile = sys.argv[-1] #in goes mhd
outpostfix = ".x"

print >> sys.stderr, 'Processing', infile

img = image.image(infile)
img.saveprojection(outpostfix, crush)


# convert batch data into mu,variance
for key, value in data_singleton.iteritems():
	#key is plotgroup, value is row
	data = np.array(value['data'])
	#data = data.reshape(data.shape[::-1])
	data = np.rollaxis(data,1)

	value['yield'] = []
	value['var'] = []

	for binn in data:
		# plt.plot(binn)
		# plt.show()

		# N=float(len(binn))
		# mu=sum(binn)/N
		# sqbinn=[(i-mu)**2 for i in binn]
		# var= ( sum(sqbinn) ) / (N*(N-1))
		# value['yield'].append(mu)
		# value['var'].append(var)

		(mu, sigma) = norm.fit(binn) #returns actually sigma
		value['yield'].append(mu)
		value['var'].append(sigma**2)

		# (mu, sigma) = norm.fit(binn) #returns actually sigma
		# value['yield'].append(mu)
		# value['var'].append(sigma**2)
	value['data'] = None #save some space when printing
# print data_singleton[data_singleton.keys()[0]]['datamu']
# print 'brent',len(data_singleton['analogEbeam1000000']['yield'])
# sys.exit()


# convert to object usable with tle.plt
uit = {}
for key, value in data_singleton.iteritems():
	# we moeten toe naar data_singleton['prims']['Z']['yield']
	# extra tussenstapje: data_singleton['analog']['mask']['prims']['Z']['yield']

	if value['type'] not in uit.keys():
		uit[value['type']] = {}
	typ = uit[value['type']]
	if value['mask'] not in typ.keys():
		typ[value['mask']] = {}
	mskset = typ[value['mask']]
	if value['nprim'] not in mskset.keys():
		mskset[value['nprim']] = {}
	nprimset = mskset[value['nprim']]
	if value['axis'] not in nprimset.keys():
		nprimset[value['axis']] = {}
	axset = nprimset[value['axis']]

	axset['yield'] = value['yield']
	axset['var'] = value['var']


### Yield + reldiff plot
tle_yrd = uit['tle']['std']
an_yrd = uit['analog']['std']
#print an_yrd[1000000].keys()
tle.setprojectiondata(tle_yrd,an_yrd[max(an_yrd.keys())],'batchhead')

f, ((tl,tr), (ml,mr) ) = plt.subplots(nrows=2, ncols=2, sharex=False, sharey=False)

tle.get_yield(tl,tle_yrd,an_yrd[max(an_yrd.keys())],'Y','head')
tle.get_yield(tr,tle_yrd,an_yrd[max(an_yrd.keys())],'E','head')
tle.get_reldiff(ml,tle_yrd,'Y','head')
tle.get_reldiff(mr,tle_yrd,'E','head')

# tl.xaxis.set_visible(False)
# tr.xaxis.set_visible(False)
# tr.yaxis.set_visible(False)
# ml.xaxis.set_visible(False)
# mr.xaxis.set_visible(False)
# mr.yaxis.set_visible(False)
#f.text(.5, 1, 'vpgTLE prompt gamma yield for patient CT + proton plan\nand relative difference w.r.t. analog reference simulation', horizontalalignment='center').set_size(16)

# tl.set_title("Yield and \nRel. Diff. w.r.t. Reference\n(along beam)")
# tr.set_title("Yield and \nRel. Diff. w.r.t. Reference\n(spectral)")
tl.set_ylim([0,2.1e-3])
tr.set_ylim([0,2.1e-3])
# ml.set_ylim([-25,25])
# mr.set_ylim([-25,25])
# bl.set_ylim([-25,25])
# br.set_ylim([-25,25])
ml.set_ylim([-3,3])
mr.set_ylim([-3,3])

tl.set_ylabel('Integrated Yield\n[PG/proton/bin]')
tl.yaxis.set_label_coords(-0.2, 0.5)#just to align on -0.2
ml.set_ylabel('Integrated\nRel. Diff.[\%]')
ml.yaxis.set_label_coords(-0.2, 0.5)#just to align on -0.2
ml.set_xlabel('Depth [mm]')
mr.set_xlabel('PG energy [MeV]')

lgd=tr.legend(loc='upper right', bbox_to_anchor=(1.2, 1.2),frameon=False)
[label.set_linewidth(1) for label in lgd.get_lines()]
f.subplots_adjust(hspace=0.3)
f.savefig('yield-reldiff-jm.pdf', bbox_inches='tight')
f.savefig('yield-reldiff-jm.png', bbox_inches='tight',dpi=300)
plt.close('all')


### Relunc
f, (tl,tr) = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=True)

tle.get_relunc(tl,tle_yrd,an_yrd[max(an_yrd.keys())],'Y','head')
tle.get_relunc(tr,tle_yrd,an_yrd[max(an_yrd.keys())],'E','head')

tl.set_title("Relative uncertainty (along beam)")
tr.set_title("Relative uncertainty (spectral)")
# tl.set_ylim([1e-1,1.1e2])
# tr.set_ylim([1e-1,1.1e2])

tr.set_ylabel('Relative Uncertainty [\%]')
tr.set_xlabel('PG energy [MeV]')
tl.set_xlabel('Depth [mm]')
#tl.xaxis.set_label_coords(1.1,-0.1)

lgd = tr.legend(loc='upper right', bbox_to_anchor=(1.7, 1.),frameon=False)
[label.set_linewidth(1) for label in lgd.get_lines()]
f.savefig('relunc-jm.pdf', bbox_inches='tight')
f.savefig('relunc-jm.png', bbox_inches='tight',dpi=300)
plt.close('all')
