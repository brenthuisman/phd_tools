#!/usr/bin/env python
import sys,subprocess,threading,ask_yn,tableio

'''
This script runs a Gate simulation (mac/main.mac) with different parameters simultaneously.
It expects a singleline parameter file with whitespace-separated values and the first value being the parameter name as found in the macfile.

TODO: Cope with multiple parameters.

'''

macfile = sys.argv[-2]
paramfile = sys.argv[-1]

if ask_yn.ask_yn("Do you want to start a paralel simulation for "+macfile+" and the parameters found in "+paramfile) == False:
    print "Mission abort."
    sys.exit()

param = tableio.read(paramfile)

print "Starting Gate simulation. Please wait..."

def popenAndCall(onExit, popenArgs):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    onExit when the subprocess completes.
    onExit is a callable object, and popenArgs is a list/tuple of args that 
    would give to subprocess.Popen.
    """
    def runInThread(onExit, popenArgs):
        proc = subprocess.Popen(popenArgs,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        proc.wait()
        onExit()
        return
    thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
    thread.start()
    # returns immediately after the thread starts
    return thread

def done():
	print "Finished subprocess!"

threadlist=[]
for para in param[0][1:]:
	command = "Gate -a '["+param[0][0]+","+str(para)+"]' "+macfile
	threadlist.append(popenAndCall(done,command))

for thread in threadlist:
	thread.join()

print "Exiting..."
