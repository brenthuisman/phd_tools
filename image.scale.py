#!/usr/bin/env python
import sys,os

outfile = sys.argv[-1]
scale = sys.argv[-2]
infile = sys.argv[-3]

os.popen("clitkImageArithm -t 1 -s "+scale+" -i "+infile+" -o "+outfile)
