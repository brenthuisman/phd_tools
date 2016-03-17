from .plt import *

import matplotlib.pyplot as plt,numpy as np,os,image


def mkpath(*args):
    return os.path.join(os.getcwd(),*args)


def load_tledata(dirs,nprims,masks,pps,yn,vn):
    retval = {}
    for nprim,dirr in zip(nprims,dirs):
        fyn = mkpath(dirr,yn)
        fvn = mkpath(dirr,vn)
        
        # if not os.path.isfile(fyn) or not os.path.isfile(fvn):
        #     fyn = mkpath(dirr,yn[:-4]+'10.mhd')
        #     fvn = mkpath(dirr,vn[:-4]+'10.mhd')

        imagey = image.image(fyn,pps=pps,nprim=nprim,type='yield')
        imagev = image.image(fvn,pps=pps,nprim=nprim,type='var')

        imagey.applymask(*masks)
        imagev.applymask(*masks)
        #imagev.divide(10) #divide variance by number of jobs in batch)
        #print "assuming 10 jobs in batch..."

        retval[nprim] = {}
        retval[nprim]['yield'] = imagey
        retval[nprim]['var'] = imagev
    return retval


def to3d(dataset,crush=[0,0,0,1],outpostfix='3d'):
    for key, value in dataset.iteritems():
        value['yield'].toprojection(outpostfix,crush)
        value['var'].toprojection(outpostfix,crush)


def setrelunc(dataset):
    for key, value in dataset.iteritems():
        value['var'].torelunc(value['yield'])


def seteff(dataset):
    for key, value in dataset.iteritems():
        value['var'].toeff()


def seteffratio(dataset,refdata):
    for key, value in dataset.iteritems():
        value['var'].toeffratio(refdata)


def __setZproj(dataset):
    for key, value in dataset.iteritems():
        value['Z'] = {}
        value['Z']['var'] = value['var'].get1dlist([1,1,0,1])
        value['Z']['yield'] = value['yield'].get1dlist([1,1,0,1])


def __setYproj(dataset):
    for key, value in dataset.iteritems():
        value['Y'] = {}
        value['Y']['var'] = value['var'].get1dlist([1,0,1,1])
        value['Y']['yield'] = value['yield'].get1dlist([1,0,1,1])


def __setEproj(dataset):
    for key, value in dataset.iteritems():
        value['E'] = {}
        value['E']['var'] = value['var'].get1dlist([1,1,1,0])
        value['E']['yield'] = value['yield'].get1dlist([1,1,1,0])


def __setZEproj(dataset):
    __setZproj(dataset)
    __setEproj(dataset)


def __setYEproj(dataset):
    __setYproj(dataset)
    __setEproj(dataset)


def setprojectiondata(dataset,refdata,typ='parodi'):
    if 'batch' not in typ:
        if 'parodi' in typ:
            __setZEproj(dataset)
            __setZEproj({0:refdata})
        if 'head' in typ:
            __setYEproj(dataset)
            __setYEproj({0:refdata})

    # refdata['Z']['var'] = refdata['var'].get1dlist([1,1,0,1])
    # refdata['E']['var'] = refdata['var'].get1dlist([1,1,1,0])

    #compute uncertainty+errorbands, relative uncertainty, reldiff
    def upunc(axis,nprim=None):
        axis['unc'] = [sqrt(item) for item in axis['var']]
        axis['yield-unc'] = [x-u for x,u in zip(axis['yield'],axis['unc'])]
        axis['yield+unc'] = [x+u for x,u in zip(axis['yield'],axis['unc'])]
        axis['relunc'] = [unc/data if data != 0 else unc for unc,data in zip(axis['unc'], axis['yield'])]

        # oud:
        # if nprim is None:
        #     axis['relunc'] = [unc/data if data != 0 else unc for unc,data in zip(axis['unc'], axis['yield'])]
        # else:
        #     axis['relunc'] = [unc/(data*sqrt(nprim)) if data != 0 else unc for unc,data in zip(axis['unc'], axis['yield'])]

    upunc(refdata['E'])
    # upunc(refdata['E'],1e9)
    if 'parodi' in typ:
        upunc(refdata['Z'])
    if 'head' in typ:
        upunc(refdata['Y'])

    for nprims, datadict in dataset.iteritems():
        def updiff(axis,refax):
            axis['reldiff'] = [((tle-an)/an) if an != 0. else tle for tle,an in zip(axis['yield'], refax['yield'])]
            # Goodman's expression (https://en.wikipedia.org/wiki/Propagation_of_uncertainty)
            newvar = [ ((t/a)**2)*( va/a**2 + vt/t**2 )
                    if a != 0. else 0.
                    for t,a,vt,va in zip(axis['yield'],refax['yield'],axis['var'], refax['var'])]

            # axis['reldiff-3sigma'] = [x-3*sqrt(var) for x,var in zip(axis['reldiff'],newvar)]
            # axis['reldiff+3sigma'] = [x+3*sqrt(var) for x,var in zip(axis['reldiff'],newvar)]
            # axis['reldiff-2sigma'] = [x-2*sqrt(var) for x,var in zip(axis['reldiff'],newvar)]
            # axis['reldiff+2sigma'] = [x+2*sqrt(var) for x,var in zip(axis['reldiff'],newvar)]
            axis['reldiff-3sigma'] = [-3*sqrt(var) for x,var in zip(axis['reldiff'],newvar)]
            axis['reldiff+3sigma'] = [3*sqrt(var) for x,var in zip(axis['reldiff'],newvar)]
            axis['reldiff-2sigma'] = [-2*sqrt(var) for x,var in zip(axis['reldiff'],newvar)]
            axis['reldiff+2sigma'] = [2*sqrt(var) for x,var in zip(axis['reldiff'],newvar)]

        #print 'E',len(datadict['E']['yield'])
        #print 'Z',len(datadict['Z']['yield'])

        upunc(datadict['E'])
        # upunc(datadict['E'],nprims)
        updiff(datadict['E'],refdata['E'])
        if 'parodi' in typ:
            upunc(datadict['Z'])
            # upunc(datadict['Z'],nprims)
            updiff(datadict['Z'],refdata['Z'])
        if 'head' in typ:
            upunc(datadict['Y'])
            # upunc(datadict['Y'],nprims)
            updiff(datadict['Y'],refdata['Y'])