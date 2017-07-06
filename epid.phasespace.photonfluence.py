#!/usr/bin/env python
import argparse,numpy as np,matplotlib,dump,plot

parser = argparse.ArgumentParser(description='Plot 2D hist from ROOT TTree.')
parser.add_argument('files', nargs='*')
args = parser.parse_args()
rootfiles = args.files

for rootfile in rootfiles:
    all = dump.scaletreefast(rootfile,['X','Y'])
    
    f, ((ax1 ,ax2), (ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)#,figsize=(28,10))
    
    f.subplots_adjust(hspace=.5,wspace=.5)
    
    ax1.set_title("Positions")
    ax2.set_title("Cutout")
    
    panelsize = 410. #mm
    numpix = 256
    
    pixsize = panelsize/numpix #mm
    
    xbins = np.linspace(-panelsize/2.,panelsize/2.,numpix+1)
    ybins = xbins
    xbins2 = plot.chopcentral(xbins,5)
    ybins2 = xbins2
    xbins3 = np.linspace(-5,5,10+1)
    ybins3 = xbins3
    xbins4 = np.linspace(-10,0,10+1)
    ybins4 = xbins4
    
    print xbins2
    
    whole = plot.plot2dhist( ax1, all['X'], all['Y'], xbins=xbins,ybins=ybins, log=True)
    plot.plot2dhist( ax2, all['X'], all['Y'], xbins=xbins2,ybins=ybins2, log=True)
    per_mm2 = plot.plot2dhist( ax3, all['X'], all['Y'], xbins=xbins3,ybins=ybins3, log=True)
    per_mm2_kwadrant = plot.plot2dhist( ax4, all['X'], all['Y'], xbins=xbins4,ybins=ybins4, log=True)
    
    print 'mean. per mm2,whole',np.mean(whole.flatten())
    print 'std. per mm2,whole',np.std(whole.flatten())
    
    print 'mean. per mm2',np.mean(per_mm2.flatten())
    print 'std. per mm2',np.std(per_mm2.flatten())
    
    print 'mean. per mm2',np.mean(per_mm2_kwadrant.flatten())
    print 'std. per mm2',np.std(per_mm2_kwadrant.flatten())
    print per_mm2_kwadrant
    
    
    f.savefig(rootfile+'.pdf', bbox_inches='tight')
    plot.close('all')
    
