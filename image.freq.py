#!/usr/bin/env python
import argparse,numpy as np,matplotlib as mpl,image,plot
from scipy import fftpack

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

# nocuts, thin

#imyields = ["run.2npr/output.local_1/epiddose-all-Dose.mhd","run.UlRn/output.local_1/epiddose-all-Dose.mhd","run.Vz1L/output.local_1/epiddose-all-Dose.mhd"]
#imuncs = ["run.2npr/output.local_1/epiddose-all-Dose-Uncertainty.mhd","run.UlRn/output.local_1/epiddose-all-Dose-Uncertainty.mhd","run.Vz1L/output.local_1/epiddose-all-Dose-Uncertainty.mhd"]

#mask90pc = image.image("run.Vz1L/output.local_1/epiddose-all-Dose.mhd",type='yield')
#mask90pc.to90pcmask()

# cuts, thick

imyields = ["run.HXmg/output.local_1/epiddose-all-Dose.mhd","run.EcGI/output.local_1/epiddose-all-Dose.mhd","run.XxPP/output.local_1/epiddose-all-Dose.mhd"]
imuncs = ["run.HXmg/output.local_1/epiddose-all-Dose-Uncertainty.mhd","run.EcGI/output.local_1/epiddose-all-Dose-Uncertainty.mhd","run.XxPP/output.local_1/epiddose-all-Dose-Uncertainty.mhd"]

#mask90pc = image.image("run.XxPP/output.local_1/epiddose-all-Dose.mhd",type='yield')
#mask90pc.toNpcmask(90)

labels = ['transmission','nontransmission','all']

fracties_totaal = []
fracties_isocentrum = []

f, axes = plot.subplots(nrows=len(imyields), ncols=3, sharex=False, sharey=False)#,figsize=(28,10))

for axrow,yim,uim,label in zip(axes,imyields,imuncs,labels):
    yim_ = image.image(yim,type='yield')
    uim_ = image.image(uim,type='relunc') #the doseactor outputs relative uncertainties as per Chetty, see GateImageWithStatistic
    #uim_.applymask(mask90pc)
    uim_.imdata = uim_.imdata.squeeze()*100. #fractions to percentages
    fracties_isocentrum.append( yim_.getcenter().mean() )
    fracties_totaal.append( yim_.imdata.sum() )
    axrow[0].imshow( yim_.imdata.squeeze() , cmap='gray')
    #axrow[0].pcolormesh(np.linspace(0,41,num=yim_.imdata.squeeze().shape[0]), np.linspace(0,41,num=yim_.imdata.squeeze().shape[1]), yim_.imdata.squeeze())#, norm = mpl.colors.LogNorm())
    plot.texax(axrow[0])
    axrow[0].set_title(label + '\n$\sum$ Dose: '+ plot.sn(fracties_totaal[-1]))
    axrow[1].set_title(label)
    plot.plot1dhist( axrow[1], uim_.imdata.flatten(), bins=np.linspace(0,100,50), log=True)
    
#axrow[0].text(0.95, 0.95, 'Counts: '+str(len(data)) , ha='left', va='center')#, transform=ax.transAxes)
print fracties_totaal[0]/fracties_totaal[1]
print fracties_isocentrum[0]/fracties_isocentrum[1]
    
f.subplots_adjust(hspace=.5)
f.subplots_adjust(wspace=.5)
f.savefig('imfreq.pdf', bbox_inches='tight')
plot.close('all')
