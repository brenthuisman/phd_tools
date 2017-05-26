#!/usr/bin/env python
import plot, numpy as np,auger,image,rtplan
from scipy.ndimage.filters import gaussian_filter

###########################################################################################################

smooth_param = 8.5 #20 mm FWHM

volume_offset=-141.59+7.96#spot sources

##61
pgelay = image.image('data/ct/source-ct-LAYERID-elayspot61.mhd')
rppgelay = image.image('data/rpct/source-rpct-LAYERID-elayspot61.mhd')
pggeolay = image.image('data/ct/source-ct-LAYERID-geolayspot61.mhd')
rppggeolay = image.image('data/rpct/source-rpct-LAYERID-geolayspot61.mhd')

ctelay = image.image('../doseactortest/output/dose-ct-LAYERID-elayspot61-Dose.mhd')
rpctelay = image.image('../doseactortest/output/dose-rpct-LAYERID-elayspot61-Dose.mhd')
ctgeolay = image.image('../doseactortest/output/dose-ct-LAYERID-geolayspot61-Dose.mhd')
rpctgeolay = image.image('../doseactortest/output/dose-rpct-LAYERID-geolayspot61-Dose.mhd')

##40
#pgelay = image.image('data/ct/source-ct-LAYERID-elayspot61.mhd')
#rppgelay = image.image('data/rpct/source-rpct-LAYERID-elayspot61.mhd')
##pggeolay = image.image('data/ct/source-ct-LAYERID-geolayspot40.mhd')
##rppggeolay = image.image('data/rpct/source-rpct-LAYERID-geolayspot40.mhd')
#pggeolay = image.image('data/ct/source-ct-LAYERID-geolayspot40.mhd')
#rppggeolay = image.image('data/rpct/source-rpct-LAYERID-geolayspot40.mhd')

##29
#pgelay = image.image('data/ct/source-ct-LAYERID-elayspot29.mhd')
#rppgelay = image.image('data/rpct/source-rpct-LAYERID-elayspot29.mhd')
#pggeolay = image.image('data/ct/source-ct-LAYERID-geolayspot29.mhd')
#rppggeolay = image.image('data/rpct/source-rpct-LAYERID-geolayspot29.mhd')


###########################################################################################################

ctelay.toprojection(".x", [0,1,1])
rpctelay.toprojection(".x", [0,1,1])
ctgeolay.toprojection(".x", [0,1,1])
rpctgeolay.toprojection(".x", [0,1,1])

pgelay.toprojection(".x", [0,1,1,1])
rppgelay.toprojection(".x", [0,1,1,1])
pggeolay.toprojection(".x", [0,1,1,1])
rppggeolay.toprojection(".x", [0,1,1,1])

pgsrc_ct_x = np.linspace(-149,149,150) #bincenters
pgsrc_ct_xhist = np.linspace(-150,150,151) #2mm voxels, endpoints
pgsrc_ct_x = pgsrc_ct_x+(volume_offset-pgsrc_ct_x[0])   #offset for pg source image
pgsrc_ct_xhist = pgsrc_ct_xhist+(volume_offset-pgsrc_ct_xhist[0]) #same

detprof_pgelay = gaussian_filter(pgelay.imdata, sigma=smooth_param)
detprof_rppgelay = gaussian_filter(rppgelay.imdata, sigma=smooth_param)
detprof_pggeolay = gaussian_filter(pggeolay.imdata, sigma=smooth_param)
detprof_rppggeolay = gaussian_filter(rppggeolay.imdata, sigma=smooth_param)

ctelay_fo=auger.get_fop(pgsrc_ct_x,ctelay.imdata)
rpctelay_fo=auger.get_fop(pgsrc_ct_x,rpctelay.imdata)
ctgeolay_fo=auger.get_fop(pgsrc_ct_x,ctgeolay.imdata)
rpctgeolay_fo=auger.get_fop(pgsrc_ct_x,rpctgeolay.imdata)

pgelay_fo=auger.get_fop(pgsrc_ct_x,pgelay.imdata)
rppgelay_fo=auger.get_fop(pgsrc_ct_x,rppgelay.imdata)
pggeolay_fo=auger.get_fop(pgsrc_ct_x,pggeolay.imdata)
rppggeolay_fo=auger.get_fop(pgsrc_ct_x,rppggeolay.imdata)

psf_pgelay_fo=auger.get_fop(pgsrc_ct_x,detprof_pgelay)
psf_rppgelay_fo=auger.get_fop(pgsrc_ct_x,detprof_rppgelay)
psf_pggeolay_fo=auger.get_fop(pgsrc_ct_x,detprof_pggeolay)
psf_rppggeolay_fo=auger.get_fop(pgsrc_ct_x,detprof_rppggeolay)

print '###########################################################################################################'

print 'PG FOPS'
print 'pgelay_fo', pgelay_fo, ', w/psf:', psf_pgelay_fo
print 'rppgelay_fo', rppgelay_fo, ', w/psf:', psf_rppgelay_fo
print 'pggeolay_fo', pggeolay_fo, ', w/psf:', psf_pggeolay_fo
print 'rppggeolay_fo', rppggeolay_fo, ', w/psf:', psf_rppggeolay_fo

print 'FOP shifts'
print 'ELAY, ct:', str(rpctelay_fo-ctelay_fo)[:4], ', pg', str(rppgelay_fo-pgelay_fo)[:4], ', pg+psf', str(psf_rppgelay_fo-psf_pgelay_fo)[:4]
print 'GEOLAY, ct:', str(rpctgeolay_fo-ctgeolay_fo)[:4], ', pg', str(rppggeolay_fo-pggeolay_fo)[:4], ', pg+psf', str(psf_rppggeolay_fo-psf_pggeolay_fo)[:4]

print '###########################################################################################################'

rtplan = rtplan.rtplan(['../doseactortest/data/plan.txt'],norm2nprim=False)#,noproc=True)
MSW=[]
for spot in rtplan.spots:
	if spot[0] == 102:#
		MSW.append(spot)

#### dose
#dose_offset=-142.097+7.96
#x = np.linspace(-149.5,149.5,300) #bincenters
#xhist = np.linspace(-150,150,301) #1mm voxels, endpoints
#x = x+(dose_offset-x[0])   #offset for pg source image
#xhist = xhist+(dose_offset-xhist[0]) #same
#dose = image.image('../doseactortest/output/new_dosespotid-ct.mhd')
#dose = dose.imdata.reshape(dose.imdata.shape[::-1]).squeeze()
#rpdose = image.image('../doseactortest/output/new_dosespotid-rpct.mhd')
#rpdose = rpdose.imdata.reshape(rpdose.imdata.shape[::-1]).squeeze()

#ct29_fo=auger.get_fop(x,dose[29])
#rpct29_fo=auger.get_fop(x,rpdose[29])
#ct40_fo=auger.get_fop(x,dose[40])
#rpct40_fo=auger.get_fop(x,rpdose[40])

###########################################################################################################

def yld(profile):
	nr=str(profile.sum()*100.)
	return nr[:3]+'\%'

def plotprof(ax,xax,emit,dete,name, **kwargs):
	if name == 'CT':
		color='steelblue'
	elif name == 'RPCT':
		color='indianred'
	else:
		color='black'
	ax.step(xax,emit, color=color,lw=1., alpha=1, label=name+', yield: '+yld(emit), where='mid')
	#ax.step(xax,dete, color=color,lw=1., alpha=0.5, label=name+' PSF', where='mid')
	return ax

###########################################################################################################

f, (ax1,ax2) = plot.subplots(nrows=1, ncols=2, sharex=True, sharey=False)

plotprof(ax1,pgsrc_ct_x,pgelay.imdata,detprof_pgelay,'CT')
plotprof(ax1,pgsrc_ct_x,rppgelay.imdata,detprof_rppgelay,'RPCT')
ax1.set_title('Iso-energy layer, PG shift: '+str(rppgelay_fo-pgelay_fo)[:4]+' mm', fontsize=10)
ax1.legend(frameon = False,loc='upper left')
ax1.set_xlim(-80,60)
ax1.set_ylim(0,0.003)
ax1.set_ylabel('Cumulative PG emission per proton')
plot.texax(ax1)

plotprof(ax2,pgsrc_ct_x,pggeolay.imdata,detprof_pggeolay,'CT')
plotprof(ax2,pgsrc_ct_x,rppggeolay.imdata,detprof_rppggeolay,'RPCT')
ax2.set_title('Iso-depth layer, PG shift: '+str(rppggeolay_fo-pggeolay_fo)[:4]+' mm', fontsize=10)
ax2.legend(frameon = False,loc='upper left')
#ax2.set_xlim(-80,70)
ax2.set_ylim(0,0.003)
ax2.set_xlabel('Position [mm]')
ax2.xaxis.set_label_coords(-0.1, -0.1)
plot.texax(ax2)

######## TopRow

#ax4.step(x,dose[29]/dose[29].max(), color='steelblue',lw=1., alpha=1, label='CT', where='mid')
#ax4.step(x,rpdose[29]/rpdose[29].max(), color='indianred',lw=1., alpha=1, label='RPCT', where='mid')
#ax4.set_title('Spot 29, Shift: '+str(rpct29_fo-ct29_fo)[:4]+' mm\n'+plot.sn(MSW[29][-1])+' protons', fontsize=10)
#ax4.legend(frameon = False,loc='upper left')
#ax4.set_xlim(-80,60)
#ax4.set_ylabel('Scaled Dose [a.u.]')
#plot.texax(ax4)

#ax5.step(x,dose[40]/dose[40].max(), color='steelblue',lw=1., alpha=1, label='CT', where='mid')
#ax5.step(x,rpdose[40]/rpdose[40].max(), color='indianred',lw=1., alpha=1, label='RPCT', where='mid')
#ax5.set_title('Spot 40, Shift: '+str(rpct40_fo-ct40_fo)[:4]+' mm\n'+plot.sn(MSW[40][-1])+' protons', fontsize=10)
#ax5.legend(frameon = False,loc='upper left')
##ax5.set_xlim(-80,70)
#ax5.set_xlabel('Position [mm]')
#plot.texax(ax5)

#ax4.xaxis.set_visible(False)
#ax5.xaxis.set_visible(False)
#ax6.xaxis.set_visible(False)
#ax5.yaxis.set_visible(False)
#ax6.yaxis.set_visible(False)

ax2.yaxis.set_visible(False)
#ax3.yaxis.set_visible(False)

f.subplots_adjust(hspace=0.3)

f.savefig('layprofiles.pdf', bbox_inches='tight')
plot.close('all')


