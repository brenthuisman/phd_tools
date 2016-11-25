from texify import *
import numpy as np,matplotlib.pyplot as plt
from math import floor, log10
from scipy import interpolate

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
	## should be replaced with iba/ipnl funcs
    return [np.random.normal(x, x/500.) if x>0. else x for x in indata]


def ipnlnoise(data,nprim):
	#IPNL: \cite{Pinto2014a}: 1000+-100 per 4e9 prims per 8mm bin
	#per prot: 2.5e-7 +- 0.25e-7 (twice better than IBA, but twice bigger bin)
	mu = 2.5e-7*nprim
	sigma = 0.25e-7*nprim
	retval = []
	for i in data:
		retval.append(i + np.random.poisson(np.random.normal(mu,sigma)))
	return retval


def onlyipnlnoise(data,nprim):
	#IPNL: \cite{Pinto2014a}: 1000+-100 per 4e9 prims per 8mm bin
	#per prot: 2.5e-7 +- 0.25e-7 (twice better than IBA, but twice bigger bin)
	mu = 2.5e-7*nprim
	sigma = 0.25e-7*nprim
	retval = []
	for i in data:
		retval.append(np.random.poisson(np.random.normal(mu,sigma)))
	return retval


def ibanoise(data,nprim):
	#IBA: \cite{Perali2014}: 5e-7 +- 0.5e-7 per prot per 4mm bin
	mu = 5e-7*nprim
	sigma = 0.5e-7*nprim
	retval = []
	for i in data:
		retval.append(i + np.random.poisson(np.random.normal(mu,sigma)))
	return retval


def onlyibanoise(data,nprim):
	#IBA: \cite{Perali2014}: 5e-7 +- 0.5e-7 per prot per 4mm bin
	mu = 5e-7*nprim
	sigma = 0.5e-7*nprim
	retval = []
	for i in data:
		retval.append(np.random.poisson(np.random.normal(mu,sigma)))
	return retval


def sampledata(indata,scale=0.1):
    #actually, cant that only be done on integer data?
    probs = np.divide(indata,indata.sum())
    print probs
    sampl = np.histogram(np.random.choice(range(len(indata)),1e7,p=probs),bins=len(indata))[0]
    return np.divide(sampl.astype(indata.dtype),sampl.max())*indata.max()*scale


def geterrorbands(uncert,sig):
	#returned as percentages
	minus = [(yields-unc) for unc,yields in zip(uncert, sig)]
	plus = [(yields+unc) for unc,yields in zip(uncert, sig)]
	return minus,plus 


def getloghist(data,nrbin=50):
	binn = np.logspace(np.log10(np.nanmin(data)),np.log10(np.nanmax(data)),num=nrbin)
	hist,bins = np.histogram(data, bins=binn)
	centers = (bins[:-1] + bins[1:]) / 2
	return centers,hist


def ipnl_fit_range(x,y):
	#take max
	y=np.array(y)
	#maxind = np.argmax(y)
	maxind = np.where(y == y.max())[0][-1] #so that we find the LAST index where argmax(y)
	#print maxind
	y = y.tolist()
	#go towards end and find 50% thrshold
	nextind=maxind+1
	while y[nextind] > 0.5*y[maxind]:
		nextind+=1
	# go x bins left and right and fit within
	hm_left=nextind-5
	hm_right=nextind+5
	xbp=x[hm_left:hm_right]
	ybp=y[hm_left:hm_right]
	#print maxind,xbp,ybp,y
	tck,u = interpolate.splprep( [xbp,ybp] ,k=3 )#cubic spline
	xnew,ynew = interpolate.splev(  np.linspace( 0, 1, 200 ), tck,der = 0)
	#take mean value in tail-window as minimum
	floor=np.mean(y[hm_right:])
	#take max val in BP window as max
	top=np.max(ybp)
	falloffval_50pc=(top-floor)*.5
	nextind=len(ynew)-1
	while ynew[nextind] < falloffval_50pc:
		nextind-=1
	falloffpos = xnew[nextind]
	#ax1.plot( xbp,ybp,'' , xnew ,ynew )
	return falloffpos,[xbp,ybp,'',xnew,ynew]


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

###################### Forwards to matplotlib.

def subplots(*args,**kwargs):
	return plt.subplots(*args,**kwargs)
	
def close(*args,**kwargs):
	return plt.close(*args,**kwargs)
