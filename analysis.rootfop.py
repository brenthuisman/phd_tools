#!/usr/bin/env python
import dump, numpy as np,glob2 as glob,auger

#(rootfiles,field,bins,lowrange,highrange):
Y=dump.dump(['output/pgprod-worldframe.root'],'X',300,-150,150)
X=np.linspace(-149.5,149.5,300)

auger.get_fop(X,Y,plot='patient-worldframe.pdf')

