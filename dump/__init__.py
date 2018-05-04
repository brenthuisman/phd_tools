import ROOT as r,numpy as np,os

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


def scaletreefast(rootfile,fields,**kwargs):
    #DONT USE

    dim = 2 #more not handled right now.
    if type(fields) != list:
        dim = 1
        fields = [fields,fields] #this way, we can avoid ROOT making a TH1 and we can get the unbinned data

    #xlow,xhigh,nx = *kwargs.pop('xbins')
    #if 'ybins' in kwargs:
        #ylow,yhigh,yx = *kwargs.pop('ybins'):
        #assert len(fields) == 2

    tfile=r.TFile(rootfile)
    tree=tfile.Get("PhaseSpace")

    #if len(kwargs) > 0: #FIXME
    cuts=''
    for key in kwargs: #compile 'cut'-string
        cuts+='&&'
        cuts+=str(key)

        if kwargs[key].startswith('not_'):
            cuts+='!='
            kwargs[key] = kwargs[key][4:]
        else:
            cuts+='=='

        if kwargs[key] == True:
            cuts+='true'
        elif kwargs[key] == False:
            cuts+='false'
        elif type(kwargs[key]) == str:
            cuts+='\"'+kwargs[key]+'\"'
        else:
            cuts+=str(kwargs[key])
    if cuts.startswith('&&'):
        cuts = cuts[2:]

    field = ':'.join(fields)

    # if field is 1D, returns TH1F. If field is 2D (or more), returns TGraph (scatterplot) according to ROOT documentation
    # THIS IS NOT CORRECT. TH2F is returned for 2D.
    # Workaround for both, because we want the unbinned data: don't write to a specific canvas/figure. According to ROOT documentation, you can access the data like so:
    # 1D: TGraph *graph = (TGraph*)gPad->GetPrimitive("Graph"); // 2D
    # 2D: TH2F   *htemp = (TH2F*)gPad->GetPrimitive("htemp"); // empty, but has axes
    # #worksforme
    # BUT WAIT!!!! NEVER RETURN MORE THAN MILLION EVENTS, SO USELESS FOR LARGE TTREES!!!!
    tree.Draw(field,cuts)
    hnew = r.gPad.GetPrimitive("Graph")

    print 'This graph has',hnew.GetN(),'points.'

    retval = {}
    for field in fields:
        retval[field] = []
        if dim == 1:
            break

    if dim == 1:
        return [i for i in hnew.GetX()] # GetX() is an iter, not a list

    if dim == 2:
        retval[retval.keys()[0]] = [i for i in hnew.GetX()]
        retval[retval.keys()[1]] = [i for i in hnew.GetY()]
        return retval


def scaletree2hist(rootfile,fields,**kwargs):

    dim = 2 #more not handled right now.
    if type(fields) != list:
        dim = 1
        fields = [fields,fields] #this way, we can avoid ROOT making a TH1 and we can get the unbinned data

    xlow,xhigh,nx = kwargs.pop('xbins')
    if 'ybins' in kwargs:
        ylow,yhigh,ny = kwargs.pop('ybins')
        assert len(fields) == 2

    tfile=r.TFile(rootfile)
    tree=tfile.Get("PhaseSpace")

    #if len(kwargs) > 0: #FIXME
    cuts=''
    for key in kwargs: #compile 'cut'-string
        cuts+='&&'
        cuts+=str(key)

        if kwargs[key].startswith('not_'):
            cuts+='!='
            kwargs[key] = kwargs[key][4:]
        else:
            cuts+='=='

        if kwargs[key] == True:
            cuts+='true'
        elif kwargs[key] == False:
            cuts+='false'
        elif type(kwargs[key]) == str:
            cuts+='\"'+kwargs[key]+'\"'
        else:
            cuts+=str(kwargs[key])
    if cuts.startswith('&&'):
        cuts = cuts[2:]

    field = ':'.join(fields)

    retval = {}
    for field in fields:
        retval[field] = []
        if dim == 1:
            break

    if dim == 1:
        tree.Draw(field+'>>eendee('+str(nx)+','+str(xlow)+','+str(xhigh)+')',cuts)
        hnew = r.gPad.GetPrimitive("eendee") #TH1F
    if dim == 2:
        print 'tweedee('+str(nx)+','+str(xlow)+','+str(xhigh)+','+str(ny)+','+str(ylow)+','+str(yhigh)+')'
        tree.Draw(field+'>>tweedee('+str(nx)+','+str(xlow)+','+str(xhigh)+','+str(ny)+','+str(ylow)+','+str(yhigh)+')',cuts)
        hnew = r.gPad.GetPrimitive("tweedee") #TH2F

    if dim == 1:
        xedges = np.linspace(xlow,xhigh,nx+1)
        outdata = np.zeros(hnew.GetNbinsX())
        #because root is a bitch, it is 1-indexed. so thats why theres a shift.
        for i in range(1,hnew.GetNbinsX()+1):
            outdata[i-1] = float(hnew.GetBinContent(i))
        return [xedges,outdata] # GetX() is an iter, not a list

    if dim == 2:
        xedges = np.linspace(xlow,xhigh,nx+1)
        yedges = np.linspace(ylow,yhigh,ny+1)
        outdata = np.zeros((hnew.GetNbinsX(),hnew.GetNbinsY()))
        #because root is a bitch, it is 1-indexed. so thats why theres a shift.
        for xi in range(1,hnew.GetNbinsX()+1):
            for yi in range(1,hnew.GetNbinsY()+1):
                outdata[xi-1,yi-1] = float(hnew.GetBinContent(xi,yi))
        print outdata.shape, hnew.GetNbinsX(), hnew.GetNbinsY()
        return [xedges,yedges,outdata]


def scaletree(rootfile,fields,**kwargs):
    #returns list-mode data, slow!
    # Does not use TTree->Draw because it seems it doesnt always work well.

    if type(fields) != list:
        print "One field",fields,"encoutered, relisting..."
        fields = [fields]

    tfile=r.TFile(rootfile)
    tree=tfile.Get("PhaseSpace")
    print tree.GetEntries(),"entries found in ttree."

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
    import pickle
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


def thist2np_xy_cache(infile,key):
    assert(infile.endswith(".root"))
    npzfile = infile+"."+str(key)+".npz"
    if os.path.isfile(npzfile):
        cached = np.load(npzfile)
        return [cached['x'].tolist(),cached['y'].tolist()]
    else:
        tfile=r.TFile(infile,"READ")
        for item in tfile.GetListOfKeys():
            outname=item.ReadObj().GetName()
            if outname == key:
                outdata_x=[]
                outdata_y=[]
                for i in range(item.ReadObj().GetNbinsX()):
                    outdata_x.append(float(item.ReadObj().GetXaxis().GetBinCenter(i+1)))
                    outdata_y.append(float(item.ReadObj().GetBinContent(i+1)))
                np.savez(npzfile, x=np.array(outdata_x), y=np.array(outdata_y))
                return [outdata_x,outdata_y]
