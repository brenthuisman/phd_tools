#!/usr/bin/env python
import os,sys,subprocess,glob2 as glob

count = 10

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
print len(sources), "files found:", sources[:3], '...', sources[-3:]

#merge
outfile = None
for index,source in enumerate(sources):
	if index%count==0:
		if index is not 0:
			# every tenth iteration, except the 0th, divide old outfile
			os.popen("clitkImageArithm -s "+str(count)+" -t 11 -i "+outfile+" -o "+outfile)
		#update name and make new outfile
		outfile = "group10." + str(index) + ".mhd"
		#start new file, copy this entry
		#subprocess.check_output(["clitkImageArithm -i "+filename+" -o "+mean+" -t 1 -s 1"],shell=True)
		os.popen("clitkImageArithm -i "+source+" -o "+outfile+" -t 1 -s 1")
		continue
	os.popen("clitkImageArithm -t 0 -i "+source+" -j "+outfile+" -o "+outfile)
#divide last file too.
os.popen("clitkImageArithm -s "+str(count)+" -t 11 -i "+outfile+" -o "+outfile)

print "Done!"
