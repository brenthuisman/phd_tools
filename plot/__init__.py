#from tle import *
from texify import *

import matplotlib.pyplot as plt,numpy as np
from math import floor, log10, sqrt
from scipy.optimize import curve_fit
from scipy.optimize import fsolve
from scipy.stats import norm

#colors = "rgbmyck"*20
colors = ['#3778bf','#feb308','#7b0323','#7bb274','#a8a495','#825f87']*20
#colors = ['#7fc97f','#beaed4','#fdc086','#ffff99','#386cb0','#f0027f','#bf5b17','#666666']*20
#colors = ['#C40233','#FFD300','#009F6B','#0087BD','#000000']*20


#nice little function to have static vars within a function (which is not in a class)
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


def fill_between_steps(ax, x, y1, y2=0, step_where='pre', **kwargs):
    ''' fill between a step plot and 

    Parameters
    ----------
    ax : Axes
       The axes to draw to

    x : array-like
        Array/vector of index values.

    y1 : array-like or float
        Array/vector of values to be filled under.
    y2 : array-Like or float, optional
        Array/vector or bottom values for filled area. Default is 0.

    step_where : {'pre', 'post', 'mid'}
        where the step happens, same meanings as for `step`

    **kwargs will be passed to the matplotlib fill_between() function.

    Returns
    -------
    ret : PolyCollection
       The added artist

    '''
    if step_where not in {'pre', 'post', 'mid'}:
        raise ValueError("where must be one of {{'pre', 'post', 'mid'}} "
                         "You passed in {wh}".format(wh=step_where))

    # make sure y values are up-converted to arrays 
    if np.isscalar(y1):
        y1 = np.ones_like(x) * y1

    if np.isscalar(y2):
        y2 = np.ones_like(x) * y2

    # temporary array for up-converting the values to step corners
    # 3 x 2N - 1 array 

    vertices = np.vstack((x, y1, y2))

    # this logic is lifted from lines.py
    # this should probably be centralized someplace
    if step_where == 'pre':
        steps = np.zeros((3, 2 * len(x) - 1), np.float)
        steps[0, 0::2], steps[0, 1::2] = vertices[0, :], vertices[0, :-1]
        steps[1:, 0::2], steps[1:, 1:-1:2] = vertices[1:, :], vertices[1:, 1:]

    elif step_where == 'post':
        steps = np.zeros((3, 2 * len(x) - 1), np.float)
        steps[0, ::2], steps[0, 1:-1:2] = vertices[0, :], vertices[0, 1:]
        steps[1:, 0::2], steps[1:, 1::2] = vertices[1:, :], vertices[1:, :-1]

    elif step_where == 'mid':
        steps = np.zeros((3, 2 * len(x)), np.float)
        steps[0, 1:-1:2] = 0.5 * (vertices[0, :-1] + vertices[0, 1:])
        steps[0, 2::2] = 0.5 * (vertices[0, :-1] + vertices[0, 1:])
        steps[0, 0] = vertices[0, 0]
        steps[0, -1] = vertices[0, -1]
        steps[1:, 0::2], steps[1:, 1::2] = vertices[1:, :], vertices[1:, :]
    else:
        raise RuntimeError("should never hit end of if-elif block for validated input")

    # un-pack
    xx, yy1, yy2 = steps

    # now to the plotting part:
    return ax.fill_between(xx, yy1, y2=yy2, **kwargs)


def addrandomnoise(indata):
    return [np.random.normal(x, x/500.) if x>0. else x for x in indata]


def sampledata(indata,scale=0.1):
    #actually, cant that only be done on integer data?
    probs = np.divide(indata,indata.sum())
    print probs
    sampl = np.histogram(np.random.choice(range(len(indata)),1e7,p=probs),bins=len(indata))[0]
    return np.divide(sampl.astype(indata.dtype),sampl.max())*indata.max()*scale


def profile(arr,angle=25,center=[0,0]):
    extract = []
    for i in range(100):
        j = int(center[0] + (center[1] - i) * np.tan(ang * np.pi /180))
        if j<=99 and j>=0:
            extract.append(arr[i,j])
    return extract


def geterrorbands(uncert,sig):
	#returned as percentages
	minus = [(yields-unc) for unc,yields in zip(uncert, sig)]
	plus = [(yields+unc) for unc,yields in zip(uncert, sig)]
	return minus,plus 


def getmuvar(somelist):
	mu = sum(somelist)/float(len(somelist))
	diff = [(mu-x)**2 for x in somelist]
	var = sum(diff)/(len(somelist)+1)
	return (mu,var)


# Define function for string formatting of scientific notation
def sci_notation(num, decimal_digits=1, precision=None, exponent=None):
    """
    Returns a string representation of the scientific
    notation of the given number formatted for use with
    LaTeX or Mathtext, with specified number of significant
    decimal digits and precision (number of decimal digits
    to show). The exponent to be used can also be specified
    explicitly.
    """
    if not exponent:
        exponent = int(floor(log10(abs(num))))
    coeff = round(num / float(10**exponent), decimal_digits)
    if not precision:
        precision = decimal_digits

    return r"${0:.{2}f}\times10^{{{1:d}}}$".format(coeff, exponent, precision)

def sn(num, decimal_digits=2):
    return sci_notation(num, decimal_digits, precision=None, exponent=None)
    #exponent = int(floor(log10(abs(num))))
    #coeff = round(num / float(10**exponent), decimal_digits)
    #return (coeff,exponent)

def snS(num, decimal_digits=1):
    return sci_notation(num, decimal_digits=1, precision=None, exponent=None)[1:-1]

def sn_mag(num):
    exponent = str(int(floor(log10(abs(num)))))
    return r"$10^"+exponent+"$"

#DELETE BELOW THIS LINE
@static_vars(color_index=-1)
def plotwfit(ax1,xlist,ylist,func=None):
    colors = "rgbcmyk"*100
    plotwfit.color_index+=1  
    #set default fit 1/sqrt(x)
    if func is None:
        def func(x,a,b):#var, params
            return a+b/np.sqrt(x)
    parameter, covariance_matrix = curve_fit(func, xlist, ylist)

    threshold = fsolve(lambda x: func(x,*parameter)-.02, 1e2) #initial guess at 1e3

    x = np.linspace(min(xlist), max([threshold,xlist[-1]]), 1e5)
    y = func(x, *parameter)

    ax1.scatter(xlist, [100*i for i in ylist], marker='x', s=100,color=colors[plotwfit.color_index])
    ax1.plot(x, 100*y, 'b-', label='Fit: '+sn(parameter[0])+'+\n'+sn(parameter[1])+'/$\sqrt{runtime}$',color=colors[plotwfit.color_index])
    ax1.autoscale(axis='x',tight=True)
    ax1.autoscale(axis='y',tight=True)
    ax1.axhline(100*0.02, color='#666666', ls='--')
    ax1.axvline(threshold, color='#999999', ls='--')
    
    plot.texify.fixax(ax1)

    print "Crossing 2pc threshold at %.2e"%threshold
    return threshold


@static_vars(color_index=-1)
def ploteffhist(ax1,data):
    colors = "rgbcmyk"*100
    plotwfit.color_index+=1  
    data = data[~np.isnan(data)].flatten()
    # label = "Min: %.2e, Median: %.2e, Max: %.2e"%(np.nanmin(data),np.median(data),np.nanmax(data))
    label = "Min: "+sn(np.nanmin(data))+"\nMedian: "+sn(np.median(data))+"\nMax: "+sn(np.nanmax(data))
    ax1.hist(data, bins = np.logspace(np.log10(np.nanmin(data)),np.log10(np.nanmax(data))) ,label=label,color=colors[plotwfit.color_index])
    # ax1.semilogy()
    ax1.semilogx()
    # ax1.set_xlabel('')
    # ax1.set_ylabel('')
    # ax1.set_title('')
    # ax1.title.set_fontsize(6)
    plt.text(0.05, 0.9,label, ha='left', va='center', transform=ax1.transAxes, fontsize=6)
    ax1.axvline(np.nanmin(data), color='#999999', ls='--')
    ax1.axvline(np.nanmax(data), color='#999999', ls='--')
    plot.texify.fixax(ax1)
    return label
