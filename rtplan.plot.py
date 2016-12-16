#!/usr/bin/env python
import argparse,rtplan,plot,math#,numpy as np
from tableio import write
from glob import glob

parser = argparse.ArgumentParser(description='RTPlanstructure plotter.')
parser.add_argument('--noproc', action='store_true')
parser.add_argument('--nonorm', action='store_true')
parser.add_argument('--nomu', action='store_true')
parser.add_argument('--dump', action='store_true')
parser.add_argument('files', nargs='*')  # This is it!!
args = parser.parse_args()

if len(args.files)<1:
	print "no files given or found. exiting..."
	quit()
print "openening",args.files

rtplan = rtplan.rtplan(args.files,norm2nprim=(not args.nonorm),MSWtoprotons=(not args.nomu),noproc=(args.noproc))

outname = args.files[0][:-4]+('nonorm' if args.nonorm else '')+('nomu' if args.nomu else '')+('noproc' if args.noproc else '')+'-plot.pdf'

if args.dump:
	write(rtplan.spots,outname+'spots.txt')
	write(rtplan.layers,outname+'layers.txt')
	write(rtplan.fields,outname+'fields.txt')

spotdata=rtplan.getspotdata()
layerdata=rtplan.getlayerdata()

nrfields=len(rtplan.fields)

if nrfields > 1:
	plotke = plot.subplots(nrows=2, ncols=nrfields, sharex='col', sharey='row')
	plotke[0].get_axes()[0].annotate('Total nr of primaries: '+plot.sn(rtplan.TotalMetersetWeight), (0.5, 0.96), xycoords='figure fraction', ha='center', fontsize=8)
	#plotke[0].suptitle('Total nr of primaries: '+plot.sn(rtplan.TotalMetersetWeight), fontsize=8)
	#f, ax1 = plot.subplots(nrows=1, ncols=rtplan.nrfields, sharex=False, sharey=False)

	first = True
	for fieldnr,(spot,ax) in enumerate(zip(spotdata,plotke[-1][0])): #0 is eerste rij
		if len(spot) == 0:
			continue
		try:
			ax.scatter(spot[0],spot[1],marker='x',alpha=0.1,c='black',clip_on=False)
		
			ax.set_xlim(min(spot[0]),max(spot[0]))
			ax.set_ylim(min(spot[1]),max(spot[1]))
		
			ax.semilogy()
		except:
			pass
		if first:
			ax.set_ylabel('Spots [nr. protons]')
			first=False
		#ax.set_xlabel('$E$ [MeV]')
		plot.texax(ax)
		ax.set_title('Field nr. '+str(fieldnr+1)+": "+str(len(spot[0]))+" spots", fontsize=8)
		
	first = True
	for layer,ax in zip(layerdata,plotke[-1][1]): #1 is tweede rij
		try:
			ax.hist(layer[0],bins=len(layer[0])*10,weights=layer[1],bottom=min(layer[1])/100.,histtype='bar',color='black')
			ax.set_xlim(min(layer[0]),max(layer[0]))
			ax.set_ylim(10.**int(math.log10(min(layer[1]))),max(layer[1]))
			ax.semilogy()
		except:
			pass
		#print 10.**int(math.log10(min(layer[1])))
		if first:
			ax.set_ylabel('Layers [nr. protons]')
			first=False
		ax.set_xlabel('$E$ [MeV]')
		ax.set_title(str(len(layer[0]))+" energy layers", fontsize=8)
		plot.texax(ax)
		
else:
	plotke = plot.subplots(nrows=2, ncols=1, sharex='col', sharey='row')
	plotke[0].get_axes()[0].annotate('Total nr of primaries: '+plot.sn(rtplan.TotalMetersetWeight), (0.5, 0.96), xycoords='figure fraction', ha='center', fontsize=8)
	#plotke[0].suptitle('Total nr of primaries: '+plot.sn(rtplan.TotalMetersetWeight), fontsize=8)

	ax = plotke[-1][0] #0 is eerste kolom
	spot=spotdata[0]
	
	ax.scatter(spot[0],spot[1],marker='x',alpha=0.1,c='black',clip_on=False)
	
	ax.set_xlim(min(spot[0]),max(spot[0]))
	ax.set_ylim(min(spot[1]),max(spot[1]))
	
	ax.semilogy()
	ax.set_ylabel('Spots [nr. protons]')
	plot.texax(ax)
	ax.set_title('Single Field'+": "+str(len(spot[0]))+" spots", fontsize=8)
	
	ax = plotke[-1][1]
	layer=layerdata[0]
	
	ax.hist(layer[0],bins=len(layer[0])*10,weights=layer[1],bottom=min(layer[1])/10.,histtype='bar',color='black')

	ax.set_xlim(min(layer[0]),max(layer[0]))
	ax.set_ylim(10.**int(math.log10(min(layer[1]))),max(layer[1]))
	ax.semilogy()
	ax.set_ylabel('Layers [nr. protons]')
	ax.set_xlabel('$E$ [MeV]')
	ax.set_title(str(len(layer[0]))+" energy layers", fontsize=8)
	plot.texax(ax)
	

plotke[0].savefig(outname, bbox_inches='tight')
plot.close('all')
