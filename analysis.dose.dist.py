#!/usr/bin/env python
import os,sys,matplotlib as mpl,matplotlib.pyplot as plt,numpy as np,plot,glob2 as glob,image

sources = glob.glob("./**/*.mhd")#,recursive=True
if len(sources) < 2:
	print "None or one file found, exiting..."
	sys.exit()

nr = len(sources)

print nr, "files found:", sources[:3], '...', sources[-3:]

data_singleton = {}

N=100.*100.
# Load up
for fp in sources:
	if 'gatesim50' not in fp:
		continue #skip

	dn,fn=os.path.split(fp)

	row = {}
	row['replan'] = {}
	row['orig'] = {}

	im=image.image(fp)

	ct = None
	ctname=None
	if 'RPCT' in fp:
		ctname='replan'
		ct = row['replan'] #pointer
	else:
		ctname='orig'
		ct = row['orig'] #pointer

	if 'source.mhd' in fp:
		ct['type'] = 'pg'
		ct['pg'] = im.get1dlist([0,1,1,1])
		# if N == None:
		# 	N = im.header['NDims']#/len(ct['pg'])
		# 	print N
	elif 'dosedist-Dose.mhd' in fp:
		ct['type'] = 'dose'
		ct['dose'] = im.get1dlist([0,1,1]) #dose is 3D,removed last index
	elif 'dosedist-Dose-Squared.mhd' in fp:
		ct['type'] = 'dosesq'
		ct['dosesq'] = im.get1dlist([0,1,1])
	else:
		continue #skip

	if 'layer' in fp:
		row['loc'] = 'layer'
	elif 'spot' in fp:
		row['loc'] = 'spot'
	else:
		row['loc'] = 'full'

	#nprim
	if 'N24n' in fp:
		row['nprim'] = 1e7
	if 'Hsl6' in fp:
		row['nprim'] = 1e7
	if 'YsgV' in fp:
		row['nprim'] = 1e6
	if 'Z2bG' in fp:
		row['nprim'] = 1e7
	if 'vtwj' in fp:
		row['nprim'] = 1e6
	if 'y1M5' in fp:
		row['nprim'] = 1e5

	if 'eTVQ' in fp:
		row['nprim'] = 1e7
	if 'qjEk' in fp:
		row['nprim'] = 1e7
	if 'EkjX' in fp:
		row['nprim'] = 1e6
	if 'CzF4' in fp:
		row['nprim'] = 1e7
	if 'WAKg' in fp:
		row['nprim'] = 1e6
	if 'LIeR' in fp:
		row['nprim'] = 1e5

	row['plotgroup'] = row['loc']+str(row['nprim'])
	
	try:
		if row['plotgroup'] not in data_singleton.keys():
			data_singleton[row['plotgroup']] = row
		elif 'dose' == ct['type']:
			data_singleton[row['plotgroup']][ctname]['dose'] = ct['dose']
		elif 'dosesq' == ct['type']:
			data_singleton[row['plotgroup']][ctname]['dosesq'] = ct['dosesq']
		elif 'pg' == ct['type']:
			data_singleton[row['plotgroup']][ctname]['pg'] = ct['pg']
	except KeyError as e:
		print row['plotgroup']
		print data_singleton
		sys.exit(1)

# print data_singleton
# sys.exit(1)
# compute correct unc
for key, valuee in data_singleton.iteritems():
	for value in [valuee['orig'],valuee['replan']]:
		data = np.array(value['dose'])
		sq = np.array(value['dosesq'])

		#mu = np.mean(data)
		#N=len(data) #TODO: ik denk dat N=#bins compressed zijn, dus product van de crushed dims
		assert len(data) == len(sq)

		# # var = sum-of-squares/# - sq(sum/#)
		# # var = ( sum([i**2 for i in binn]) / N ) - ( (mu)**2 ) #JM!!!
		# if (mean != 0.0 && N != 1 && squared != 0.0){
		#   *po = sqrt( (1.0/(N-1))*(squared/N - pow(mean/N, 2)))/(mean/N);
		# }
		# else *po = 1;
		var = []
		for sq_i,dose_i in zip(sq,data):
			if dose_i > 0 and sq_i >0:
				var.append( ( (sq_i / N) - ( (dose_i/N)**2 ) ) / (dosi_N-1) )
			else:
				var.append(1.)

		#print var #var is too small to be interesting, and also negative.
		with np.errstate(invalid='ignore'):
			#bug! this is always NaN
			value['doseunc'] = np.sqrt(np.array(var))
			#print value['doseunc']
		value['dose-unc'],value['dose+unc'] = plot.geterrorbands(value['doseunc'],value['dose'])

##data is now in order. lets plot!

def plotwunc(ax1,dataset,label=''):
	global color_index
	colors=plot.colors
	x_axis = np.linspace(0,300,150)#300mm,2mm voxels

	color_index+=1
	scale=np.max(dataset['dose'])/np.max(dataset['pg'])
	ax1.step(x_axis,dataset['pg']*scale, label='pg,scaled,'+label, color=colors[color_index], lw=0.5)
	color_index+=1
	ax1.step(x_axis,dataset['dose'], label='dose,'+label, color=colors[color_index],lw=0.5)
	#plot.fill_between_steps(ax1,x_axis,dataset['dose-unc'],dataset['dose+unc'],alpha=0.25,color=colors[color_index], lw=0.01)
	

for key, value in data_singleton.iteritems():
	color_index=0
	f, plo = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=True)

	plotwunc(plo,value['orig'],'orig')
	plotwunc(plo,value['replan'],'replan')
	#ax1.autoscale(axis='x',tight=True)
	plot.texax(plo)

	plo.set_title("Yield")
	# plo.set_ylim([1e-1,1.1e2])
	plo.set_ylabel('Dose [gy], PG Yield [a.u.]')
	plo.set_xlabel('Depth [mm]')
	#plo.xaxis.set_label_coords(1.1,-0.1)

	lgd = plo.legend(loc='upper right', bbox_to_anchor=(1.7, 1.),frameon=False)
	[label.set_linewidth(1) for label in lgd.get_lines()]
	f.savefig(key+'.pdf', bbox_inches='tight')
	#f.savefig(key+'.png', bbox_inches='tight',dpi=300)
	plt.close('all')
