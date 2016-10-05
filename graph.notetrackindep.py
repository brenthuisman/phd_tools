#!/usr/bin/env python
import numpy as np,matplotlib.pyplot as plt,plot,image,sys
from scipy.stats import norm

clrs=plot.colors

f, ax1 = plt.subplots(nrows=1, ncols=1, sharex=False, sharey=False)

batchims=["output1/source.mhd",
		"output2/source.mhd",
		"output3/source.mhd",
		"output4/source.mhd",
		"output5/source.mhd",
		"output6/source.mhd",
		"output7/source.mhd",
		"output8/source.mhd",
		"output9/source.mhd",
		"output10/source.mhd"]

analyt = "output-analytic/source.mhd"
analytvar = "output-analytic/source-debugvar.mhd"

x_axis=np.linspace(0,300,150)

im_analyt = image.image(analyt)
im_analyt.toprojection('3d',[0,0,0,1])
im_analyt = im_analyt.imdata.flatten()
im_analytvar = image.image(analytvar)
im_analytvar.toprojection('3d',[0,0,0,1])
im_analytvar = im_analytvar.imdata.flatten()

im_batch = []
for im in batchims:
    tmp = image.image(im)
    tmp.toprojection('3d',[0,0,0,1])
    im_batch.append(tmp.imdata.flatten())
im_batch = np.vstack((im_batch))
im_batch = np.rollaxis(im_batch,1) #list of 10 values per bin

im_batch_var = []
for binn in im_batch:
    (mu, sigma) = norm.fit(binn)
    im_batch_var.append(sigma/mu)


ax1.step(x_axis,np.sqrt(im_analytvar)/im_analyt, label='Independent analytic', color=clrs[0],lw=0.5)
ax1.step(x_axis,im_batch_var, label='Batch', color=clrs[1],lw=0.5)
#ax1.set_xlim(0,30)
ax1.set_xlabel('Beam Axis [mm]')
ax1.set_ylabel('Variance on PG yield')
ax1.semilogy()
#ax1.set_title('Cumulative tracklength distribution')
plot.texax(ax1)
lgd = ax1.legend(loc='upper right',frameon=False, bbox_to_anchor=(1.2, 1.))
f.savefig('note-on-indep.pdf', bbox_inches='tight')
plt.close('all')
