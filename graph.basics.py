#!/usr/bin/env python
import dump, numpy as np,matplotlib.pyplot as plt,plot,image,scipy.ndimage

clrs=plot.colors

### range plot
f, ax1 = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False)

y_axis=[1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,12.5,15,17.5,20,25,27.5,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,125,150,175,200]
x_axis=[0.002458,0.003499,0.004698,0.006052,0.007555,0.009203,0.01099,0.01292,0.01499,0.01952,0.02458,0.03015,0.03623,0.04279,0.04984,0.05737,0.06537,0.07384,0.08277,0.09215,0.102,0.1123,0.123,0.1832,0.2539,0.335,0.426,0.637,0.7566,0.8853,1.17,1.489,1.841,2.227,2.644,3.093,3.572,4.08,4.618,5.184,5.777,6.398,7.045,7.718,11.46,15.77,20.62,25.96]

ax1.plot(x_axis,y_axis, color=clrs[0],lw=0.5)

ax1.set_ylabel('Energy [MeV]')
ax1.set_xlabel('Depth [cm]')
ax1.set_title('Proton Range in Water')
plot.texax(ax1)
f.savefig('protonrangeinwater.pdf', bbox_inches='tight')
f.savefig('protonrangeinwater.png', bbox_inches='tight',dpi=300)
plt.close('all')

### rifi plot
f, ax1 = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
x_axis=np.linspace(0,70,700)
ax1.step(x_axis,dump.thist2np("output/dosedist-Dose.root").itervalues().next(), label='Dose (w/RiFi)', color=clrs[0],lw=0.5)
ax1.step(x_axis,dump.thist2np("output/dosedist-norifi-Dose.root").itervalues().next(), label='Dose', color=clrs[1],lw=0.5)

ax1.set_xlim(0,30)
ax1.set_ylabel('Dose [Gy]')
ax1.set_xlabel('Depth [cm]')
ax1.set_title('Effect of a ripple filter (RiFi)')
plot.texax(ax1)
lgd = ax1.legend(loc='upper right',frameon=False, bbox_to_anchor=(1.2, 1.))
f.savefig('rifi.pdf', bbox_inches='tight')
f.savefig('rifi.png', bbox_inches='tight',dpi=300)
plt.close('all')

### peaksumming plot
orig = dump.thist2np("output/dosedist-Dose.root").itervalues().next()
pksum = orig[:]

def dice(indata,factor,step=10):
	global pksum
	retval=[]
	for it,x in enumerate(indata):
		if it%step==0:
			continue
		else:
			retval.append(x)
	#print retval
	retval.extend([0.]*(len(indata)-len(retval)))
	retval = [x*factor for x in retval]
	pksum = [a+b for a,b in zip(pksum,retval)]
	return plot.addrandomnoise(retval)

orig = pksum[:]
or90 = dice(orig, 0.3)
or80 = dice(or90, 0.85)
or70 = dice(or80, 0.6)
or60 = dice(or70, 0.75)
or50 = dice(or60, 1.)

f, ax1 = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
x_axis=np.linspace(0,70,700)
ax1.step(x_axis,orig, color=clrs[1],lw=0.5)
ax1.step(x_axis,or90, color=clrs[1],lw=0.5)
ax1.step(x_axis,or80, color=clrs[1],lw=0.5)
ax1.step(x_axis,or70, color=clrs[1],lw=0.5)
ax1.step(x_axis,or60, color=clrs[1],lw=0.5)
ax1.step(x_axis,or50, color=clrs[1],lw=0.5)
ax1.step(x_axis,pksum, color=clrs[0],lw=0.5)

ax1.set_xlim(0,30)
ax1.set_ylabel('Dose [Gy]')
ax1.set_xlabel('Depth [cm]')
ax1.set_title('Peak summing')
plot.texax(ax1)
lgd = ax1.legend(loc='upper right',frameon=False, bbox_to_anchor=(1.2, 1.))
f.savefig('peaksumming.pdf', bbox_inches='tight')
f.savefig('peaksumming.png', bbox_inches='tight',dpi=300)
plt.close('all')

### beamspread plot
f, ax1 = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False)

images=["output/carbon/1800mev/dosedist-norifi-Dose.mhd",
		"output/carbon/2400mev/dosedist-norifi-Dose.mhd",
		"output/carbon/3000mev/dosedist-norifi-Dose.mhd",
		"output/proton/100mev/dosedist-norifi-Dose.mhd",
		"output/proton/150mev/dosedist-norifi-Dose.mhd",
		"output/proton/200mev/dosedist-norifi-Dose.mhd"]
num = 700 #each bin is 1mm
noise_threshold = 1e-4
x_axis=np.linspace(0,70,70)
ci=0
for imf in images:
	im = image.image(imf)
	width_depth = []
	for depth in range(70):
		cum_profile = np.zeros(num, dtype=np.float)
		slicee = im.getslice('x',depth)
		#http://stackoverflow.com/questions/7878398/how-to-extract-an-arbitrary-line-of-values-from-a-numpy-array
		r=350
		for angle in np.arange(0,np.pi*2,np.pi/8.):
			x0 =  r + r * np.cos(angle)
			y0 =  r + r * np.sin(angle)
			x1 =  r - r * np.cos(angle)
			y1 =  r - r * np.sin(angle)
			#ax1.plot([x0, x1], [y0, y1], 'ro-')
			x, y = np.linspace(x0, x1, num), np.linspace(y0, y1, num)
			cum_profile += scipy.ndimage.map_coordinates(slicee, np.vstack((x,y)))
		#sla cum_profile op
		#ax1.plot((cum_profile+cum_profile[::-1])[num/2:])
		#sum profile with its opposite, and cut off first half so that we can just count until we have 90pc of yield for the threshold.
		cum_profile = (cum_profile+cum_profile[::-1])[num/2:]
		maxx=cum_profile.max()

		# cut off small values, these are noise.
		# if cum_profile.sum() < noise_threshold:
		# 	width_depth.append(0)
		# 	continue
		for index in range(len(cum_profile)):
			if cum_profile[index] < maxx*0.5:
				width_depth.append(index*2.)
				break
	ax1.plot(x_axis,width_depth, color=clrs[ci],label=imf.split('/')[2],lw=0.5)
	ci+=1


#ax1.set_xlim(0,30)
ax1.set_ylabel('Cross section FWHM [mm]')
ax1.set_xlabel('Depth [cm]')
ax1.set_title('Beam cross sections')
plot.texax(ax1)
lgd = ax1.legend(loc='upper right',frameon=False, bbox_to_anchor=(1.2, 1.))
f.savefig('beamspread.pdf', bbox_inches='tight')
f.savefig('beamspread.png', bbox_inches='tight',dpi=300)
plt.close('all')