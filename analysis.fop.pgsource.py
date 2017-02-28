#!/usr/bin/env python
import image,numpy as np,auger,plot

volume_offset=-141.597+7.96
#-141.597 komt uit mhd header source images, en is centrum van eerste voxel (bin).
#Dit is in MHD coords systeem, en dat verschilt van het met isocenter
#NOOT: offset in images is ANDERS dan in spotid simulaties (voxels in x direction zijn hier 2mm, elders 1mm (met MHD offset -142.097)

#volume_offset=-141.04 # OLD waterbox sources
volume_offset=-149#waterbox sources

###########################################################################################################

#spotim_ct = image.image('output/source-ct-'+str(int(args.dosepg))+'.mhd')
#spotim_rpct = image.image('output/source-rpct-'+str(int(args.dosepg))+'.mhd')

#spotim_ct = image.image("output/source-ct-61.mhd")
#spotim_rpct = image.image("output/source-rpct-61.mhd")

#spotim_ct = image.image("output/dosedist-ct-61-Dose.mhd")
#spotim_rpct = image.image("output/dosedist-rpct-61-Dose.mhd")

spotim_ct = image.image('data/source-139.mhd')
spotim_rpct = image.image('data/source-144.mhd')

#spotim_ct = image.image('ct/source-ct-LAYERID-geolay5e8.mhd')
#spotim_rpct = image.image('rpct/source-rpct-LAYERID-geolay5e8.mhd')

#spotim_ct = image.image('ct/source-ct-LAYERID-elay5e8.mhd')
#spotim_rpct = image.image('rpct/source-rpct-LAYERID-elay5e8.mhd')

###########################################################################################################

spotim_ct.toprojection(".x", [0,1,1,1])
spotim_rpct.toprojection(".x", [0,1,1,1])

x = np.linspace(-149,149,150) #bincenters
xhist = np.linspace(-150,150,151) #2mm voxels, endpoints
x = x+(volume_offset-x[0])   #offset for pg source image
xhist = xhist+(volume_offset-xhist[0]) #same

#print x

spot = spotim_ct.imdata
spot2 = spotim_rpct.imdata
ctfo=auger.get_fop(x,spot)
rpctfo=auger.get_fop(x,spot2)

# '####################'

print ctfo,rpctfo
print '####################'
print rpctfo-ctfo

f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)

ax1.step(x,spot, color='steelblue',lw=1., label='CT FOP: '+str(ctfo))
ax1.step(x,spot2, color='indianred',lw=1., label='RPCT FOP: '+str(rpctfo))

ax1.set_xlabel('FOP [mm], shift: '+str(rpctfo-ctfo) )
#ax1.set_ylabel('Number of spots')
#ax1.set_xlim(-60,25)
#ax1.set_ylim(0,140)

ax1.legend(frameon = False)
plot.texax(ax1)

f.savefig('fop-pgsource.pdf', bbox_inches='tight')
plot.close('all')
