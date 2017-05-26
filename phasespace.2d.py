#!/usr/bin/env python
import argparse,numpy as np,matplotlib,dump,plot

parser = argparse.ArgumentParser(description='Plot 2D hist from ROOT TTree.')
parser.add_argument('files', nargs='*')
args = parser.parse_args()
rootfiles = args.files

for rootfile in rootfiles:
    all = dump.get2D(rootfile,['X','Y'])
    phot_trans = dump.get2D(rootfile,['X','Y'],ParticleName='gamma',Transmission=True)
    phot_scatter = dump.get2D(rootfile,['X','Y'],ParticleName='gamma',Transmission=False)
    nonphot = dump.get2D(rootfile,['X','Y'],ParticleName='not_gamma')
    
    all_E = dump.get1D(rootfile,'Ekine')
    phot_trans_E = dump.get1D(rootfile,'Ekine',ParticleName='gamma',Transmission=True)
    phot_scatter_E = dump.get1D(rootfile,'Ekine',ParticleName='gamma',Transmission=False)
    phot_nonphot_E = dump.get1D(rootfile,'Ekine',ParticleName='not_gamma')
    
    partname = dump.get1D(rootfile,'ParticleName')
    
    f, ((ax1 ,ax2 ,ax3 ,ax4),(ax5 ,ax6, ax7 ,ax8),(ax9 ,ax10, ax11 ,ax12))= plot.subplots(nrows=3, ncols=4, sharex=False, sharey=False)#,figsize=(28,10))
    
    f.subplots_adjust(hspace=.5)
    f.subplots_adjust(wspace=.5)
    
    ax1.set_title("Total")
    ax2.set_title("Photon Trans")
    ax3.set_title("Photon Scatter")
    ax4.set_title("Secondaries")
    
    ax5.set_title("Total Energy")
    ax6.set_title("P T Energy")
    ax7.set_title("P S Energy")
    ax8.set_title("Sec. Energy")
    
    xbins = np.linspace(-150,150,50)
    ybins = np.linspace(-150,150,50)
    
    a = plot.plot2dhist( ax1, all['X'], all['Y'], xbins=xbins,ybins=ybins, log=True)
    a = plot.plot2dhist( ax2, phot_trans['X'], phot_trans['Y'], xbins=xbins,ybins=ybins, log=True)
    a = plot.plot2dhist( ax3, phot_scatter['X'], phot_scatter['Y'], xbins=xbins,ybins=ybins, log=True)
    a = plot.plot2dhist( ax4, nonphot['X'], nonphot['Y'], xbins=xbins,ybins=ybins, log=True)
    
    #,norm=matplotlib.colors.LogNorm(),vmin=1e0,vmax=1e2)
    
    plot.plot1dhist(ax5,all_E,30)
    plot.plot1dhist(ax6,phot_trans_E,30)
    plot.plot1dhist(ax7,phot_scatter_E,30)
    plot.plot1dhist(ax8,phot_nonphot_E,30)
    
    d = {
    'e-':'Electron',
    'e+':'Positron',
    'gamma':'Photon'
    }
    plot.plotbar(ax9,partname,relabel=d,log=True)
    
    
    #cb = f.colorbar(a, ax=(ax1,ax2,ax3,ax4))#, aspect=50)
    #cb.outline.set_visible(False)
    #cb.set_label('Hits', rotation=270)
    
    f.savefig(rootfile+'.pdf', bbox_inches='tight')
    plot.close('all')
    
