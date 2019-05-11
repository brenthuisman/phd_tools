import uproot, glob, os

fname= "ipnl-pre.root"

print("We're in",os.getcwd())
print("Looking for",fname)

filelist = glob.glob("./**/"+fname,recursive=True)

def count_entries_in_phasespace(treefilename):
    assert(treefilename.endswith(".root"))
    f=uproot.open(treefilename)
    return f['PhaseSpace'].numentries



for i,ff in enumerate(filelist):
    print ("Progress",i,"of",len(filelist))
    nb=count_entries_in_phasespace(ff)
    nb=str(nb)
    with open(ff+".txt","w") as f:
        f.writelines(nb)
