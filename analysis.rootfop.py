#!/usr/bin/env python
import dump, numpy as np,glob2 as glob,auger,image

##(rootfiles,field,bins,lowrange,highrange):
#Y=dump.dump(['pgprod-worldframe.root'],'X',300,-150,150)
#X=np.linspace(-149.5,149.5,300)
#auger.get_fop(X,Y,plot='patient-worldframe.pdf')


#X=np.linspace(-39,79,60)

##Y=dump.dump(['output/iba-perdet.root'],'X',60,-40,80)
##auger.get_fop(X,Y,plot='iba-perdet.pdf')

##Y=dump.dump(['output/iba-perdet-world.root'],'X',60,-40,80)
##auger.get_fop(X,Y,plot='iba-perdet-worldframe.pdf')

#Y=dump.dump(['output/ipnl-perdet.root'],'X',60,-40,80)
#auger.get_fop(X,Y,plot='ipnl-perdet.pdf')

##Y=dump.dump(['output/ipnl-perdet-world.root'],'X',60,-40,80)
##auger.get_fop(X,Y,plot='ipnl-perdet-world.pdf')



#lst=dump.thist2np_xy('GammProdCount-Prod.root')
#auger.get_fop(lst['histo'][0],lst['histo'][1],plot='GammProdCount.pdf')


###########################################################################################################

volume_offset=-141.59+7.96#spot sources

pgsrc_ct = image.image('data/ct/source-ct-LAYERID-elayspot61.mhd')
pgsrc_ct.toprojection(".x", [0,1,1,1])
pgsrc_ct_y = pgsrc_ct.imdata/pgsrc_ct.imdata.max()
#pgsrc_rpct = image.image('data/rpct/source-rpct-LAYERID-elayspot61.mhd')
#pgsrc_rpct = image.image('data/rpct/source-rpct-LAYERID-geolayspot61.mhd')
pgsrc_rpct = image.image('data/ct/source-ct-LAYERID-geolayspot61.mhd') #ALIGN AT CT, NOT RPCT
pgsrc_rpct.toprojection(".x", [0,1,1,1])
pgsrc_rpct_y = pgsrc_rpct.imdata/pgsrc_rpct.imdata.max()

pgsrc_ct_x = np.linspace(-149,149,150) #bincenters
pgsrc_ct_xhist = np.linspace(-150,150,151) #2mm voxels, endpoints
pgsrc_ct_x = pgsrc_ct_x+(volume_offset-pgsrc_ct_x[0])   #offset for pg source image
pgsrc_ct_xhist = pgsrc_ct_xhist+(volume_offset-pgsrc_ct_xhist[0]) #same

pgsrc_rpct_x = np.linspace(-149,149,150) #bincenters
pgsrc_rpct_xhist = np.linspace(-150,150,151) #2mm voxels, endpoints
pgsrc_rpct_x = pgsrc_rpct_x+(volume_offset-pgsrc_rpct_x[0])   #offset for pg source image
pgsrc_rpct_xhist = pgsrc_rpct_xhist+(volume_offset-pgsrc_rpct_xhist[0]) #same

pgsrc_ctfo=auger.get_fop(pgsrc_ct_x,pgsrc_ct_y)
pgsrc_rpctfo=auger.get_fop(pgsrc_rpct_x,pgsrc_rpct_y)

###########################################################################################################

print 'elayspot61' , pgsrc_ctfo
print 'geolayspot61' , pgsrc_rpctfo

#quit()
import plot
f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)

ax1.step(pgsrc_ct_x,pgsrc_ct_y, color='steelblue',lw=1., alpha=0.2, label='elayspot61 FOP: '+str(pgsrc_ctfo), where='mid')
ax1.step(pgsrc_rpct_x,pgsrc_rpct_y, color='indianred',lw=1., alpha=0.2, label='geolayspot61 FOP: '+str(pgsrc_rpctfo), where='mid')

ax1.legend(frameon = False,loc='lower left')
plot.texax(ax1)

f.savefig('layerfops.pdf', bbox_inches='tight')
plot.close('all')


