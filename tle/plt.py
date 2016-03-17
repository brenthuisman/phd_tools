import plot

import matplotlib.pyplot as plt,numpy as np,matplotlib as mpl
from math import floor, log10, sqrt
from scipy.optimize import curve_fit
from scipy.optimize import fsolve

#nice little function to have static vars within a function (which is not in a class)
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


def __withinsigma(value):
    # UPDATE FEB 2016: reldiff-+Xsigma is now 0+-Xsigma. We assume no bias, and check if the mean is indeed without.

    #Based on the relative difference data, give number of bins not in range and wether or not this is expected or not.
    print 'reldiff: likelyhood report'
    #bias = sqrt( sum( [x**2 for x in value['reldiff']] ) / len(value['reldiff']) )
    bias = sum( value['reldiff'] ) / len(value['reldiff'])
    #print 'RMS (average relative difference):',bias
    print 'Av. Rel. Bias:',bias

    #print value['reldiff-2sigma'],value['reldiff+2sigma']
    
    #we test the range inclusively, because rangecutoffs give values of 0.0, but we musnt count that as out of range.
    rule95=['inrange' if low <= rd <= high else 'outrange' for low,rd,high in zip(value['reldiff-2sigma'],value['reldiff'],value['reldiff+2sigma'])]
    print 'rule95. Bins outrange:',rule95.count('outrange'), '. Expected:', len(value['yield'])*(1-0.9545)

    rule99=['inrange' if low <= rd <= high else 'outrange' for low,rd,high in zip(value['reldiff-3sigma'],value['reldiff'],value['reldiff+3sigma'])]
    print 'rule99. Bins outrange:',rule99.count('outrange'), '. Expected:', len(value['yield'])*(1-0.9973)

    print ' '
    return 'Av. Rel. Bias: '+plot.sci_notation(bias,1)


@static_vars(color_index=-1)
def get_reluncconv(ax1,xlist,ylist,func=None):
    colors = 'rk'
    labels = ['vpgTLE','Analog']
    get_reluncconv.color_index+=1  
    #set default fit 1/sqrt(x)
    if func is None:
        def func(x,b):#var, params
            return b/np.sqrt(x)
            # return a+b/np.sqrt(x)
    parameter, covariance_matrix = curve_fit(func, xlist, ylist)

    threshold = fsolve(lambda x: func(x,*parameter)-.02, 1e1) #initial guess at 1e3

    x = np.linspace(min(xlist), max([threshold,max(xlist)]), 1e5)
    y = func(x, *parameter)

    #'Fit: '+plot.sn(parameter[0])+'+\n'+plot.sn(parameter[1])+'/$\sqrt{runtime}$'
    fitlabel = labels[get_reluncconv.color_index]+', Fit:\n'+r'$\frac{%s}{\sqrt{t}}$'%plot.snS(parameter[0])

    ax1.scatter(xlist, [100*i for i in ylist],marker='x',s=100,color=colors[get_reluncconv.color_index])
    ax1.plot(x, 100*y, 'b-',label=fitlabel,color=colors[get_reluncconv.color_index])
    ax1.autoscale(axis='x',tight=True)
    ax1.autoscale(axis='y',tight=True)
    ax1.axhline(100*0.02, color='#666666', ls='--')
    ax1.axvline(threshold, color='#999999', ls='--')
    
    plot.texax(ax1)

    print "Crossing 2pc threshold at %.2e"%threshold
    return threshold


@static_vars(color_index=-1)
def get_effhist_oud(ax1,image,name=None):
    colors = plot.colors
    get_effhist.color_index+=1  
    data = image.imdata[~np.isnan(image.imdata)].flatten()
    # data=data/np.nanmax(data)
    # with np.errstate(divide='ignore', invalid='ignore'):
    #     data = np.true_divide(data,np.nanmax(data))
    #data = np.nonzero(data)]
    #print image.nprim,np.nanmin(data),np.nanmax(data)
    if np.nanmin(data) == 0:
        label=plot.sn_mag(image.nprim)+" primaries\nMin: "+str(0)+"\nMax: "+plot.sn(np.nanmax(data))
        y, x, _=ax1.hist(data, bins = np.logspace(1,np.log10(np.nanmax(data))) ,label=label,color=colors[get_effhist.color_index],histtype='step', lw=1)
    else:
        label=plot.sn_mag(image.nprim)+" primaries\nMin: "+plot.sn(np.nanmin(data))+"\nMax: "+plot.sn(np.nanmax(data))
        y, x, _=ax1.hist(data, bins = np.logspace(np.log10(np.nanmin(data)),np.log10(np.nanmax(data))) ,label=label,color=colors[get_effhist.color_index],histtype='step', lw=1)
    print y.max()
    # label=str(image.nprim)+" primaries\nMin: "+str(np.nanmin(data))+"\nMax: "+str(np.nanmax(data))
    # ax1.hist(data, bins = np.linspace(np.nanmin(data),np.nanmax(data)) ,label=label,color=colors[get_effhist.color_index],histtype='step', lw=1)
    ax1.semilogx()

    plot.texax(ax1)
    # print 'Median of efficiency:',np.median(data)
    # print 'Mean of efficiency:',np.mean(data)
    return [np.nanmin(data),np.median(data),np.nanmax(data),np.mean(data)]


@static_vars(color_index=-1)
def get_effhist(ax1,image,name=None):
    colors = plot.colors
    get_effhist.color_index+=1  
    data = image.imdata[~np.isnan(image.imdata)].flatten()

    if np.nanmin(data) == 0:
        binn = np.logspace(1,np.log10(np.nanmax(data)))
        label = plot.sn_mag(image.nprim)+" primaries\nMin: "+str(0)+"\nMax: "+plot.sn(np.nanmax(data))
    else:
        binn = np.logspace(np.log10(np.nanmin(data)),np.log10(np.nanmax(data)))
        label = plot.sn_mag(image.nprim)+" primaries\nMin: "+plot.sn(np.nanmin(data))+"\nMax: "+plot.sn(np.nanmax(data))

    hist,bins = np.histogram(data, bins=binn)
    center = (bins[:-1] + bins[1:]) / 2
    bins=center
    # hist[0] = 0
    # hist[-1] = 0
    
    if name is None:
        ax1.plot(bins,hist/float(hist.max()),label=label,color=colors[get_effhist.color_index],drawstyle='steps')
    else:
        ax1.plot(bins,hist/float(hist.max()),label=name+'\nMedian gain: '+plot.sn(np.median(data)),color=colors[get_effhist.color_index],drawstyle='steps')
    
    ax1.semilogx()
    plot.texax(ax1)
    # print 'Median of efficiency:',np.median(data)
    # print 'Mean of efficiency:',np.mean(data)
    return [np.nanmin(data),np.median(data),np.nanmax(data),np.mean(data)]


def get_yield(ax1,dataset,refdata,ax,typ='parodi'):
    colors = plot.colors
    color_index=0
    
    #asume voxels are 2mm
    if 'Z' in ax and 'parodi' in typ:
        x_axis = np.linspace(0,222,111)
    if 'Y' in ax and 'head' in typ:
        x_axis = np.linspace(0,170,85)
    if 'E' in ax:
        x_axis = np.linspace(0,10,250)

    for key, valuee in iter(sorted(dataset.iteritems())):
        # if TLE
        value = valuee[ax]
        # print ax, len(value['yield'])
        ax1.step(x_axis,value['yield'], label=plot.sn_mag(key)+' primaries', color=colors[color_index], lw=0.5)
        plot.fill_between_steps(ax1, x_axis, value['yield-unc'], value['yield+unc'], alpha=0.5, color=colors[color_index], lw=0.5)
        color_index+=1

    #analog reference
    refdata = refdata[ax]
    ax1.step(x_axis,refdata['yield'], label='Reference', color='k', lw=0.5)
    plot.fill_between_steps(ax1, x_axis, refdata['yield-unc'], refdata['yield+unc'], alpha=0.5, color='k', lw=0.5)

    ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax1.autoscale(axis='x',tight=True)

    # #PG falloff line parodi
    spectcutoff = [1,8]
    if ax == 'E':
        ax1.set_xlim(spectcutoff)
    
    plot.texax(ax1)


def get_reldiff(ax1,dataset,ax,typ='parodi'):
    colors = plot.colors
    color_index=0
    
    #asume voxels are 2mm
    if 'Z' in ax and 'parodi' in typ:
        x_axis = np.linspace(0,222,111)
    if 'Y' in ax and 'head' in typ:
        x_axis = np.linspace(0,170,85)
    if 'E' in ax:
        x_axis = np.linspace(0,10,250)

    for key, valuee in iter(sorted(dataset.iteritems())):
        value = valuee[ax]

        ax1.step(x_axis,
            [x*100. for x in value['reldiff']],
            label=plot.sn_mag(key) +' primaries', color=colors[color_index], lw=0.5)
        
        print key, __withinsigma(value)
        
        plot.fill_between_steps(ax1, x_axis,
                    [x*100. for x in value['reldiff-2sigma']],
                    [x*100. for x in value['reldiff+2sigma']],
                    alpha=0.25, color=colors[color_index], lw=0.01)
            
        color_index+=1
    
    ax1.autoscale(axis='x',tight=True)
    #ax1.set_ylim([-4,4])
    
    # #PG falloff line parodi
    spectcutoff = [1,8]
    if ax == 'E':
        ax1.set_xlim(spectcutoff)
    # if ax == 'E':
    #     ax1.axvline(spectcutoff[0], color='#999999', ls='--')
    #     ax1.axvline(spectcutoff[1], color='#999999', ls='--')
    
    plot.texax(ax1)


def get_relunc(ax1,dataset,refdata,ax,typ='parodi'):
    colors = plot.colors
    color_index=0
    
    #asume voxels are 2mm
    if 'Z' in ax and 'parodi' in typ:
        x_axis = np.linspace(0,222,111)
    if 'Y' in ax and 'head' in typ:
        x_axis = np.linspace(0,170,85)
    if 'E' in ax:
        x_axis = np.linspace(0,10,250)

    for key, valuee in iter(sorted(dataset.iteritems())):
        value = valuee[ax]
        try:
            ax1.step(x_axis,[x*100. for x in value['relunc']], label=plot.sn_mag(key)+' primaries', color=colors[color_index])
        except TypeError:
            ax1.step(x_axis,[x*100. for x in value['relunc']], label=key, color=colors[color_index])
        
        color_index+=1

    if refdata is not None:
        refdata = refdata[ax]
        ax1.step(x_axis,[x*100. for x in refdata['relunc']], label='Reference', color='k')

    ax1.semilogy()
    ax1.autoscale(axis='x',tight=True)
    #ax1.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.0f%%'))
    
    #PG falloff line
    spectcutoff = [1,8]
    if ax == 'E':
        ax1.set_xlim(spectcutoff)
    # if ax == 'E':
    #     ax1.axvline(spectcutoff[0], color='#999999', ls='--')
    #     ax1.axvline(spectcutoff[1], color='#999999', ls='--')

    plot.texax(ax1)


def get_unc(ax1,dataset,refdata,ax,typ='parodi'):
    colors = plot.colors
    color_index=0
    
    #asume voxels are 2mm
    if 'Z' in ax and 'parodi' in typ:
        x_axis = np.linspace(0,222,111)
    if 'Y' in ax and 'head' in typ:
        x_axis = np.linspace(0,170,85)
    if 'E' in ax:
        x_axis = np.linspace(0,10,250)

    for key, valuee in iter(sorted(dataset.iteritems())):
        value = valuee[ax]
        ax1.step(x_axis,[x*100. for x in value['unc']], label=plot.sn_mag(key)+' primaries', color=colors[color_index])
        color_index+=1

    refdata = refdata[ax]
    ax1.step(x_axis,[x*100. for x in refdata['unc']], label='Reference', color='k')

    ax1.semilogy()
    ax1.autoscale(axis='x',tight=True)
    #ax1.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.0f%%'))
    
    #PG falloff line
    spectcutoff = [1,8]
    if ax == 'E':
        ax1.set_xlim(spectcutoff)
    # if ax == 'E':
    #     ax1.axvline(spectcutoff[0], color='#999999', ls='--')
    #     ax1.axvline(spectcutoff[1], color='#999999', ls='--')

    plot.texax(ax1)
