#!/usr/bin/env python
import plot, numpy as np,auger,image,rtplan
from scipy.ndimage.filters import gaussian_filter

###########################################################################################################

smooth_param = 8.5 #20 mm FWHM

volume_offset=-141.59+7.96#spot sources

pg29 = image.image('data/ct/source-ct-29.mhd')
rppg29 = image.image('data/rpct/source-rpct-29.mhd')
pg40 = image.image('data/ct/source-ct-40.mhd')
rppg40 = image.image('data/rpct/source-rpct-40.mhd')
pg61 = image.image('data/ct/source-ct-61.mhd')
rppg61 = image.image('data/rpct/source-rpct-61.mhd')

pg29.toprojection(".x", [0,1,1,1])
rppg29.toprojection(".x", [0,1,1,1])
pg40.toprojection(".x", [0,1,1,1])
rppg40.toprojection(".x", [0,1,1,1])
pg61.toprojection(".x", [0,1,1,1])
rppg61.toprojection(".x", [0,1,1,1])

pgsrc_ct_x = np.linspace(-149,149,150) #bincenters
pgsrc_ct_xhist = np.linspace(-150,150,151) #2mm voxels, endpoints
pgsrc_ct_x = pgsrc_ct_x+(volume_offset-pgsrc_ct_x[0])   #offset for pg source image
pgsrc_ct_xhist = pgsrc_ct_xhist+(volume_offset-pgsrc_ct_xhist[0]) #same

pg29_fo=auger.get_fop(pgsrc_ct_x,pg29.imdata)
rppg29_fo=auger.get_fop(pgsrc_ct_x,rppg29.imdata)
pg40_fo=auger.get_fop(pgsrc_ct_x,pg40.imdata)
rppg40_fo=auger.get_fop(pgsrc_ct_x,rppg40.imdata)
pg61_fo=auger.get_fop(pgsrc_ct_x,pg61.imdata)
rppg61_fo=auger.get_fop(pgsrc_ct_x,rppg61.imdata)

psf_pg29_fo=auger.get_fop(pgsrc_ct_x,gaussian_filter(pg29.imdata, sigma=smooth_param))
psf_rppg29_fo=auger.get_fop(pgsrc_ct_x,gaussian_filter(rppg29.imdata, sigma=smooth_param))
psf_pg40_fo=auger.get_fop(pgsrc_ct_x,gaussian_filter(pg40.imdata, sigma=smooth_param))
psf_rppg40_fo=auger.get_fop(pgsrc_ct_x,gaussian_filter(rppg40.imdata, sigma=smooth_param))
psf_pg61_fo=auger.get_fop(pgsrc_ct_x,gaussian_filter(pg61.imdata, sigma=smooth_param))
psf_rppg61_fo=auger.get_fop(pgsrc_ct_x,gaussian_filter(rppg61.imdata, sigma=smooth_param))

rtplan = rtplan.rtplan(['../doseactortest/data/plan.txt'],norm2nprim=False)#,noproc=True)
MSW=[]
for spot in rtplan.spots:
	if spot[0] == 102:#
		MSW.append(spot)


#### dose
dose_offset=-142.097+7.96
x = np.linspace(-149.5,149.5,300) #bincenters
xhist = np.linspace(-150,150,301) #1mm voxels, endpoints
x = x+(dose_offset-x[0])   #offset for pg source image
xhist = xhist+(dose_offset-xhist[0]) #same
dose = image.image('../doseactortest/output/new_dosespotid-ct.mhd')
dose = dose.imdata.reshape(dose.imdata.shape[::-1]).squeeze()
rpdose = image.image('../doseactortest/output/new_dosespotid-rpct.mhd')
rpdose = rpdose.imdata.reshape(rpdose.imdata.shape[::-1]).squeeze()

ct29_fo=auger.get_fop(x,dose[29])
rpct29_fo=auger.get_fop(x,rpdose[29])
ct40_fo=auger.get_fop(x,dose[40])
rpct40_fo=auger.get_fop(x,rpdose[40])
ct61_fo=auger.get_fop(x,dose[61])
rpct61_fo=auger.get_fop(x,rpdose[61])

print '###########################################################################################################'

print 'PG FOPS'
print 'pg29', pg29_fo, ', w/psf:', psf_pg29_fo
print 'rppg29', rppg29_fo, ', w/psf:', psf_rppg29_fo
print 'pg40', pg40_fo, ', w/psf:', psf_pg40_fo
print 'rppg40', rppg40_fo, ', w/psf:', psf_rppg40_fo
print 'pg61', pg61_fo, ', w/psf:', psf_pg61_fo
print 'rppg61', rppg61_fo, ', w/psf:', psf_rppg61_fo

print 'FOP shifts'
print '29, ct:', str(rpct29_fo-ct29_fo)[:4], ', pg', str(rppg29_fo-pg29_fo)[:4], ', pg+psf', str(psf_rppg29_fo-psf_pg29_fo)[:4]
print '40, ct:', str(rpct40_fo-ct40_fo)[:4], ', pg', str(rppg40_fo-pg40_fo)[:4], ', pg+psf', str(psf_rppg40_fo-psf_pg40_fo)[:4]
print '61, ct:', str(rpct61_fo-ct61_fo)[:4], ', pg', str(rppg61_fo-pg61_fo)[:4], ', pg+psf', str(psf_rppg61_fo-psf_pg61_fo)[:4]

print '###########################################################################################################'

###########################################################################################################

def yld(profile):
	nr=str(profile.imdata.sum()*100.)
	return nr[:3]+'\%'

def plotprof(ax,xax,emit,dete,name, **kwargs):
	if name == 'CT':
		color='steelblue'
	elif name == 'RPCT':
		color='indianred'
	else:
		color='black'
	ax.step(xax,emit, color=color,lw=1., alpha=1, label=name+', yield: '+yld(emit), where='mid')
	#ax1.step(pgsrc_ct_x,dete, color=color,lw=1., alpha=0.5, label=name+' PSF', where='mid')
	return ax

###########################################################################################################

f, ((ax4,ax5,ax6),(ax1,ax2,ax3)) = plot.subplots(nrows=2, ncols=3, sharex=True, sharey=False)

ax1.step(pgsrc_ct_x,pg29.imdata, color='steelblue',lw=1., alpha=1, label='CT, yield: '+yld(pg29), where='mid')
ax1.step(pgsrc_ct_x,rppg29.imdata, color='indianred',lw=1., alpha=1, label='RPCT, yield: '+yld(rppg29), where='mid')
ax1.set_title('PG shift: '+str(rppg29_fo-pg29_fo)[:4]+' mm', fontsize=10)
ax1.legend(frameon = False,loc='upper left')
ax1.set_xlim(-80,60)
ax1.set_ylim(0,0.004)
ax1.set_ylabel('Cumulative PG emission per proton')
plot.texax(ax1)

ax2.step(pgsrc_ct_x,pg40.imdata, color='steelblue',lw=1., alpha=1, label='CT, yield: '+yld(pg40), where='mid')
ax2.step(pgsrc_ct_x,rppg40.imdata, color='indianred',lw=1., alpha=1, label='RPCT, yield: '+yld(rppg40), where='mid')
ax2.set_title('PG shift: '+str(rppg40_fo-pg40_fo)[:4]+' mm', fontsize=10)
ax2.legend(frameon = False,loc='upper left')
#ax2.set_xlim(-80,70)
ax2.set_ylim(0,0.004)
ax2.set_xlabel('Position [mm]')
plot.texax(ax2)

ax3.step(pgsrc_ct_x,pg61.imdata, color='steelblue',lw=1., alpha=1, label='CT, yield: '+yld(pg61), where='mid')
ax3.step(pgsrc_ct_x,rppg61.imdata, color='indianred',lw=1., alpha=1, label='RPCT, yield: '+yld(rppg61), where='mid')
ax3.set_title('PG shift: '+str(rppg61_fo-pg61_fo)[:4]+' mm', fontsize=10)
ax3.legend(frameon = False,loc='upper left')
#ax3.set_xlim(-80,70)
ax3.set_ylim(0,0.004)
plot.texax(ax3)

######## TopRow

ax4.step(x,dose[29]/dose[29].max(), color='steelblue',lw=1., alpha=1, label='CT', where='mid')
ax4.step(x,rpdose[29]/rpdose[29].max(), color='indianred',lw=1., alpha=1, label='RPCT', where='mid')
ax4.set_title('Spot A, Shift: '+str(rpct29_fo-ct29_fo)[:4]+' mm\n'+plot.sn(MSW[29][-1])+' protons', fontsize=10)
ax4.legend(frameon = False,loc='upper left')
ax4.set_xlim(-80,60)
ax4.set_ylabel('Scaled Dose [a.u.]')
plot.texax(ax4)

ax5.step(x,dose[40]/dose[40].max(), color='steelblue',lw=1., alpha=1, label='CT', where='mid')
ax5.step(x,rpdose[40]/rpdose[40].max(), color='indianred',lw=1., alpha=1, label='RPCT', where='mid')
ax5.set_title('Spot 40, Shift: '+str(rpct40_fo-ct40_fo)[:4]+' mm\n'+plot.sn(MSW[40][-1])+' protons', fontsize=10)
ax5.legend(frameon = False,loc='upper left')
#ax5.set_xlim(-80,70)
ax5.set_xlabel('Position [mm]')
plot.texax(ax5)

ax6.step(x,dose[61]/dose[61].max(), color='steelblue',lw=1., alpha=1, label='CT', where='mid')
ax6.step(x,rpdose[61]/rpdose[61].max(), color='indianred',lw=1., alpha=1, label='RPCT', where='mid')
ax6.set_title('Spot C, Shift: '+str(rpct61_fo-ct61_fo)[:4]+' mm\n'+plot.sn(MSW[61][-1])+' protons', fontsize=10)
ax6.legend(frameon = False,loc='upper left')
#ax6.set_xlim(-80,70)
plot.texax(ax6)

ax4.xaxis.set_visible(False)
ax5.xaxis.set_visible(False)
ax6.xaxis.set_visible(False)
ax5.yaxis.set_visible(False)
ax6.yaxis.set_visible(False)

ax2.yaxis.set_visible(False)
ax3.yaxis.set_visible(False)

f.subplots_adjust(hspace=0.3)

f.savefig('spotprofiles.pdf', bbox_inches='tight')
plot.close('all')


