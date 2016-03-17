#!/usr/bin/env python
import sys,image
from subprocess import call

if len(sys.argv) < 2:
	print "Specify a maskfile."
	sys.exit()

maskfile = sys.argv[-1]

spacing = 2
size = 399

maskimagefile = sys.argv[-1][:-4]+'.mhd'
spacingstr = str(spacing)
sizeinvox = str(size/spacing)
call(["rtkdrawgeometricphantom","--phantomfile",maskfile,"--dimension",sizeinvox,"--spacing",spacingstr,"--output",maskimagefile])
call(["clitkCropImage","-i",maskimagefile,"-o",maskimagefile,"--BG=-1000"])
call(["clitkBinarizeImage","-i",maskimagefile,"-o",maskimagefile,"-l","0.5","-u","1.5"]) #the intensity egion that is 1, and not 0
#call(["clitkImageConvert","-i",maskimagefile,"-o",maskimagefile,"-t","float"]) #to float, so our image class can read it (TODO: find out how numpy can read raw UCHAR)
#call(["clitkImageConvert","-i",maskimagefile,"-o",maskimagefile,"-c"])

# these lines will output a second mhd file that takes care of adding the fourth dimensions,
# useful when you want to use clitkCropImage with --like.
data = image.image(maskimagefile)
data.tofake4d()