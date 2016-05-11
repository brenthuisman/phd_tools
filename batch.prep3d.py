#!/usr/bin/env python
'''
This tool is a general purpose tool for batch processing of image-output.
Given a set of input images, it will output a mean and variance image, so a mean and variance per voxel.
In addition, it outputs an inverse variance image, in case you want to compute the efficiency.
'''
import sys,subprocess,glob2 as glob,image

if len(sys.argv) is not 2:
	print "No input file names given, assume analog.mhd"
	indir = "."
	infile = "analog.mhd"
else:
	indir = "."
	infile = str(sys.argv[-1])

sources = glob.glob(indir+"/**/"+infile)#,recursive=True
if len(sources) < 2:
	print "None or one file found, exiting..."
	sys.exit()

nr = len(sources)

print nr, "files found:", sources[:3], '...', sources[-3:]

if nr>10:
	print "using only the first 10 files..."
	sources=sources[0:10]
	nr=len(sources)

#apply 1-8mev mask and turn all into 3d:
msk = image.image("../mask-spect1-8/finalmask.mhd")

threedees=[]
for source in sources:
	img = image.image(source)
	img.applymask(msk)
	threedees.append(img.saveprojection(".3d", [0,0,0,1]))

print "Converted",len(threedees),"files into 3d images."

mean=indir+"/mean3d.mhd"
var=indir+"/var3d.mhd"

N = len(threedees)
#NNm1 = str(N*(N-1))
Nm1 = str(N-1)
N=str(N)

#
# 		N=float(len(binn))
# 		mu=sum(binn)/N
# 		sqbinn=[(i-mu)**2 for i in binn]
# 		var= ( sum(sqbinn) ) / (N*(N-1))
#

print "Compute mean..." #sum all data
for index,filename in enumerate(threedees):
	if index is 0:
		#first we copy by multiplting with 1.
		subprocess.check_output(["clitkImageArithm -t 1 -s 1 -i "+filename+" -o "+mean],shell=True)
	else:
		#then we add
		subprocess.check_output(["clitkImageArithm -t 0 -i "+filename+" -j "+mean+" -o "+mean],shell=True)
#now divide by N
subprocess.check_output(["clitkImageArithm -t 11 -s "+N+" -i "+mean+" -o "+mean],shell=True)

print mean,"done."

print "Computing squared difference..." #compute sqdiff for each image
sqdiffs=[]
for index,filename in enumerate(threedees):
	newfile = filename[:-4]+".sqd.mhd"
	sqdiffs.append(newfile)
	#miraculously, clitkImageArithm option 6 is exactly what we need!
	subprocess.check_output(["clitkImageArithm -t 6 -i "+filename+" -j "+mean+" -o "+newfile],shell=True)

print "Compute variance..." #sum sqdiff
for index,filename in enumerate(sqdiffs):
	if index is 0:
		#first we copy by multiplting with 1.
		subprocess.check_output(["clitkImageArithm -t 1 -s 1 -i "+filename+" -o "+var],shell=True)
	else:
		#then we add
		subprocess.check_output(["clitkImageArithm -t 0 -i "+filename+" -j "+var+" -o "+var],shell=True)
#now divide by N*(N-1)
subprocess.check_output(["clitkImageArithm -t 11 -s "+Nm1+" -i "+var+" -o "+var],shell=True)

print var,"done."

for filename in threedees + sqdiffs:
	subprocess.check_output(["rm "+filename],shell=True)
	subprocess.check_output(["rm "+filename[:-4]+".raw"],shell=True)

print "All cleaned up. Exiting..."