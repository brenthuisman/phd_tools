#!/usr/bin/env python
import sys,rtplan,matplotlib.pyplot as plt,plot,math

rtplan = rtplan.rtplan(sys.argv[-1])
#rtplan.savelayerhistos()
#rtplan.savespothistos()

spotdata=rtplan.getspotdata()
layerdata=rtplan.getlayerdata()

if rtplan.nrfields > 1:
    plotke = plt.subplots(nrows=2, ncols=rtplan.nrfields, sharex='col', sharey='row')
    #f, ax1 = plt.subplots(nrows=1, ncols=rtplan.nrfields, sharex=False, sharey=False)

    first = True
    for fieldnr,(spot,ax) in enumerate(zip(spotdata,plotke[-1][0])): #0 is eerste rij
        ax.scatter(spot[0],spot[1],marker='x',alpha=0.1,c='black')
        
        ax.set_xlim(min(spot[0]),max(spot[0]))
        ax.set_ylim(min(spot[1]),max(spot[1]))
        ax.semilogy()
        if first:
            ax.set_ylabel('Spots [nr. protons]')
            first=False
        #ax.set_xlabel('$E$ [MeV]')
        plot.texax(ax)
        ax.set_title('Field nr. '+str(fieldnr+1))
        
    first = True
    for layer,ax in zip(layerdata,plotke[-1][1]): #1 is tweede rij
        ax.hist(layer[0],bins=len(layer[0])*10,weights=layer[1],bottom=min(layer[1])/10.,histtype='bar',color='black')
        
        ax.set_xlim(min(layer[0]),max(layer[0]))
        ax.set_ylim(10.**int(math.log10(min(layer[1]))),max(layer[1]))
        ax.semilogy()
        if first:
            ax.set_ylabel('Layers [nr. protons]')
            first=False
        ax.set_xlabel('$E$ [MeV]')
        plot.texax(ax)
        
else:
    plotke = plt.subplots(nrows=2, ncols=1, sharex=False, sharey='row')

    ax = plotke[-1][0] #0 is eerste kolom
    spot=spotdata[0]
    
    ax.scatter(spot[0],spot[1],marker='x',alpha=0.1,c='black')
    
    ax.set_xlim(min(spot[0]),max(spot[0]))
    ax.set_ylim(min(spot[1]),max(spot[1]))
    
    ax.semilogy()
    ax.set_ylabel('Spots [nr. protons]')
    plot.texax(ax)
    ax.set_title('Single Field')
    
    ax = plotke[-1][1]
    layer=layerdata[0]
    
    ax.hist(layer[0],bins=len(layer[0])*10,weights=layer[1],bottom=min(layer[1])/10.,histtype='bar',color='black')

    ax.set_xlim(min(layer[0]),max(layer[0]))
    ax.set_ylim(10.**int(math.log10(min(layer[1]))),max(layer[1]))
    ax.semilogy()
    ax.set_ylabel('Layers [nr. protons]')
    ax.set_xlabel('$E$ [MeV]')
    plot.texax(ax)
    

plotke[0].savefig(sys.argv[-1][:-3]+'plot.pdf', bbox_inches='tight')
plt.close('all')
