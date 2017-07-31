#!/usr/bin/env python
import argparse,numpy as np,dump,plot,glob2 as glob,image

parser = argparse.ArgumentParser(description='Plot uncs for PhS, dose and tledose.')
parser.add_argument('indir', nargs='*')
args = parser.parse_args()
indir = args.indir[0]

runtime = ''
with open(glob.glob(indir+"/**/*stat.txt")[0],'r') as statfile:
    for line in statfile:
        newline = line.strip()
        if len(newline)==0:
            continue
        newline=[x.strip() for x in newline.split('=')]
        if 'ElapsedTime' in newline[0]:
            runtime = newline[1]

dosephs = glob.glob(indir+"/**/epid-entry.root")[0] #1B doesnt have this, only without dash
doseim = glob.glob(indir+"/**/epiddose-Dose.mhd")[0]
doseuncim = glob.glob(indir+"/**/epiddose-Dose-Uncertainty.mhd")[0]
dosetleim = glob.glob(indir+"/**/epiddose-tle-Dose.mhd")[0]
dosetleuncim = glob.glob(indir+"/**/epiddose-tle-Dose-Uncertainty.mhd")[0]

#electronprod = glob.glob(indir+"/**/epid-entry.root")[0]

all = dump.get2D(dosephs,['X','Y'])

doseim_ = image.image(doseim,type='yield')
doseuncim_ = image.image(doseuncim,type='relunc')
doseuncim_.imdata = doseuncim_.imdata.squeeze()*100.

dosetleim_ = image.image(dosetleim,type='yield')
dosetleuncim_ = image.image(dosetleuncim,type='relunc')
dosetleuncim_.imdata = dosetleuncim_.imdata.squeeze()*100.

unc_axis = np.linspace(0,50,50)

f, ((ax1 ,ax2, ax3 ),(ax4, ax5, ax6))= plot.subplots(nrows=2, ncols=3, sharex=False, sharey=False)#,figsize=(28,10))

#f.subplots_adjust(hspace=.5)
#f.subplots_adjust(wspace=.5)
f.suptitle('Runtime: '+runtime+'s', fontsize=10)
ax1.set_title("PhS, X,Y")
ax2.set_title("Dose")
ax3.set_title("Dose TLE")
ax4.set_title("PhS, rel. unc")
ax5.set_title("Dose, rel. unc")
ax6.set_title("Dose TLE, rel. unc")

# BIN EDGES!
xbins = np.linspace(-410/2.,410/2.,256+1)
ybins = np.linspace(-410/2.,410/2.,256+1)

counts = plot.plot2dhist( ax1, all['X'], all['Y'], xbins=xbins,ybins=ybins, log=True)
plot.plot1dhist(ax4,(1./np.sqrt(counts.flatten()))*100.,bins=unc_axis, range=(min(unc_axis),max(unc_axis)), log=True,count=True)

ax2.imshow( doseim_.imdata.squeeze() , extent = [0,41,0,41], cmap='gray')
plot.plot1dhist( ax5, doseuncim_.imdata.flatten(), bins=unc_axis, log=True)

ax3.imshow( dosetleim_.imdata.squeeze() , extent = [0,41,0,41], cmap='gray')
plot.plot1dhist( ax6, dosetleuncim_.imdata.flatten(), bins=unc_axis, log=True)



f.savefig(indir.replace('/','_')+'_unc.pdf', bbox_inches='tight')
plot.close('all')
    
