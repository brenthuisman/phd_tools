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
maskbeam = image.image("../mask-beamline/maskfile.mhd")
# maskbox1 = image.image("../mask-boxes/phantom_Parodi_TNS_2005_52_3_modified.maskfile1.mhd")
maskbox2 = image.image("../mask-box2/phantom_Parodi_TNS_2005_52_3_modified.maskfile2.mhd")
maskbox8 = image.image("../mask-box8/phantom_Parodi_TNS_2005_52_3_modified.maskfile8.mhd")
# maskbox5 = image.image("../mask-boxes/phantom_Parodi_TNS_2005_52_3_modified.maskfile5.mhd")
# maskbox7 = image.image("../mask-boxes/phantom_Parodi_TNS_2005_52_3_modified.maskfile7.mhd")
mask90pc = image.image("../mask90pc/mean.mhd") #is simply analog1B mean
mask90pc.to90pcmask()

for filename in sources:
	im = image.image(filename)

	im.save1dlist("E.nofilter.pylist",[1,1,1,0]) #no masks whatsoever
	im.save1dlist("Z.nofilter.pylist",[1,1,0,1])

	im.applymask(mask90pc,maskspect)#default
	im.savesum(".sum.pylist")
	
	imbeam = image.image(filename)
	imbeam.applymask(mask90pc,maskspect,maskbeam)
	imbox2 = image.image(filename)
	imbox2.applymask(mask90pc,maskspect,maskbox2)
	imbox8 = image.image(filename)
	imbox8.applymask(mask90pc,maskspect,maskbox8)

	spect = im.save1dlist("E.std.pylist",[1,1,1,0])
	spectb = imbeam.save1dlist("E.beam.pylist",[1,1,1,0])
	spectb2 = imbox2.save1dlist("E.box2.pylist",[1,1,1,0])
	spectb8 = imbox8.save1dlist("E.box8.pylist",[1,1,1,0])
	z = im.save1dlist("Z.std.pylist",[1,1,0,1])
	zb = imbeam.save1dlist("Z.beam.pylist",[1,1,0,1])
	zb2 = imbox2.save1dlist("Z.box2.pylist",[1,1,0,1])
	zb8 = imbox8.save1dlist("Z.box8.pylist",[1,1,0,1])

	# imbox1 = image.image(filename)
	# imbox1.applymask(mask90pc,maskspect,maskbox1)
	# imbox1.save1dlist("E.box1.pylist",[1,1,1,0])
	# imbox1.save1dlist("Z.box1.pylist",[1,1,0,1])

	# imbox5 = image.image(filename)
	# imbox5.applymask(mask90pc,maskspect,maskbox5)
	# imbox5.save1dlist("E.box5.pylist",[1,1,1,0])
	# imbox5.save1dlist("Z.box5.pylist",[1,1,0,1])

	# imbox5 = image.image(filename)
	# imbox5.applymask(mask90pc,maskspect,maskbox7)
	# imbox5.save1dlist("E.box7.pylist",[1,1,1,0])
	# imbox5.save1dlist("Z.box7.pylist",[1,1,0,1])

	print filename, "projected..."
