#!/usr/bin/env python
import argparse,numpy as np,matplotlib,dump,plot

parser = argparse.ArgumentParser(description='Plot 2D hist from ROOT TTree.')
parser.add_argument('files', nargs='*')
args = parser.parse_args()
rootfiles = args.files

for rootfile in rootfiles:
    all = dump.get2D(rootfile,['X','Y'])
    phot_trans = dump.get2D(rootfile,['X','Y'],ParticleName='gamma',Primary=True,Transmission=True) #transmission implies primary and gamma but anyway
    phot_scatter = dump.get2D(rootfile,['X','Y'],ParticleName='gamma',Primary=True,Transmission=False)
    phot_other = dump.get2D(rootfile,['X','Y'],ParticleName='gamma',Primary=False)
    nonphot = dump.get2D(rootfile,['X','Y'],ParticleName='not_gamma')
    
    all_E = dump.get1D(rootfile,'Ekine')
    phot_trans_E = dump.get1D(rootfile,'Ekine',ParticleName='gamma',Primary=True,Transmission=True)
    phot_scatter_E = dump.get1D(rootfile,'Ekine',ParticleName='gamma',Primary=True,Transmission=False)
    phot_other_E = dump.get1D(rootfile,'Ekine',ParticleName='gamma',Primary=False)
    nonphot_E = dump.get1D(rootfile,'Ekine',ParticleName='not_gamma')
    
    partname = dump.get1D(rootfile,'ParticleName')
    
    f, ((ax1 ,ax2 ,ax3 ,ax4, ax5),(ax6, ax7 ,ax8, ax9 ,ax10),(ax11 ,ax12, ax13, ax14, ax15))= plot.subplots(nrows=3, ncols=5, sharex=False, sharey=False)#,figsize=(28,10))
    
    f.subplots_adjust(hspace=.5)
    f.subplots_adjust(wspace=.5)
    
    ax1.set_title("Total Counts")
    ax2.set_title("Prim Trans")
    ax3.set_title("Prim Scat")
    ax4.set_title("Secon Phot")
    ax5.set_title("Nonphot")
    
    xbins = np.linspace(-150,150,50)
    ybins = np.linspace(-150,150,50)
    
    a = plot.plot2dhist( ax1, all['X'], all['Y'], xbins=xbins,ybins=ybins, log=True)
    a = plot.plot2dhist( ax2, phot_trans['X'], phot_trans['Y'], xbins=xbins,ybins=ybins, log=True)
    a = plot.plot2dhist( ax3, phot_scatter['X'], phot_scatter['Y'], xbins=xbins,ybins=ybins, log=True)
    a = plot.plot2dhist( ax4, phot_other['X'], phot_other['Y'], xbins=xbins,ybins=ybins, log=True)
    a = plot.plot2dhist( ax5, nonphot['X'], nonphot['Y'], xbins=xbins,ybins=ybins, log=True)
    
    #,norm=matplotlib.colors.LogNorm(),vmin=1e0,vmax=1e2)
    
    plot.plot1dhist(ax6,all_E,30,count=True)
    plot.plot1dhist(ax7,phot_trans_E,30,count=True)
    plot.plot1dhist(ax8,phot_scatter_E,30,count=True)
    plot.plot1dhist(ax9,phot_other_E,30,count=True)
    ax9.set_xlim(0,2)
    plot.plot1dhist(ax10,nonphot_E,30,count=True)
    
    d = {
        'e-':'Electron',
        'e+':'Positron',
        'gamma':'Photon'
    }
    plot.plotbar(ax14,partname,relabel=d,log=True)
    
    plot.plotbar(ax15,['Total Counts' for i in range(len(all['X']))]+['Prim Trans' for i in range(len(phot_trans['X']))]+['Prim Scat' for i in range(len(phot_scatter['X']))]+['Secon Phot' for i in range(len(phot_other['X']))],rotation=30)
    ax15.text(0.05, 0.95, 'Trans/Total: '+str( len(phot_trans['X'])/float(len(all['X'])) ) , ha='left', va='center', transform=ax15.transAxes)
    
    #cb = f.colorbar(a, ax=(ax1,ax2,ax3,ax4))#, aspect=50)
    #cb.outline.set_visible(False)
    #cb.set_label('Hits', rotation=270)
    
    f.savefig(rootfile+'.pdf', bbox_inches='tight')
    plot.close('all')
    
