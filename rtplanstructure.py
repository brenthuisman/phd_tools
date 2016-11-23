#!/usr/bin/env python
import sys,rtplan,matplotlib.pyplot as plt,plot,math,numpy as np
from tableio import write

fname = ''
if sys.argv[-1] == 'noproc':
	fname = sys.argv[-2]
	rtplan = rtplan.rtplan(fname,norm2nprim=False,MSW_to_protons=False)
if sys.argv[-1] == 'nonorm':
	fname = sys.argv[-2]
	rtplan = rtplan.rtplan(fname,norm2nprim=False)
elif sys.argv[-1] == 'nomu':
	fname = sys.argv[-2]
	rtplan = rtplan.rtplan(fname,MSW_to_protons=False)
else:
	fname = sys.argv[-1]
	rtplan = rtplan.rtplan(fname)

#write(rtplan.spots,fname+'spots.txt')
#write(rtplan.layers,fname+'layers.txt')
#write(rtplan.fields,fname+'fields.txt')

spotdata=rtplan.getspotdata()
layerdata=rtplan.getlayerdata()

nrfields=len(rtplan.fields)

if nrfields > 1:
    plotke = plt.subplots(nrows=2, ncols=nrfields, sharex='col', sharey='row')
    #f, ax1 = plt.subplots(nrows=1, ncols=rtplan.nrfields, sharex=False, sharey=False)

    first = True
    for fieldnr,(spot,ax) in enumerate(zip(spotdata,plotke[-1][0])): #0 is eerste rij
        ax.scatter(spot[0],spot[1],marker='x',alpha=0.1,c='black',clip_on=False)
        
        ax.set_xlim(min(spot[0]),max(spot[0]))
        ax.set_ylim(min(spot[1]),max(spot[1]))
        
        ax.semilogy()
        if first:
            ax.set_ylabel('Spots [nr. protons]')
            first=False
        #ax.set_xlabel('$E$ [MeV]')
        plot.texax(ax)
        ax.set_title('Field nr. '+str(fieldnr+1)+"\n"+str(len(spot[0]))+" spots")
        
    first = True
    for layer,ax in zip(layerdata,plotke[-1][1]): #1 is tweede rij
        ax.hist(layer[0],bins=len(layer[0])*10,weights=layer[1],bottom=min(layer[1])/100.,histtype='bar',color='black')
        
        ax.set_xlim(min(layer[0]),max(layer[0]))
        ax.set_ylim(10.**int(math.log10(min(layer[1]))),max(layer[1]))
        #print 10.**int(math.log10(min(layer[1])))
        ax.semilogy()
        if first:
            ax.set_ylabel('Layers [nr. protons]')
            first=False
        ax.set_xlabel('$E$ [MeV]')
        ax.set_title(str(len(layer[0]))+" energy layers")
        plot.texax(ax)
        
else:
    plotke = plt.subplots(nrows=2, ncols=1, sharex='col', sharey='row')

    ax = plotke[-1][0] #0 is eerste kolom
    spot=spotdata[0]
    
    ax.scatter(spot[0],spot[1],marker='x',alpha=0.1,c='black',clip_on=False)
    
    ax.set_xlim(min(spot[0]),max(spot[0]))
    ax.set_ylim(min(spot[1]),max(spot[1]))
    
    ax.semilogy()
    ax.set_ylabel('Spots [nr. protons]')
    plot.texax(ax)
    ax.set_title('Single Field'+"\n"+str(len(spot[0]))+" spots")
    
    ax = plotke[-1][1]
    layer=layerdata[0]
    
    ax.hist(layer[0],bins=len(layer[0])*10,weights=layer[1],bottom=min(layer[1])/10.,histtype='bar',color='black')

    ax.set_xlim(min(layer[0]),max(layer[0]))
    ax.set_ylim(10.**int(math.log10(min(layer[1]))),max(layer[1]))
    ax.semilogy()
    ax.set_ylabel('Layers [nr. protons]')
    ax.set_xlabel('$E$ [MeV]')
    ax.set_title(str(len(layer[0]))+" energy layers")
    plot.texax(ax)
    

plotke[0].savefig(fname[:-4]+'-plot.pdf', bbox_inches='tight')
plt.close('all')
