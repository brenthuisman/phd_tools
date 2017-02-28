#!/usr/bin/env python
import argparse,rtplan,plot,math,numpy as np,matplotlib
from tableio import write
from glob import glob
import matplotlib as mpl

parser = argparse.ArgumentParser(description='RTPlanstructure plotter.')
parser.add_argument('--noproc', action='store_true')
parser.add_argument('--nonorm', action='store_true')
parser.add_argument('--nomu', action='store_true')
parser.add_argument('--dump', action='store_true')
parser.add_argument('--scatter', action='store_true')
parser.add_argument('files', nargs='*')  # This is it!!
args = parser.parse_args()

if len(args.files)<1:
	print "no files given or found. exiting..."
	quit()
print "openening",args.files

rtplan = rtplan.rtplan(args.files,norm2nprim=(not args.nonorm),MSWtoprotons=(not args.nomu),noproc=(args.noproc))

outname = args.files[0][:-4]+('nonorm' if args.nonorm else '')+('nomu' if args.nomu else '')+('noproc' if args.noproc else '')+('scatter' if args.scatter else '')+'-plot.pdf'

if args.dump:
	write(rtplan.spots,outname+'spots.txt')
	write(rtplan.layers,outname+'layers.txt')
	write(rtplan.fields,outname+'fields.txt')

spotdata=rtplan.getspotdata()
layerdata=rtplan.getlayerdata()

MSW=[]
for spot in rtplan.spots:
	MSW.append(spot[-1])

#spot_weight_mean = np.median(MSW)
spot_weight_mean = np.mean(MSW)

nrfields=len(rtplan.fields)

fontsize=6
mpl.rcParams['xtick.labelsize'] = fontsize
mpl.rcParams['ytick.labelsize'] = fontsize
mpl.rcParams['axes.titlesize'] = fontsize
mpl.rcParams['axes.labelsize'] = fontsize

plotke = plot.subplots(nrows=2, ncols=nrfields, sharex='col', sharey='row')
plotke[0].get_axes()[0].annotate('Total nr of primaries: '+plot.sn(rtplan.TotalMetersetWeight)+'. Mean spot weight: '+plot.sn(spot_weight_mean), (0.5, 0.96), xycoords='figure fraction', ha='center', fontsize=fontsize)

if nrfields == 1:
	spotaxes = [plotke[-1][0]] #0 is eerste kolom
	layaxes = [plotke[-1][1]] #0 is eerste kolom
	spotloop= [spotdata[0]]
	layloop = [layerdata[0]]
else:
	spotaxes = plotke[-1][0] #0 is eerste kolom
	layaxes = plotke[-1][1] #0 is eerste kolom
	spotloop = spotdata
	layloop = layerdata

first = True
layer_min_y = 1e10
layer_max_y = 1e1
#vmax=10

for fieldnr,(spot,ax) in enumerate(zip(spotloop,spotaxes)): #0 is eerste rij
	if len(spot) == 0:
		continue
	try:
		if args.scatter:
			ax.scatter(spot[0],spot[1],marker='x',alpha=0.1,c='black',clip_on=False)
			ax.set_xlim(min(spot[0]),max(spot[0]))
		else:
			xbins = plot.bincenters_to_binedges(sorted(list(set(spot[0]))))
			ybins = np.logspace(np.log10(min(spot[1])),np.log10(max(spot[1])),30,endpoint=True)
			
			counts, _, _ = np.histogram2d(spot[0], spot[1], bins=(xbins, ybins))
			#if vmax < np.max(counts):
				#vmax = np.max(counts)
			a = ax.pcolormesh(xbins, ybins, counts.T,cmap='coolwarm',norm=matplotlib.colors.LogNorm(),vmin=1e0,vmax=1e2)
			#a = ax.pcolormesh(xbins, ybins, counts.T,cmap='Greys',norm=matplotlib.colors.LogNorm(), vmin=0.7)
			
			ax.set_xlim(min(xbins),max(xbins))

		ax.set_ylim(min(spot[1]),max(spot[1])*1.05)
	
		ax.semilogy()
	except Exception as e:
		print str(e)
		pass
	if first:
		ax.set_ylabel('Spots\nNr. protons')
		first=False
	#ax.set_xlabel('$E$ [MeV]')
	plot.texax(ax)
	ax.set_title('Field '+str(fieldnr+1)+"\n"+str(len(spot[0]))+" spots")
	
first = True
for layer,ax in zip(layloop,layaxes): #1 is tweede rij
	try:
		xbins = plot.bincenters_to_binedges(sorted(layer[0]))
		ax.hist(layer[0],bins=xbins,weights=layer[1],bottom=min(layer[1])/100.,histtype='bar',color='grey',linewidth=0.2)
		
		new_layer_min_y = min(layer[1])/1.5
		new_layer_max_y = max(layer[1])*1.5
		if new_layer_min_y < layer_min_y:
			layer_min_y=new_layer_min_y
			ax.set_ylim(ymin=layer_min_y)
		if new_layer_max_y > layer_max_y:
			layer_max_y=new_layer_max_y
			ax.set_ylim(ymax=layer_max_y)
		
		ax.semilogy()
	except:
		pass
	#print 10.**int(math.log10(min(layer[1])))
	if first:
		ax.set_ylabel('Layers\nNr. protons')
		first=False
	ax.set_xlabel('$E$ [MeV]')
	ax.set_title(str(len(layer[0]))+" energy layers")
	plot.texax(ax)


if not args.scatter:
	cb = plotke[0].colorbar(a, ax=plotke[-1].ravel().tolist(), aspect=50)
	cb.outline.set_visible(False)
	cb.set_label('Spotcount', rotation=270)

plotke[0].savefig(outname, bbox_inches='tight')
print 'Plot saved to',outname
plot.close('all')
