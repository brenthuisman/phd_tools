#!/usr/bin/env python
import argparse,numpy as np,matplotlib,dump,plot

parser = argparse.ArgumentParser(description='Plot 2D hist from ROOT TTree.')
parser.add_argument('files', nargs='*')
args = parser.parse_args()
rootfiles = args.files

panelsize = 210. #mm
numpix = 256
pixsize = panelsize/numpix #mm
    
for rootfile in rootfiles:
    #Z because patient rotated
    
    fpos_e = dump.scaletreefast(rootfile,['X','Z'],ParticleName='not_gamma')
    fE_e = dump.scaletreefast(rootfile,'Ekine',ParticleName='not_gamma')
    
    #pos_e = dump.scaletree2hist(rootfile,['X','Z'],ParticleName='not_gamma',xbins=(-panelsize/2.,panelsize/2.,numpix),ybins=(-panelsize/2.,panelsize/2.,numpix))
    E_e = dump.scaletree2hist(rootfile,'Ekine',xbins=(0,10,100),ParticleName='not_gamma')
    
    f, ((ax1 ,ax2),(ax3 ,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)#,figsize=(28,10))
    
    f.subplots_adjust(hspace=.5,wspace=.5)
    
    ax1.set_title("Positions")
    ax2.set_title("Energy")
    
    xbins = np.linspace(-panelsize/2.,panelsize/2.,numpix+1)
    ybins = xbins
    xbins2 = plot.chopcentral(xbins,5)
    ybins2 = xbins2
    xbins3 = np.linspace(-5,5,10+1)
    ybins3 = xbins3
    xbins4 = np.linspace(-10,0,10+1)
    ybins4 = xbins4
    
    plot.plot2dhist( ax1, fpos_e['X'], fpos_e['Z'], xbins=xbins,ybins=ybins, log=True)
    plot.plot1dhist( ax2, fE_e,count=True)
    
    #ax3.pcolormesh(pos_e[0], pos_e[1], pos_e[2].T)#, log=True)
    #ax3.pcolormesh(pos_e[0], pos_e[1], pos_e[2])#, log=True)
    ax4.step(E_e[0][:-1],E_e[1])
    
    f.savefig(rootfile+'.pdf', bbox_inches='tight')
    plot.close('all')
    
