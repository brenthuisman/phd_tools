#!/usr/bin/env python
import sys,glob2 as glob,image

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

### Load masks
maskspect = image.image("../mask-spect1-8/finalmask.mhd")
mask90pc = image.image("../mask-90pc/mean.90pcmask.mhd") #is simply analog1B mean
mask90pc.to90pcmask()

for filename in sources:
	im = image.image(filename)

	im.save1dlist("E.nofilter.pylist",[1,1,1,0])
	im.save1dlist("Y.nofilter.pylist",[1,0,1,1])

	im.applymask(mask90pc,maskspect)#default

	spect = im.save1dlist("E.std.pylist",[1,1,1,0])
	z = im.save1dlist("Y.std.pylist",[1,0,1,1])

	print filename, "projected..."
