#!/usr/bin/env python
import os,sys,dump

filename = sys.argv[-1]

rootfiles = [x.strip() for x in os.popen("find "+sys.argv[-1]+" -print | grep -i '.root$'").readlines()]

print dump.getyield(rootfiles)
