#!/usr/bin/env python
import sys,math,subprocess,threading,rtplan as rp,geo,ask_yn,mac

'''
This script runs a Gate simulation (mac/main.mac), taking into account different fields and different changing geometries between fields.

* Read an RT plan and extracts the number of fields and the rotation angles
* Generate for each field a macrofile with the geometry properly set
* Run the simulation for each field in paralel (poor mans multiprocessing for free)
* Afterwards, ???. Not sure if we should merge anything afterwards. perhaps its beter to keep any analysis separated per field, and in the frame of the detector.

'''

macfile = sys.argv[-2]
primaries = sys.argv[-1]
rtplanfile = mac.getrtplanfile(macfile)
#rtplanfile = rtplan.sourcefile

if ask_yn.ask_yn("Do you want to start a paralel simulation for each field using "+macfile+" and "+primaries+" primaries and rtplan: "+rtplanfile) == False:
	print "Mission abort."
	sys.exit()

if ask_yn.ask_yn("Does your macfile have the following variables: primaries,notFieldID,rotAng,rotAx,rotAy,rotAz,fieldID ?\nTerrible things will happen if you didn't!") == False:
	print "Mission abort."
	sys.exit()

primaries = int(primaries)
rtplan = rp.rtplan(rtplanfile)

#use to weight dose per beam.
TCMW = 0
for field in rtplan.metadata:
	TCMW+=field[-2]

print "Starting Gate simulation with",primaries,"primaries, ratio per field as defined in RTplan. Please wait..."

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
	print "Finished Field!"

#the default position of the half cylinder is in the pos z direction, with the bulge in the pos y direction. A rotation over x of minus 90 degrees puts it in the x,y-plane, which is the plane of the gantry angle.
#a gantry angle of 0 is in the negative y direction. An increasing angle is a rotation about the z axis in the positive x direction.

threadlist=[]
for field in rtplan.metadata:
	gantryAngle=field[-1]
	fieldID = field[0]
	notFieldID = rtplan.metadata[fieldID-2][0] #ugly hack, change to cope with >2 fields. Gauthier says 2 or 3 are typical
	CMW=field[-2] #use to weight dose per beam.
	
	heading=math.radians(0)
	attitude=math.radians(gantryAngle)
	bank=math.radians(-90)
	rotAng,rotAx,rotAy,rotAz=geo.rotator(heading,attitude,bank)
	
	command = "Gate -a '[primaries,"+str(int(primaries*CMW/TCMW))+"] [notFieldID,"+str(notFieldID)+"] [rotAng,"+str(rotAng)+"] [rotAx,"+str(rotAx)+"] [rotAy,"+str(rotAy)+"] [rotAz,"+str(rotAz)+"] [fieldID,"+str(fieldID)+"]' "+macfile
	
	threadlist.append(popenAndCall(done,command))
	#os.system("Gate -a '[primaries,"+str(primaries)+"] [notFieldID,"+str(notFieldID)+"] [rotAng,"+str(rotAng)+"] [rotAx,"+str(rotAx)+"] [rotAy,"+str(rotAy)+"] [rotAz,"+str(rotAz)+"] [fieldID,"+str(fieldID)+"]' mac/param.mac")

for thread in threadlist:
	thread.join()

print "Exiting..."
