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


### Yield + reldiff plot
tle_yrd = uit['tle']['std']
an_yrd = uit['analog']['std']
tle_yrd_beam = uit['tle']['beam']
an_yrd_beam = uit['analog']['beam']

tle.setprojectiondata(tle_yrd,an_yrd[max(an_yrd.keys())],'batchparodi')
tle.setprojectiondata(tle_yrd_beam,an_yrd_beam[max(an_yrd_beam.keys())],'batchparodi')

f, ((tl,tr), (ml,mr), (bl,br) ) = plt.subplots(nrows=3, ncols=2, sharex=False, sharey=False)

tle.get_yield(tl,tle_yrd,an_yrd[max(an_yrd.keys())],'Z')
tle.get_yield(tr,tle_yrd,an_yrd[max(an_yrd.keys())],'E')
tle.get_reldiff(ml,tle_yrd,'Z')
tle.get_reldiff(mr,tle_yrd,'E')
tle.get_reldiff(bl,tle_yrd_beam,'Z')
tle.get_reldiff(br,tle_yrd_beam,'E')

# tl.set_ylim([0,2.8e-3])
# tr.set_ylim([0,2.8e-3])
# ml.set_ylim([-6,6])
# mr.set_ylim([-6,6])
# bl.set_ylim([-12,12])
# br.set_ylim([-12,12])
tl.set_ylim([0,2.8e-3])
tr.set_ylim([0,2.8e-3])
ml.set_ylim([-3,3])
mr.set_ylim([-3,3])
bl.set_ylim([-6,6])
br.set_ylim([-6,6])

tl.set_ylabel('Integrated Yield\n[PG/proton/voxel]')
tl.yaxis.set_label_coords(-0.2, 0.5)#just to align on -0.2
ml.set_ylabel('Integrated\nRel. Diff.[\%]')
ml.yaxis.set_label_coords(-0.2, 0.5)#just to align on -0.2
bl.set_ylabel('Voxels beam path\nRel. Diff.[\%]')
bl.yaxis.set_label_coords(-0.2, 0.5)#just to align on -0.2
bl.set_xlabel('Depth [mm]')
br.set_xlabel('PG energy [MeV]')

lgd=tr.legend(loc='upper right', bbox_to_anchor=(1.2, 1.2),frameon=False)
[label.set_linewidth(1) for label in lgd.get_lines()]
f.subplots_adjust(hspace=0.3)
f.savefig('yield-reldiff-jm.pdf', bbox_inches='tight')
plt.close('all')


# ### yield of two boxes.
# tle_2 = uit['tle']['box2']
# an_2 = uit['analog']['box2']
# tle_8 = uit['tle']['box8']
# an_8 = uit['analog']['box8']
# tle.setprojectiondata(tle_2,an_2[max(an_2.keys())],'batchparodi')
# tle.setprojectiondata(tle_8,an_8[max(an_8.keys())],'batchparodi')

# f, (ll,lr) = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=True)
# tl = ll.twinx()
# tr = lr.twinx()

# tle.get_yield(tl,tle_2,tle_2[10000],'E')
# tle.get_yield(tr,tle_8,tle_8[10000],'E')
# tle.get_yield(ll,tle_2,an_2[max(an_2.keys())],'E')
# tle.get_yield(lr,tle_8,an_8[max(an_8.keys())],'E')

# #tl.set_ylim([1,5e2])
# #tr.set_ylim([1,5e2])

# ll.yaxis.set_label_position("right")
# lr.yaxis.set_label_position("right")
# tl.yaxis.set_label_position("left")
# tr.yaxis.set_label_position("left")

# # tl.set_title("Medium 2 (Bone)\nMedian gain: "+plot.sn(lmed2))
# # tr.set_title("Medium 8 (Muscle)\nMedian gain: "+plot.sn(lmed8))
# # tl.set_ylim([1e-1,1.1e2])
# # tr.set_ylim([1e-1,1.1e2])

# ll.yaxis.set_visible(False)
# lr.yaxis.set_visible(False)
# # tr.yaxis.set_visible(False)

# tr.plot([0],[0],color='#cccccc',linewidth=0,label='Yield (not to scale)')
# for child in ll.get_children() + lr.get_children():
# 	if isinstance(child, mpl.lines.Line2D) or isinstance(child, mpl.collections.PolyCollection):
# 		child.set_color('#cccccc')

# tl.set_ylabel('Relative Uncertainty [\%]')
# ll.set_xlabel('PG energy [MeV]')
# ll.xaxis.set_label_coords(1.1,-0.1)

# lgd = tr.legend(loc='upper right', bbox_to_anchor=(1.7, 1.),frameon=False)
# [label.set_linewidth(1) for label in lgd.get_lines()]
# f.savefig('boxes-jm.pdf', bbox_inches='tight')
# plt.close('all')


# ### Unc of two boxes.
# tle_2 = uit['tle']['box2']
# an_2 = uit['analog']['box2']
# tle_8 = uit['tle']['box8']
# an_8 = uit['analog']['box8']
# tle.setprojectiondata(tle_2,an_2[max(an_2.keys())],'batchparodi')
# tle.setprojectiondata(tle_8,an_8[max(an_8.keys())],'batchparodi')

# f, (ll,lr) = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=True)
# tl = ll.twinx()
# tr = lr.twinx()

# tle.get_unc(tl,tle_2,an_2[max(an_2.keys())],'E')
# tle.get_unc(tr,tle_8,an_8[max(an_8.keys())],'E')
# tle.get_yield(ll,tle_2,an_2[max(an_2.keys())],'E')
# tle.get_yield(lr,tle_8,an_8[max(an_8.keys())],'E')

# #tl.set_ylim([1,5e2])
# #tr.set_ylim([1,5e2])

# ll.yaxis.set_label_position("right")
# lr.yaxis.set_label_position("right")
# tl.yaxis.set_label_position("left")
# tr.yaxis.set_label_position("left")

# # tl.set_title("Medium 2 (Bone)\nMedian gain: "+plot.sn(lmed2))
# # tr.set_title("Medium 8 (Muscle)\nMedian gain: "+plot.sn(lmed8))
# # tl.set_ylim([1e-1,1.1e2])
# # tr.set_ylim([1e-1,1.1e2])

# ll.yaxis.set_visible(False)
# lr.yaxis.set_visible(False)
# # tr.yaxis.set_visible(False)

# tr.plot([0],[0],color='#cccccc',linewidth=0,label='Yield (not to scale)')
# for child in ll.get_children() + lr.get_children():
# 	if isinstance(child, mpl.lines.Line2D) or isinstance(child, mpl.collections.PolyCollection):
# 		child.set_color('#cccccc')

# tl.set_ylabel('Relative Uncertainty [\%]')
# ll.set_xlabel('PG energy [MeV]')
# ll.xaxis.set_label_coords(1.1,-0.1)

# lgd = tr.legend(loc='upper right', bbox_to_anchor=(1.7, 1.),frameon=False)
# [label.set_linewidth(1) for label in lgd.get_lines()]
# f.savefig('boxes-unc-jm.pdf', bbox_inches='tight')
# plt.close('all')


### Relunc of two boxes.
tle_2 = uit['tle']['box2']
an_2 = uit['analog']['box2']
tle_8 = uit['tle']['box8']
an_8 = uit['analog']['box8']
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


### Relunc of boxes 1,5,7
# tle_1 = uit['tle']['steplim']
tle_1 = uit['tle']['box1']
tle_2 = uit['tle']['box5']
an_2 = uit['analog']['box2']
tle_8 = uit['tle']['box7']
an_8 = uit['analog']['box8']
tle.setprojectiondata(tle_1,an_2[max(an_2.keys())],'batchparodi')
tle.setprojectiondata(tle_2,an_2[max(an_2.keys())],'batchparodi')
tle.setprojectiondata(tle_8,an_8[max(an_8.keys())],'batchparodi')

f, (sl,ll,lr) = plt.subplots(nrows=1, ncols=3, sharex=False, sharey=False)
tl = ll.twinx()
tr = lr.twinx()
tsl = sl.twinx()

tle.get_relunc(tsl,tle_1,None,'E')
tle.get_relunc(tl,tle_2,None,'E')
tle.get_relunc(tr,tle_8,None,'E')
# tle.get_yield(ll,tle_2,an_2[max(an_2.keys())],'E')
# tle.get_yield(lr,tle_8,an_8[max(an_8.keys())],'E')

# tsl.set_ylim([5e-3,5])
# tl.set_ylim([5e-3,5])
# tr.set_ylim([5e-3,5])

ll.yaxis.set_label_position("right")
lr.yaxis.set_label_position("right")
tl.yaxis.set_label_position("left")
tr.yaxis.set_label_position("left")

tsl.set_title("Medium 1 ()")
tl.set_title("Medium 5 ()")
tr.set_title("Medium 7 ()")
# tl.set_ylim([1e-1,1.1e2])
# tr.set_ylim([1e-1,1.1e2])

sl.yaxis.set_visible(False)
ll.yaxis.set_visible(False)
lr.yaxis.set_visible(False)
# tr.yaxis.set_visible(False)

sl.set_ylabel('Relative Uncertainty [\%]')
ll.set_xlabel('PG energy [MeV]')
ll.xaxis.set_label_coords(1.1,-0.1)

lgd = tr.legend(loc='upper right', bbox_to_anchor=(1.7, 1.),frameon=False)
[label.set_linewidth(1) for label in lgd.get_lines()]
f.savefig('boxes-relunc-jm-57.pdf', bbox_inches='tight')
plt.close('all')


# Save sum() to disk
# sum_d = {}
# sum_d['tle']={}
# sum_d['analog']={}
# for prims, dataa in iter(sorted(uit['tle']['sum'].iteritems())):
# 	sum_d['tle'][prims] = dataa['sum']
# for prims, dataa in iter(sorted(uit['analog']['sum'].iteritems())):
# 	sum_d['analog'][prims] = dataa['sum']
# with open("sum.pydict",'w') as thefile:
# 	pickle.dump(sum_d, thefile)