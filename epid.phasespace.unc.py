#!/usr/bin/env python
import argparse,numpy as np,matplotlib,dump,plot

parser = argparse.ArgumentParser(description='Plot 2D hist from ROOT TTree.')
parser.add_argument('files', nargs='*')
args = parser.parse_args()
rootfiles = args.files

for rootfile in rootfiles:
    all = dump.get2D(rootfile,['X','Y'])
    
    f, (ax1 ,ax2 )= plot.subplots(nrows=1, ncols=2, sharex=False, sharey=False)#,figsize=(28,10))
    
    f.subplots_adjust(hspace=.5)
    f.subplots_adjust(wspace=.5)
    
    ax1.set_title("X,Y")
    ax2.set_title("unc histo")
    
    # BIN EDGES!
    xbins = np.linspace(-410/2.,410/2.,256+1)
    ybins = np.linspace(-410/2.,410/2.,256+1)
    
    counts = plot.plot2dhist( ax1, all['X'], all['Y'], xbins=xbins,ybins=ybins, log=True)
    
    #,norm=matplotlib.colors.LogNorm(),vmin=1e0,vmax=1e2)
    
    #plot.plot1dhist(ax2,counts.flatten(),bins=np.linspace(0,200,100), log=True,count=True)
    #with np.errstate(divide='ignore', invalid='ignore'):
        #unc = np.true_divide(1.,counts.flatten()*100.)
    #unc[unc == np.inf] = 0
    #unc[unc == np.nan] = 0
    plot.plot1dhist(ax2,(1./np.sqrt(counts.flatten()))*100.,bins=np.linspace(0,50,50), range=(0,50), log=True,count=True)
    
    f.savefig(rootfile+'.unc.pdf', bbox_inches='tight')
    plot.close('all')
    
