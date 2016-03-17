#!/usr/bin/env python
import os,glob2 as glob,sys,matplotlib as mpl,matplotlib.pyplot as plt,numpy as np,pickle,tle,plot
from scipy.stats import norm

'''
## Wat moet er gebeuren?


'''

sources = glob.glob("./**/*.pylist")#,recursive=True
if len(sources) < 2:
	print "None or one file found, exiting..."
	sys.exit()

nr = len(sources)

print nr, "files found:", sources[:3], '...', sources[-3:]

data_singleton = {}

# Load up

for fp in sources:
	row = {}
	row['data'] = [pickle.load(open(fp))] #list of lists

	dn,fn=os.path.split(fp)

	#parodi tle
	if 'run.UzFE' in fp:
		row['nprim'] = int(1e4)
		row['type'] = 'tle'
		#'steplim'
		# continue
	if 'run.ASZg' in fp:
		row['nprim'] = int(1e5)
		row['type'] = 'tle'
		#'steplim'
		# continue
	if 'run.Yr1h' in fp:
		row['nprim'] = int(1e5)
		row['type'] = 'tle'
		#'steplim'
		# continue
	if 'run.ERzl' in fp:
		row['nprim'] = int(1e5)
		row['type'] = 'tle'
		#'steplim'
		continue
	if 'run.R75J' in fp:
		row['nprim'] = int(1e5)
		row['type'] = 'tle'
		#'steplim'
		continue

	if 'run.ZJsX' in fp:
		row['nprim'] = int(1e3)
		row['type'] = 'tle'
	if 'run.Rhxd' in fp:
		row['nprim'] = int(1e4)
		row['type'] = 'tle'
	if 'run.9Odj' in fp:
		row['nprim'] = int(1e5)
		row['type'] = 'tle'
	if 'run.GTKJ' in fp:
		row['nprim'] = int(1e6)
		row['type'] = 'tle'

	if 'run.3Mtt' in fp:
		row['nprim'] = int(1e3)
		row['type'] = 'tle'
		
	if 'run.MkUk' in fp:
		row['nprim'] = int(1e3)
		row['type'] = 'tle'
	if 'run.R75J' in fp:
		row['nprim'] = int(1e4)
		row['type'] = 'tle'
		# continue
	if 'run.iegm' in fp:
		row['nprim'] = int(1e5)
		row['type'] = 'tle'
		# continue
	if 'run.1HQI' in fp:
		row['nprim'] = int(1e6)
		row['type'] = 'tle'
	#parodi analog
	if 'run.tlzH' in fp:
		row['nprim'] = int(1e6)
		row['type'] = 'analog'
	if 'run.N4Ul/output' in fp:
		row['nprim'] = int(1e7)
		row['type'] = 'analog'
	if 'run.N4Ul/group10' in fp:
		row['nprim'] = int(1e8)
		row['type'] = 'analog'
	if 'run.cym5' in fp:
		row['nprim'] = int(1e9)
		row['type'] = 'analog'

	#axes
	if 'Z.' in fn:
		row['axis'] = 'Z'
	if 'Y.' in fn:
		row['axis'] = 'Y'
	if 'E.' in fn:
		row['axis'] = 'E'
	if 'X.' in fn:
		row['axis'] = 'X'

	#masks
	if 'sum' in fn:
		row['mask'] = 'sum'
		row['axis'] = 'sum'
		row['data'] = [row['data']]
	if 'nofilter' in fn:
		row['mask'] = 'nofilter'
	if 'beam' in fn:
		row['mask'] = 'beam'
	if 'std' in fn:
		row['mask'] = 'std'
	if 'box2' in fn:
		row['mask'] = 'box2'
	if 'box1' in fn:
		row['mask'] = 'box1'
	if 'box5' in fn:
		row['mask'] = 'box5'
	if 'box7' in fn:
		row['mask'] = 'box7'
	if 'box8' in fn:
		row['mask'] = 'box8'
	# if 'run.UzFE' in fp:
	# 	row['mask'] = 'steplim'
	# if 'run.ASZg' in fp:
	# 	row['mask'] = 'steplim'

	row['plotgroup'] = row['type']+row['axis']+row['mask']+str(row['nprim'])
	
	if row['plotgroup'] not in data_singleton.keys():
		data_singleton[row['plotgroup']] = row
	else:
		data_singleton[row['plotgroup']]['data'].extend(row['data'])

# convert batch data into mu,variance
for key, value in data_singleton.iteritems():
	#key is plotgroup, value is row
	data = np.array(value['data'])
	data = np.rollaxis(data,1)

	value['yield'] = []
	value['var'] = []

	for binn in data:
		# N=float(len(binn))
		# mu=sum(binn)/N
		# sqbinn=[(i-mu)**2 for i in binn]
		# var= ( sum(sqbinn) ) / (N*(N-1)) # Walters 2002/Chetty 2006
		# var= ( sum(sqbinn) ) / (N-1) # WE MUST REMOVE 1 N FACTOR, BECAUSE WE LOOK AT YIELD, NOT COUNT

		# # var = sum-of-squares/# - sq(sum/#)
		# # var = ( sum([i**2 for i in binn]) / N ) - ( (mu)**2 ) #JM!!!

		# value['yield'].append(mu)
		# value['var'].append(var)

		(mu, sigma) = norm.fit(binn) #returns actually sigma
		value['yield'].append(mu)
		value['var'].append(sigma**2)

		# 4 options to compute var tested:
		# - JM and Python: same result
		# - Walter and Chetty: same result
		# if we remove a factor N from Walter/Chetty, all results are the same
		# WE MUST REMOVE 1 N FACTOR, BECAUSE WE LOOK AT YIELD, NOT COUNT

	value['data'] = None #save some space when printing

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



### Relunc of two boxes.
tle_2 = uit['tle']['box2']
an_2 = uit['tle']['box2']
tle_8 = uit['tle']['box8']
an_8 = uit['tle']['box8']
tle.setprojectiondata(tle_2,an_2[max(an_2.keys())],'batchparodi')
tle.setprojectiondata(tle_8,an_8[max(an_8.keys())],'batchparodi')

f, (ll,lr) = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
tl = ll.twinx()
tr = lr.twinx()

tle.get_relunc(tl,tle_2,an_2[max(an_2.keys())],'E')
tle.get_relunc(tr,tle_8,an_8[max(an_8.keys())],'E')
tle.get_yield(ll,tle_2,an_2[max(an_2.keys())],'E')
tle.get_yield(lr,tle_8,an_8[max(an_8.keys())],'E')

tl.set_ylim([1e-2,5])
tr.set_ylim([1e-2,5])

ll.yaxis.set_label_position("right")
lr.yaxis.set_label_position("right")
tl.yaxis.set_label_position("left")
tr.yaxis.set_label_position("left")

tl.set_title("Medium 2 (Bone)")
tr.set_title("Medium 8 (Muscle)")
# tl.set_ylim([1e-1,1.1e2])
# tr.set_ylim([1e-1,1.1e2])

ll.yaxis.set_visible(False)
lr.yaxis.set_visible(False)
# tr.yaxis.set_visible(False)

tr.plot([0],[0],color='#cccccc',linewidth=0,label='Yield (not to scale)')
for child in ll.get_children() + lr.get_children():
	if isinstance(child, mpl.lines.Line2D) or isinstance(child, mpl.collections.PolyCollection):
		child.set_color('#cccccc')

tl.set_ylabel('Relative Uncertainty [\%]')
ll.set_xlabel('PG energy [MeV]')
ll.xaxis.set_label_coords(1.1,-0.1)

lgd = tr.legend(loc='upper right', bbox_to_anchor=(1.7, 1.),frameon=False)
[label.set_linewidth(1) for label in lgd.get_lines()]
f.savefig('boxes-relunc-jm.pdf', bbox_inches='tight')
plt.close('all')

