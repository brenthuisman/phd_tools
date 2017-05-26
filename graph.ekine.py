#!/usr/bin/env python
import numpy as np,sys,plot,pickle,dump

if len(sys.argv) < 2:
	print "Specify at least one input."
	quit()
filesin = sys.argv[1:]

for filename in filesin:
	data = np.fromfile(filename, dtype='<f4')
	x = np.linspace(0,10,250)
	
	f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
	
	ax1.step(x,data, label='PG production',color='steelblue',alpha=0.8, where='mid')

	ax1.set_xlim(0,10)
	ax1.set_ylim(0,0.0025)
	ax1.set_ylabel('Yield (a.u.)')
	ax1.set_xlabel('Energy (MeV)')
	
	#plot.legend(prop={'size':10},bbox_to_anchor=(1.2, 1.),frameon=False)
	plot.texax(ax1)

	ax1.legend(frameon = False)#,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'upper right')

	f.savefig('graph-ekine.pdf', bbox_inches='tight')
	plot.close('all')
