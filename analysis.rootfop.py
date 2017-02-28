#!/usr/bin/env python
import dump, numpy as np,glob2 as glob,auger

##(rootfiles,field,bins,lowrange,highrange):
#Y=dump.dump(['pgprod-worldframe.root'],'X',300,-150,150)
#X=np.linspace(-149.5,149.5,300)
#auger.get_fop(X,Y,plot='patient-worldframe.pdf')


#X=np.linspace(-39,79,60)

##Y=dump.dump(['output/iba-perdet.root'],'X',60,-40,80)
##auger.get_fop(X,Y,plot='iba-perdet.pdf')

##Y=dump.dump(['output/iba-perdet-world.root'],'X',60,-40,80)
##auger.get_fop(X,Y,plot='iba-perdet-worldframe.pdf')

#Y=dump.dump(['output/ipnl-perdet.root'],'X',60,-40,80)
#auger.get_fop(X,Y,plot='ipnl-perdet.pdf')

##Y=dump.dump(['output/ipnl-perdet-world.root'],'X',60,-40,80)
##auger.get_fop(X,Y,plot='ipnl-perdet-world.pdf')



lst=dump.thist2np_xy('GammProdCount-Prod.root')
auger.get_fop(lst['histo'][0],lst['histo'][1],plot='GammProdCount.pdf')
