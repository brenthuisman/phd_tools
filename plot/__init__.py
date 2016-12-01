from texify import *
import numpy as np,matplotlib.pyplot as plt
from math import floor, log10
import scipy.interpolate
import scipy.signal
import scipy.optimize
import plot

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


def ipnl_fit_range_oud(x,y):
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
	tck,u = scipy.interpolate.splprep( [xbp,ybp] ,k=3 )#cubic spline
	xnew,ynew = scipy.interpolate.splev(  np.linspace( 0, 1, 200 ), tck,der = 0)
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


def ipnl_fit_range(x,y):
	y=np.array(y)
	
	#f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
	#ax1.step( x,y, color='moccasin') #bindata
	
	#smooth that shit out.
	#https://en.wikipedia.org/wiki/Smoothing_spline
	y2 = scipy.signal.cspline1d(y,lamb=2)
	y_intpol_f = scipy.interpolate.interp1d(x,y2,kind='cubic') #interpolate function
	x_intpol = np.linspace(x[0],x[-1],1024,endpoint=False)
	y_intpol = y_intpol_f(x_intpol) #interpolate for x_intpol
	y_intpol = y_intpol.clip(min=0) #set any possible negatives to zero
	#ax1.step(x,y2,color='steelblue')
	#ax1.plot(x_intpol,y_intpol,color='indianred')
	
	#take max
	maxind = np.where(y_intpol == y_intpol.max())[0][-1] #so that we find the LAST index where argmax(y)
	#ax1.axvline(x_intpol[maxind],color='green')
	
	#get 25 percentile, and take mean as baseline.
	baseline = y_intpol[y_intpol < np.percentile(y_intpol, 25)].mean()
	#ax1.axhline(baseline,color='green')
	#ax1.axhline(y_intpol.max(),color='green')
	
	falloff = y_intpol[maxind]-baseline
	falloff_index=len(x_intpol)-1
	while y_intpol[falloff_index] < 0.5*falloff+baseline:
		falloff_index-=1
	falloff_pos=x_intpol[falloff_index]
	#ax1.axvline(falloff_pos,color='green')
	
	#f.savefig('recons.pdf', bbox_inches='tight')
	#plot.close('all')
	#quit()
	return falloff_pos


def gueth_fit_range(xs,profile,falloff=.5,window_width=80.,smooth=2):
    # x,y=xs,profile
    xs=np.array(xs)
    profile=np.array(profile)/sum(profile)
    assert(xs.shape==profile.shape)
    
    profile_falloff = profile.mean()*1.3
    index_max = profile.size-1
    assert(profile[index_max]<profile_falloff)
    while profile[index_max]<profile_falloff:
        index_max -= 1

    x_max = xs[index_max]
    x_res = xs[index_max+1]-xs[index_max]

    index_window = int(window_width/x_res)
    xs_window = xs[index_max-index_window:index_max+index_window]
    profile_window = profile[index_max-index_window:index_max+index_window]
    profile_window_spline = scipy.signal.cspline1d(profile_window,lamb=smooth)

    f, ax1 = plot.subplots(nrows=1, ncols=1, sharex=False, sharey=False)
    ax1.plot(xs,profile)
    ax1.plot(xs_window,profile_window,'o-')
    xs_window_interp = np.linspace(xs_window.min(),xs_window.max(),128,endpoint=False)
    profile_window_interp = scipy.signal.cspline1d_eval(profile_window_spline,xs_window_interp,dx=x_res,x0=xs_window_interp.min())
    ax1.plot(xs_window_interp,profile_window_interp,'*-')
    #f.savefig('testplot-falloff.pdf', bbox_inches='tight')
    #plot.close('all')
    #quit()
    
    def eval_profile_window_spline(position):
        #assert(type(position)==float64)
        assert(position>=xs_window.min() and position<=xs_window.max())
        value = scipy.signal.cspline1d_eval(profile_window_spline,[position],dx=x_res,x0=xs_window.min())
        return value[0]

    def maximum_profile_window_spline(position):
        #position = position[0]
        value = eval_profile_window_spline(position) 
        return -value

    x_max_spline = scipy.optimize.fminbound(maximum_profile_window_spline,xs_window.min(),xs_window.max(),disp=False)
    #x_max_spline = x_max_spline[0]
    profile_max_spline = eval_profile_window_spline(x_max_spline)
    
    ax1.axvline(x_max_spline)
    ax1.axhline(profile_max_spline)

    #print "x_max_spline",x_max_spline
    #print "profile_max_spline",profile_max_spline

    def dichotomy_profile_window_spline(bounds,bounds_level,level):
        assert(bounds_level[0]<level and bounds_level[1]>level)

        # if level diff become too small then linear intepolation for final step
        if (bounds_level[1]-bounds_level[0]) < 2e-3:
            alpha = (level-bounds_level[0])/(bounds_level[1]-bounds_level[0])
            assert(alpha>0 and alpha<1)
            return alpha*(bounds[1]-bounds[0])+bounds[0]

        middle = bounds[0]+bounds[1]
        middle /= 2.
        middle_level = eval_profile_window_spline(middle)

        if middle_level > level:
            return dichotomy_profile_window_spline((bounds[0],middle),(bounds_level[0],middle_level),level)
        else:
            return dichotomy_profile_window_spline((middle,bounds[1]),(middle_level,bounds_level[1]),level)

    def find_level_profile_window_spline(level,bounds):
        return dichotomy_profile_window_spline(bounds,(eval_profile_window_spline(bounds[0]),eval_profile_window_spline(bounds[1])),level)

    profile_falloff_spline = profile_max_spline * falloff
    ax1.axhline(profile_falloff_spline)
    x_falloff_spline = find_level_profile_window_spline(profile_falloff_spline,(xs_window.max(),x_max_spline))

    ax1.axvline(x_max,color='indianred')
    ax1.axvline(x_max_spline,color='steelblue')
    ax1.axhline(profile_max_spline)
    ax1.axvline(x_falloff_spline,color='mediumseagreen')
    ax1.axhline(profile_falloff_spline)
    #ax1.xlim(x_max-1.5*window_width,x_max+1.5*window_width)
    f.savefig('testplot-falloff.pdf', bbox_inches='tight')
    plot.close('all')
    quit()

    return x_falloff_spline


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
