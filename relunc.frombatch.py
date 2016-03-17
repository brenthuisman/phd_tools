#!/usr/bin/env python
'''
generate relunc plot directly from batch.
'''
import sys,copy,glob2,image,tle,plot,numpy as np,matplotlib.pyplot as plt,matplotlib as mpl
from numpy import sqrt

if len(sys.argv) is not 2:
	print "No input file names given, assume analog.mhd"
	indir = "."
	infile = "analog.mhd"
else:
	indir = "."
	infile = str(sys.argv[-1])

sources = glob2.glob(indir+"/**/"+infile)
if len(sources) < 2:
	print "None or one file found, exiting..."
	sys.exit()

nr = len(sources)

print len(sources), "files found:", sources[:3], '...', sources[-3:]
######################################################################################################## TODO: divide by N-1, because var = sigma^2/(N-1)
# sigma^2 = sum_of_squares/N - mean^2
# var = sum-of-squares/# - sq(sum/#)


### Load up
maskspect = image.image("mask-spect1-8/finalmask.mhd")
maskbox2 = image.image("mask-box2/phantom_Parodi_TNS_2005_52_3_modified.maskfile2.mhd")
maskbox8 = image.image("mask-box8/phantom_Parodi_TNS_2005_52_3_modified.maskfile8.mhd")
mask90pc = image.image("mask90pc/mean.mhd") #is simply analog1B mean
mask90pc.to90pcmask()

# box2ims = []
box2_sum = [0]*250
box2_sumsq = [0]*250
for filename in sources:
	im = image.image(filename)
	im.applymask(mask90pc,maskspect,maskbox2)
	spect = im.get1dlist([1,1,1,0])
	box2_sum   = [x+y for x,y in zip(box2_sum, spect)]
	box2_sumsq = [x+(y**2) for x,y in zip(box2_sumsq, spect)]

# box8ims = []
box8_sum = [0]*250
box8_sumsq = [0]*250
for filename in sources:
	# box8ims.append(image.image(filename))
	# box8ims[-1].applymask([mask90pc,maskspect,maskbox8])
	# spect=box8ims[-1].get1dlist([1,1,1,0])
	im = image.image(filename)
	im.applymask(mask90pc,maskspect,maskbox8)
	spect = im.get1dlist([1,1,1,0])
	box8_sum   = [x+y for x,y in zip(box8_sum, spect)]
	box8_sumsq = [x+(y**2) for x,y in zip(box8_sumsq, spect)]

# print "box8_sum",box8_sum
# print "box8_sumsq",box8_sumsq

### get var
# var = sum-of-squares/# - (sum/#)^2          /          N-1

relunc2 = [0]*250
relunc8 = [0]*250
for E in range(250):
	if box2_sum[E] > 0 and box2_sum[E] > 0:
		sig2 = box2_sum[E] / nr
		var2 = ( box2_sumsq[E]/nr-(sig2)**2 ) / (nr-1)
		# relunc2[E] = sqrt(abs(var2))/sig2
		relunc2[E] = sqrt(var2)/sig2

	if box8_sum[E] > 0 and box8_sum[E] > 0:
		sig8 = box8_sum[E] / nr
		var8 = ( box8_sumsq[E]/nr-(sig8)**2 ) / (nr-1)
		# relunc8[E] = sqrt(abs(var8))/sig8
		relunc8[E] = sqrt(var8)/sig8


#modified from  tle.plt
def plot1d(ax1,dataset):
	colors = plot.colors
	color_index=0

	#asume voxels are 2mm
	x_axis = np.linspace(0,10,250)

	key = 1e4
	ax1.step(x_axis,[x*100. for x in dataset], label=plot.sn_mag(key)+' primaries', color=colors[color_index])
	color_index+=1

	ax1.semilogy()
	ax1.autoscale(axis='x',tight=True)
	#ax1.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.0f%%'))

	#PG falloff line
	spectcutoff = [1,8]
	ax1.set_xlim(spectcutoff)

	plot.texax(ax1)


f, (tl,tr) = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)

plot1d(tl,relunc2)
plot1d(tr,relunc8)
# plot1d(tl,box2_sum)
# plot1d(tr,box8_sum)

tl.yaxis.set_label_position("left")
tr.yaxis.set_label_position("left")

tl.set_title("Medium 2 (Bone)")#\nMedian gain: "+plot.sn(lmed2))
tr.set_title("Medium 8 (Muscle)")#\nMedian gain: "+plot.sn(lmed8))
# tl.set_ylim([1e-1,1.1e2])
# tr.set_ylim([1e-1,1.1e2])

tl.set_ylabel('Relative Uncertainty [\%]')
tl.set_xlabel('PG energy [MeV]')
tl.xaxis.set_label_coords(1.1,-0.1)

lgd = tr.legend(loc='upper right', bbox_to_anchor=(1.7, 1.),frameon=False)
[label.set_linewidth(1) for label in lgd.get_lines()]
f.savefig('relunc-boxes.pdf', bbox_inches='tight')
plt.close('all')
