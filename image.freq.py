#!/usr/bin/env python
import argparse,numpy as np,matplotlib as mpl,image,plot
from scipy import fftpack
from collections import OrderedDict

parser = argparse.ArgumentParser(description='Perform frequency analysis on image. Is it blurry?')
parser.add_argument('files', nargs='*')
args = parser.parse_args()
files_ = args.files

def azimuthalAverage(image, center=None):
    """
    Calculate the azimuthally averaged radial profile.

    image - The 2D image
    center - The [x,y] pixel coordinates used as the center. The default is 
             None, which then uses the center of the image (including 
             fracitonal pixels).
    
    """
    # Calculate the indices from the image
    y, x = np.indices(image.shape)

    if not center:
        center = np.array([(x.max()-x.min())/2.0, (x.max()-x.min())/2.0])

    r = np.hypot(x - center[0], y - center[1])

    # Get sorted radii
    ind = np.argsort(r.flat)
    r_sorted = r.flat[ind]
    i_sorted = image.flat[ind]

    # Get the integer part of the radii (bin size = 1)
    r_int = r_sorted.astype(int)

    # Find all pixels that fall within each radial bin.
    deltar = r_int[1:] - r_int[:-1]  # Assumes all radii represented
    rind = np.where(deltar)[0]       # location of changed radius
    nr = rind[1:] - rind[:-1]        # number of radius bin
    
    # Cumulative sum to figure out sums for each radius bin
    csim = np.cumsum(i_sorted, dtype=float)
    tbin = csim[rind[1:]] - csim[rind[:-1]]

    radial_prof = tbin / nr

    return radial_prof



# 10x10@isoc 1e8

imyields = ["run.012r/output.local_1/epiddose-all-Dose.mhd","run.kKw2/output.local_1/epiddose-all-Dose.mhd","run.GucV/output.local_1/epiddose-gamma-Dose.mhd","run.GucV/output.local_1/epiddose-electron-Dose.mhd","run.GucV/output.local_1/epiddose-all-Dose.mhd"]
imuncs = ["run.012r/output.local_1/epiddose-all-Dose-Uncertainty.mhd","run.kKw2/output.local_1/epiddose-all-Dose-Uncertainty.mhd","run.GucV/output.local_1/epiddose-gamma-Dose-Uncertainty.mhd","run.GucV/output.local_1/epiddose-electron-Dose-Uncertainty.mhd","run.GucV/output.local_1/epiddose-all-Dose-Uncertainty.mhd"]

# 10x10@panel square field 5e8

#imyields = ["run.012r/output.local_1/epiddose-all-Dose.mhd","run.kKw2/output.local_1/epiddose-all-Dose.mhd","run.GucV/output.local_1/epiddose-gamma-Dose.mhd","run.GucV/output.local_1/epiddose-electron-Dose.mhd","run.GucV/output.local_1/epiddose-all-Dose.mhd"]
#imuncs = ["run.012r/output.local_1/epiddose-all-Dose-Uncertainty.mhd","run.kKw2/output.local_1/epiddose-all-Dose-Uncertainty.mhd","run.GucV/output.local_1/epiddose-gamma-Dose-Uncertainty.mhd","run.GucV/output.local_1/epiddose-electron-Dose-Uncertainty.mhd","run.GucV/output.local_1/epiddose-all-Dose-Uncertainty.mhd"]

labels = ['transmission','nontransmission','total dose']

fracties_totaal = []
fracties_isocentrum = []

f, axes = plot.subplots(nrows=len(imyields), ncols=4, sharex=False, sharey=False)#,figsize=(28,10))

for axrow,yim,uim,label in zip(axes,imyields,imuncs,labels):
    yim_ = image.image(yim,type='yield')
    uim_ = image.image(uim,type='relunc') #the doseactor outputs relative uncertainties as per Chetty, see GateImageWithStatistic
    #uim_.applymask(mask90pc)
    uim_.imdata = uim_.imdata.squeeze()*100. #fractions to percentages
    fracties_isocentrum.append( yim_.getcenter().mean() )
    fracties_totaal.append( yim_.imdata.sum() )
    axrow[0].imshow( yim_.imdata.squeeze() , extent = [0,41,0,41], cmap='gray')
    #axrow[0].pcolormesh(np.linspace(0,41,num=yim_.imdata.squeeze().shape[0]), np.linspace(0,41,num=yim_.imdata.squeeze().shape[1]), yim_.imdata.squeeze())#, norm = mpl.colors.LogNorm())
    axrow[0].set_title(label + '\n$\sum$ Dose: '+ plot.sn(fracties_totaal[-1]))
    axrow[1].set_title(label + ' Profile')
    axrow[1].plot(*yim_.getprofile('y'), color = 'steelblue' , label='x')
    axrow[1].plot(*yim_.getprofile('x'), color = 'indianred' , label='y')
    axrow[1].legend(loc='upper right', bbox_to_anchor=(1., 1.),frameon=False)
    axrow[1].axvline(41./2.-5., color='#999999', ls='--')
    axrow[1].axvline(41./2.+5., color='#999999', ls='--')
    axrow[1].set_xlim(0,41)
    
    
    
    axrow[2].set_title(label)
    plot.plot1dhist( axrow[2], uim_.imdata.flatten(), bins=np.linspace(0,100,50), log=True)
    
#axrow[0].text(0.95, 0.95, 'Counts: '+str(len(data)) , ha='left', va='center')#, transform=ax.transAxes)
staaf = OrderedDict()
for label,ft,fi in zip(labels,fracties_totaal,fracties_isocentrum)[:-1]:
    staaf[label+' whole']=float(ft)/fracties_totaal[-1]*100. #pc
    staaf[label+' isoc']=float(fi)/fracties_isocentrum[-1]*100.
#staaf = [labels[0], fracties_totaal[0]/fracties_totaal[2]
#print fracties_isocentrum[0]/fracties_isocentrum[2]
staaf

plot.plotbar(axes[0][-1],staaf,bincount='%')#,rotation=30)

staaf2 = OrderedDict()
staaf2['sum/all whole']=(fracties_totaal[0]+fracties_totaal[1])/fracties_totaal[2]*100. #pc
staaf2['sum/all isoc']=(fracties_isocentrum[0]+fracties_isocentrum[1])/fracties_isocentrum[2]*100.
plot.plotbar(axes[1][-1],staaf2,bincount='%')



f.subplots_adjust(hspace=.5,wspace=.5)
f.savefig('imfreq.pdf', bbox_inches='tight')
plot.close('all')
