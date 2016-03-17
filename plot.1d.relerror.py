#!/usr/bin/env python
import numpy,sys,matplotlib.pyplot as plt,math,operator,pickle

## THIS PLOTS Standard Dev, NOT Variance

#print plt.style.available
#plt.style.use('ggplot')

#nrprim = float(600*28800000)
nrprim = float(1e6)

if len(sys.argv) < 3:
	print "Specify at least one input and one output."
	sys.exit()
filesin = sys.argv[1:-1]
fileout = sys.argv[-1]


def getreldata(list1,list2=[]):
	out=[]
	if list2==[]:
		for item in list1:
			if item > 0.:
				out.append(math.sqrt( item/nrprim ) / item)
			else:
				out.append(1./nrprim)
	else:
		for item1,item2 in zip(list1,list2):
			if item2 > 0.:
				out.append(math.sqrt( item1 ) / item2)
			else:
				out.append(math.sqrt( item1 ))
	return out


for filename in filesin:
	if filename.endswith('.txt'):
		header = open(filename,'r')
		data = []
		for line in header:
			newline = line.strip()
			newline = float(newline.split()[-1])
			data.append( newline )
		plotdata = getreldata(data)
		plt.plot(plotdata[:70], label=filename)
	if filename.endswith('.raw'):
		rawfilenames = filename.split(":")
		data=[]
		if len(rawfilenames) is 2:
			data = numpy.fromfile(rawfilenames[1], dtype='<f4').tolist()
		reldata = numpy.fromfile(rawfilenames[0], dtype='<f4').tolist()
		plotdata = getreldata(reldata,data)
		plt.plot(plotdata[:70], label=filename)
		#plt.plot(plotdata, label=filename)
	if filename.endswith('.pylist') or:
		rawfilenames = filename.split(":")
		data=[]
		if len(rawfilenames) is 2:
			data = pickle.load(open(rawfilenames[1]))
		reldata = [math.sqrt(x) for x in pickle.load(open(rawfilenames[0]))]
		plotdata = getreldata(reldata,data)
		plt.plot(plotdata[:91], label=filename)
		#plt.plot(plotdata, label=filename)
	#plt.plot(data, label=filename)
	plt.ylabel('Counts')
	plt.ylabel('PG energy')
	#plt.legend(loc=4,prop={'size':6})
	plt.legend(prop={'size':10})
	plt.savefig(fileout)

