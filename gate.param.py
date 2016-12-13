#!/usr/bin/env python
import argparse

'''
run afterwards with
find -name 'autogen*' -exec gate_run_submit_cluster_nomove.sh {} 1 \;
'''

parser = argparse.ArgumentParser(description='launch multiple params.')
parser.add_argument('--mac')
parser.add_argument('--param')
args = parser.parse_args()

def readmac(fn):
	f = open(fn)
	text = f.read()
	f.close()
	return text

def readparam(filename,headersize=0):
    sourcefile = open(filename,'r')
    newarr=[]
    for line in sourcefile.readlines()[headersize:]:
        try:
            newarr.append([float(x) for x in line.strip('\n').replace('--','0').replace(',','.').split()])
        except ValueError:
            newarr.append([x for x in line.strip('\n').replace('--','0').replace(',','.').split()])
    sourcefile.close()
    return newarr

paramfile = readparam(args.param)
macfile = readmac(args.mac)
assert args.mac.startswith('param-')
assert args.mac.endswith('.mac')

for val in range(len(paramfile[0]))[1:]:
	parstr = ''
	parfstr = ''
	
	for par in range(len(paramfile)):
		parstr = parstr + '/control/alias ' + paramfile[par][0] + ' ' + paramfile[par][val] + '\n'
		parfstr = parfstr + '-' + paramfile[par][0] + '-' + paramfile[par][val]
	
	
	outname = 'autogen-'+args.mac.replace('.mac','').replace('param-','')+parfstr+'.mac'
	#print outname
	#print parstr+macfile
	with open(outname,'w') as newmacfile:
		newmacfile.write(parstr)
		newmacfile.write(macfile)



#def popenAndCall(onExit, popenArgs):
    #"""
    #Runs the given args in a subprocess.Popen, and then calls the function
    #onExit when the subprocess completes.
    #onExit is a callable object, and popenArgs is a list/tuple of args that 
    #would give to subprocess.Popen.
    #"""
    #def runInThread(onExit, popenArgs):
        #proc = subprocess.Popen(popenArgs,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #proc.wait()
        #onExit()
        #return
    #thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
    #thread.start()
    ## returns immediately after the thread starts
    #return thread

#def done():
	#print "Finished subprocess!"

#threadlist=[]
#for para in param[0][1:]:
	#command = "Gate -a '["+param[0][0]+","+str(para)+"]' "+macfile
	#threadlist.append(popenAndCall(done,command))

#for thread in threadlist:
	#thread.join()
