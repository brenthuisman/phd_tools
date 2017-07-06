#!/usr/bin/env python
import argparse,numpy as np,matplotlib as mpl,image,plot,glob2 as glob
from scipy import fftpack
from collections import OrderedDict

parser = argparse.ArgumentParser(description='Perform frequency analysis on image. Is it blurry?')
parser.add_argument('files', nargs='*')
args = parser.parse_args()
files_ = args.files

outname = 'epid_plot.pdf'
imyields = glob.glob("./**/epiddose-trans-Dose.mhd")+glob.glob("./**/epiddose-nontrans-Dose.mhd")+glob.glob("./**/epiddose-Dose.mhd")
imuncs = glob.glob("./**/epiddose-trans-Dose-Uncertainty.mhd")+glob.glob("./**/epiddose-nontrans-Dose-Uncertainty.mhd")+glob.glob("./**/epiddose-Dose-Uncertainty.mhd")

outname = 'epid_tle_plot.pdf'
imyields = glob.glob("./**/epiddose-trans-tle-Dose.mhd")+glob.glob("./**/epiddose-nontrans-tle-Dose.mhd")+glob.glob("./**/epiddose-tle-Dose.mhd")
imuncs = glob.glob("./**/epiddose-trans-tle-Dose-Uncertainty.mhd")+glob.glob("./**/epiddose-nontrans-tle-Dose-Uncertainty.mhd")+glob.glob("./**/epiddose-tle-Dose-Uncertainty.mhd")

print imyields

labels = ['nontransmission','transmission','total dose'] #(non) transmission swapped, because IT IS KILLED BY THE ACTOR!!!!

fracties_totaal = []
fracties_isocentrum = []

f, axes = plot.subplots(nrows=len(imyields), ncols=4, sharex=False, sharey=False)#,figsize=(28,10))

for axrow,yim,uim,label in zip(axes,imyields,imuncs,labels):
    print yim,uim,label
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
    axrow[1].axvline(41./2.-8., color='#999999', ls='--') #10x10 at isoc is 16x16 at epid level
    axrow[1].axvline(41./2.+8., color='#999999', ls='--')
    axrow[1].set_xlim(0,41)
    plot.set_metric_prefix_y(axrow[1])
    
    
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
f.savefig(outname, bbox_inches='tight')
plot.close('all')
