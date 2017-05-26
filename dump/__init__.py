import ROOT as r,pickle,numpy as np

def dump(rootfiles,field,bins,lowrange,highrange,statfile=None):
    #dump is fast because of TTree.Draw
    if statfile != None:
        #get nr primaries
        prims=0
        #print '/'.join(rootfiles[0].split('/')[:-1])+'/stat-proton.txt'
        header = open('/'.join(rootfiles[0].split('/')[:-1])+'/stat-proton.txt','r')
        for line in header:
            newline = line.strip()
            if len(newline)==0:
                continue
            if 'NumberOfEvents' in newline:
                prims = float(newline.split()[-1])
        if prims is 0:
            print "No valid number of primaries detected. Aborting..." 
            return
    outdata = [0]*bins

    for rootfile in rootfiles:
        tfile=r.TFile(rootfile)
        tree=tfile.Get("PhaseSpace")
        #http://root.cern.ch/root/html/TTree.html#TTree:Draw@1
        tree.Draw(field+'>>hnew('+str(bins)+','+str(lowrange)+','+str(highrange)+')')
        #Note that this returns a TH1F, not TH1D, so not very precise.
        hnew = r.gPad.GetPrimitive("hnew");
        #because root is a bitch, it is 1-indexed. so thats why theres a shift.
        for i in range(1,hnew.GetNbinsX()+1):
            #print hnew.GetBinCenter(i), hnew.GetBinContent(i)
            if statfile == None:
                outdata[i-1] = float(hnew.GetBinContent(i))
            else:
                outdata[i-1] = float(hnew.GetBinContent(i))/float(prims)

    return outdata


def scaletree(rootfile,fields,**kwargs):
    
    tfile=r.TFile(rootfile)
    tree=tfile.Get("PhaseSpace")
    
    retval = {}
    for field in fields:
        retval[field] = []
    
    for event in tree:
        checks = True
        for key in kwargs: #check every condition
            
            datapoint = getattr(event,key)
            if type(datapoint) == str:
                datapoint = datapoint.split('\x00')[0]
                #There is a nasty thing with ROOT outputting strings with an invisible character appended to any string it outputs. Sometimes even more than one...
                
                # first check for negation
                if kwargs[key].startswith('not_'):
                    if datapoint == kwargs[key][4:]:
                        checks = False
                else:
                    if not datapoint == kwargs[key]:
                        checks = False
                        
            else:
                if not datapoint == kwargs[key]:
                    checks = False
            if not checks:
                break
        if checks:
            for field in fields:
                if type(getattr(event,field)) == str:
                    # ROOT sanitation on isle 4 ...
                    retval[field].append( getattr(event,field).split('\x00')[0] )
                else:
                    retval[field].append( getattr(event,field) )
    return retval
    

def get1D(rootfile,field,**kwargs):
    return scaletree(rootfile,[field],**kwargs)[field]
    

def get2D(rootfile,fields,**kwargs):
    return scaletree(rootfile,fields,**kwargs)
    

def getyield(rootfiles):
    #get nr primaries
    prims=0
    header = open('/'.join(rootfiles[0].split('/')[:-1])+'/stat-proton.txt','r')
    for line in header:
        newline = line.strip()
        if len(newline)==0:
            continue
        if 'NumberOfEvents' in newline:
            prims = float(newline.split()[-1])
    if prims is 0:
        print "No valid number of primaries detected. Aborting..." 
        return

    totentries = 0
    for rootfile in rootfiles:
        tfile=r.TFile(rootfile)
        tree=tfile.Get("PhaseSpace")
        totentries += tree.GetEntries()

    return float(totentries)/(len(rootfiles)*prims)

def getcount(rootfiles):
    totentries = 0
    for rootfile in rootfiles:
        tfile=r.TFile(rootfile)
        tree=tfile.Get("PhaseSpace")
        totentries += tree.GetEntries()

    return totentries

def savedump(rootfiles,field,bins,lowrange,highrange,outname):
    dumpdata = dump(rootfiles,field,bins,lowrange,highrange)
    #print dumpdata
    with open(outname,'w') as thefile:
        pickle.dump(dumpdata, thefile)


def thist2np(infile,dt='<f4'):
    tfile=r.TFile(infile,"READ")
    retval={}
    for item in tfile.GetListOfKeys():
        outname=item.ReadObj().GetName()
        outdata=[]
        for i in range(item.ReadObj().GetNbinsX()):
            #print hnew.GetBinCenter(i), hnew.GetBinContent(i)
            outdata.append(float(item.ReadObj().GetBinContent(i+1)))
        #outdata=np.array(outdata, dtype=dt)
        #outdata.tofile(outname+'.raw')
        retval[outname]=outdata
    return retval


def thist2np_xy(infile):
    tfile=r.TFile(infile,"READ")
    retval={}
    for item in tfile.GetListOfKeys():
        outname=item.ReadObj().GetName()
        outdata_x=[]
        outdata_y=[]
        for i in range(item.ReadObj().GetNbinsX()):
            outdata_x.append(float(item.ReadObj().GetXaxis().GetBinCenter(i+1)))
            outdata_y.append(float(item.ReadObj().GetBinContent(i+1)))
        retval[outname]=[outdata_x,outdata_y]
    return retval
