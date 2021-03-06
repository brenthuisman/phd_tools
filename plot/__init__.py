from texify import *
import numpy as np,matplotlib.pyplot as plt
from math import floor, log10
import scipy.interpolate
import scipy.signal
import scipy.optimize
import plot
import matplotlib as mpl

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


def plot_errorbands(ax,x,y,ystddev,**kwargs):
	ax.plot(x,y,**kwargs)
	ax.fill_between(x, [i-istd for i,istd in zip(y,ystddev)], [i+istd for i,istd in zip(y,ystddev)],alpha=0.3,interpolate=True,lw=0,**kwargs)
	return ax


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


def chopcentral(ndarr,nbins):
    assert type(nbins) is int
    retval = ndarr[int(len(ndarr)/2.-nbins/2.):int(len(ndarr)/2.+nbins/2.)]
    assert len(retval) == nbins
    return retval


def bincenters_to_binedges(indata):
	indata = np.array(indata)
	outdata = (indata[1:] + indata[:-1]) / 2
	leftedge = 2*indata[0]-outdata[0]
	rightedge = 2*indata[-1]-outdata[-1]
	return np.append(np.append(leftedge,outdata),rightedge)


def addrandomnoise(indata):
	## should be replaced with iba/ipnl funcs
    return [np.random.normal(x, x/500.) if x>0. else x for x in indata]


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


###################### Histogram plotters

def plot2dhist(ax,X,Y,**kwargs):
    
    if len(X) == 0:
        return
    
    if 'log' in kwargs:
        if kwargs.pop('log'):
            kwargs['norm'] = mpl.colors.LogNorm()
    
    if 'xbins' in kwargs: # SHOULD BE BIN EDGES!!!!!
        xbins = kwargs.pop('xbins')
    else:
        xbins = np.linspace(min(X),max(X),40)
        
    if 'ybins' in kwargs: # SHOULD BE BIN EDGES!!!!!
        ybins = kwargs.pop('ybins')
    else:
        ybins = np.linspace(min(Y),max(Y),40)
    
    #default args to pcolormesh
    if 'cmap' not in kwargs:
        kwargs['cmap'] = 'coolwarm'
    
    counts, _, _ = np.histogram2d(X, Y, bins=(xbins, ybins))
    #a = ax.imshow(counts.T)
    a = ax.pcolormesh(xbins, ybins, counts.T, **kwargs)
    #cmap='coolwarm')#,norm=mpl.colors.LogNorm(),vmin=1e0,vmax=1e2)
    #texax(ax)
    ax.text(0.05, 0.95, 'Counts: '+str(len(X)) , ha='left', va='center', transform=ax.transAxes)
    if len(xbins) == len(ybins):
        ax.axis('equal')
    #return a
    return counts

def plot1dhist(ax,data,**kwargs):
    
    if len(data) == 0:
        return
    
    if not 'facecolor' in kwargs:
        kwargs['facecolor'] = 'indianred'
    
    if not 'lw' in kwargs:
        kwargs['lw'] = 0
        
    if not 'bins' in kwargs: # SHOULD BE BIN EDGES!!!!!
        kwargs['bins']=np.linspace(min(data),max(data),40)
        
    if 'count' in kwargs:
        ax.text(0.05, 0.95, 'Counts: '+str(len(data)) , ha='left', va='center', transform=ax.transAxes)
        kwargs.pop('count')
    
    n, _, _ = ax.hist(data,**kwargs)
    return n


def plotbar(ax,data,**kwargs):
    #if you want logarithmic axis, supply log=True to kwargs
    
    from collections import Counter
    
    if type(data) is list:
        cntr = Counter(data)
        labels = cntr.keys()
    if issubclass(type(data), dict):
        cntr = data
        labels = data.keys()
    
    if not 'facecolor' in kwargs:
        kwargs['facecolor'] = 'indianred'
    
    if not 'lw' in kwargs:
        kwargs['lw'] = 0
        
    if 'relabel' in kwargs:
        relabel = kwargs.pop('relabel')
        labels = [relabel[lab] for lab in labels]
        
    if 'bincount' in kwargs:
        postfix = kwargs.pop('bincount')
        for i, v in enumerate(cntr.values()):
            ax.text(i, v + 3, str(int(round(v)))+postfix, color=kwargs['facecolor'], fontweight='bold')
        
    if 'rotation' in kwargs:
        rotation = kwargs.pop('rotation')
    else:
        rotation = 20
    
    ind = np.arange(len(cntr))
    margin = 0.2
    width = (1.-2.*margin)
    xdata = ind - width/2.

    ax.bar(xdata, cntr.values(), width, **kwargs)
    ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(range(len(cntr))))
    ax.set_xticklabels(labels, rotation=rotation, ha='center')
    #texax(ax)
    return cntr


###################### Scientific notation

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

###################### Metric prefixes

def metric_prefix_formatter(x, pos):
    'The two args are the value and tick position'
    if x >= 1e16:
        return '{:1.0f}P'.format(x*1e-16)
    if x >= 1e15:
        return '{:1.1f}P'.format(x*1e-16)
    if x >= 1e13:
        return '{:1.0f}T'.format(x*1e-13)
    if x >= 1e12:
        return '{:1.1f}T'.format(x*1e-12)
    if x >= 1e10:
        return '{:1.0f}G'.format(x*1e-9)
    if x >= 1e9:
        return '{:1.1f}G'.format(x*1e-9)
    if x >= 1e7:
        return '{:1.0f}M'.format(x*1e-6)
    if x >= 1e6:
        return '{:1.1f}M'.format(x*1e-6)
    if x >= 1e4:
        return '{:1.0f}k'.format(x*1e-3)
    if x >= 1e3:
        return '{:1.1f}k'.format(x*1e-3)
    if x >= 1e1:
        return '{:1.0f}'.format(x)
    if x >= 1e0:
        return '{:1.1f}'.format(x)
    if x >= 1e-2:
        return '{:1.0f}m'.format(x*1e3)
    if x >= 1e-3:
        return '{:1.1f}m'.format(x*1e3)
    if x >= 1e-5:
        return '{:1.0f}$\mu$'.format(x*1e6)
    if x >= 1e-6:
        return '{:1.1f}$\mu$'.format(x*1e6)
    if x >= 1e-8:
        return '{:1.0f}n'.format(x*1e9)
    if x >= 1e-9:
        return '{:1.1f}n'.format(x*1e9)
    if x >= 1e-11:
        return '{:1.0f}p'.format(x*1e12)
    if x >= 1e-12:
        return '{:1.1f}p'.format(x*1e12)
    if x >= 1e-14:
        return '{:1.0f}f'.format(x*1e15)
    if x >= 1e-15:
        return '{:1.1f}f'.format(x*1e15)
    return '{:1.0f}'.format(x)

def set_metric_prefix_x(ax):
    from matplotlib.ticker import FuncFormatter
    ax.xaxis.set_major_formatter(FuncFormatter(metric_prefix_formatter))

def set_metric_prefix_y(ax):
    from matplotlib.ticker import FuncFormatter
    ax.yaxis.set_major_formatter(FuncFormatter(metric_prefix_formatter))

###################### Forwards to matplotlib.

def subplots(*args,**kwargs):
    #return plt.subplots(*args,**kwargs)
    f, axes = plt.subplots(*args,**kwargs)
    try:
        for row in axes:
            try:
                for cell in row:
                    #2D
                    texax(cell)
            except TypeError:
                #twas 1D?
                texax(row)
    except TypeError:
        #twas 0D
        texax(axes)
    return (f,axes)

def legend(*args,**kwargs):
	return plt.legend(*args,**kwargs)
	
def close(*args,**kwargs):
	return plt.close(*args,**kwargs)
	
def get_cmap(*args,**kwargs):
	return plt.get_cmap(*args,**kwargs)

def figtext(*args,**kwargs):
	print args[2]
	return plt.figtext(*args,**kwargs)

def colorbar(*args,**kwargs):
	return plt.colorbar(*args,**kwargs)

def plot(*args,**kwargs):
	return plt.plot(*args,**kwargs)

def subplot_tool(*args,**kwargs):
	return plt.subplot_tool(*args,**kwargs)

def errorbar(*args,**kwargs):
	return plt.errorbar(*args,**kwargs)

def show(*args,**kwargs):
	return plt.show(*args,**kwargs)
