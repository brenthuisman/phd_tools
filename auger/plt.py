import numpy as np,plot,scipy
from numpy import sqrt

FONTSIZE = 12
Fontsize = 10

def plotrange(ax1,ct):
    x = ct['ct']['x']
    y = ct['ct']['av']
    um = ct['ct']['uncm']
    up = ct['ct']['uncp']
    ymax = max(y)

    if len(um)>0:
        ymax = max(ymax,max(up))
        plot.fill_between_steps(ax1, x, um, up, alpha=0.2, color='steelblue', lw=0.5,clip_on=False) #doesnt support where=mid
    else:
        ax1.step(x, y, label=ct['name']+'ct', color='steelblue', lw=1, where='mid',clip_on=False)
        #ax1.step(x, y, label=ct['name']+'ct', color='steelblue', lw=1, where='mid')

    x = ct['rpct']['x']
    y = ct['rpct']['av']
    um = ct['rpct']['uncm']
    up = ct['rpct']['uncp']
    ymax = max(ymax,max(y))

    if len(um)>0:
        ymax = max(ymax,max(up))
        plot.fill_between_steps(ax1, x, um, up, alpha=0.2, color='indianred', lw=0.5,clip_on=False)
    else:
        ax1.step(x, y, label=ct['name']+'rpct', color='indianred', lw=1, where='mid',clip_on=False)
        #ax1.step(x, y, label=ct['name']+'rpct', color='indianred', lw=1, where='mid')
    ax1.set_xlabel('Depth [mm]', fontsize=FONTSIZE)
    ax1.set_ylabel('PG detected [counts]', fontsize=FONTSIZE)
    ax1.set_ylim(bottom=0,top=ymax)
    #ax1.set_title('PG detection for '+plot.sn_mag(ct['nprim'])+'primaries', fontsize=FONTSIZE)
    plot.texax(ax1)


def plot_all_ranges(ax1,ct):
    yield_ct=0
    for i in range(len(ct['ct']['data'])):
        yield_ct+=sum(ct['ct']['data'][i])
        x,y,fo=ct['ct']['x'],ct['ct']['data'][i],ct['ct']['falloff'][i]
        ax1.step(x, y, label=ct['name']+'ct', color='steelblue', lw=1, where='mid',clip_on=False, alpha=0.5)
        ax1.axvline(fo, color='steelblue', ls='-',lw=1, alpha=0.5)
    yield_ct = yield_ct/len(ct['ct']['data']) #per realisatie

    ax1.set_xlabel('Depth [mm]', fontsize=FONTSIZE)
    ax1.set_ylabel('PG detected [counts]', fontsize=FONTSIZE)
    ax1.set_title(plot.sn(ct['nprim'],0)+' primaries', fontsize=Fontsize)
    plot.texax(ax1)

    yield_rpct=0
    for i in range(len(ct['rpct']['data'])):
        yield_rpct+=sum(ct['rpct']['data'][i])
        x,y,fo=ct['rpct']['x'],ct['rpct']['data'][i],ct['rpct']['falloff'][i]
        ax1.step(x, y, label=ct['name']+'ct', color='indianred', lw=1, where='mid',clip_on=False, alpha=0.5)
        ax1.axvline(fo, color='indianred', ls='-',lw=1, alpha=0.5)
    yield_rpct = yield_rpct/len(ct['rpct']['data']) #per realisatie

    if str(ct['nprim'])[1] == '0':
        ax1.set_title('PG detection for '+plot.sn_mag(ct['nprim'])+' primaries', fontsize=Fontsize)
    else:
        ax1.set_title('PG detection for '+plot.sn(ct['nprim'])+' primaries', fontsize=Fontsize)
    ax1.set_ylim(bottom=0)

    ct_labelextra = ''
    rpct_labelextra = ''
    if True:
        ct_labelextra += 'CT DE: '+plot.sn(yield_ct/ct['nprim']) #yield per prot
        rpct_labelextra += 'RPCT DE: '+plot.sn(yield_rpct/ct['nprim'])

    ax1.text(0.05, 0.95, ct_labelextra , ha='left', va='center', fontsize=Fontsize, transform=ax1.transAxes)
    ax1.text(0.05, 0.8, rpct_labelextra , ha='left', va='center', fontsize=Fontsize, transform=ax1.transAxes)
    plot.texax(ax1)


def plot_all_ranges_CTONLY(ax1,ct):
    yield_ct=0
    for i in range(len(ct['ct']['data'])):
        yield_ct+=sum(ct['ct']['data'][i])
        x,y,fo=ct['ct']['x'],ct['ct']['data'][i],ct['ct']['falloff'][i]
        ax1.step(x, y, label=ct['name']+'ct', color='steelblue', lw=1, where='mid',clip_on=False, alpha=0.5)
        ax1.axvline(fo, color='steelblue', ls='-',lw=1, alpha=0.5)
    yield_ct = yield_ct/len(ct['ct']['data']) #per realisatie

    ax1.set_xlabel('Depth [mm]', fontsize=FONTSIZE)
    ax1.set_ylabel('PG detected [counts]', fontsize=FONTSIZE)
    ax1.set_title(plot.sn(ct['nprim'],0)+' primaries', fontsize=Fontsize)
    plot.texax(ax1)

    if str(ct['nprim'])[1] == '0':
        ax1.set_title('PG detection for '+plot.sn_mag(ct['nprim'])+' primaries', fontsize=Fontsize)
    else:
        ax1.set_title('PG detection for '+plot.sn(ct['nprim'])+' primaries', fontsize=Fontsize)
    ax1.set_ylim(bottom=0)

    ct_labelextra = ''
    if True:
        ct_labelextra += 'DE: '+plot.sn(yield_ct/ct['nprim']) #yield per prot

    ax1.text(0.05, 0.95, ct_labelextra , ha='left', va='center', fontsize=Fontsize, transform=ax1.transAxes)
    plot.texax(ax1)


def plot_all_ranges_2(ax1,ct,firstcolor='steelblue',secondcolor='indianred'):
    yield_ct=0
    for i in range(len(ct['ct']['data'])):
        yield_ct+=sum(ct['ct']['data'][i])
        x,y,fo=ct['ct']['x'],ct['ct']['data'][i],ct['ct']['falloff'][i]
        ax1.step(x, y, label=ct['name']+'ct', color=firstcolor, lw=1, where='mid',clip_on=True, alpha=0.5)
        ax1.axvline(fo, color=firstcolor, ls='-',lw=1, alpha=0.5)
    yield_ct = yield_ct/len(ct['ct']['data']) #per realisatie

    if secondcolor is not None:
        yield_rpct=0
        for i in range(len(ct['rpct']['data'])):
            yield_rpct+=sum(ct['rpct']['data'][i])
            x,y,fo=ct['rpct']['x'],ct['rpct']['data'][i],ct['rpct']['falloff'][i]
            ax1.step(x, y, label=ct['name']+'ct', color=secondcolor, lw=1, where='mid',alpha=0.5, clip_on=True)
            ax1.axvline(fo, color=secondcolor, ls='-',lw=1, alpha=0.5)
        yield_rpct = yield_rpct/len(ct['rpct']['data']) #per realisatie

        plot.texax(ax1)

        return (yield_ct+yield_rpct)/(2.*ct['nprim'])
    return yield_ct/ct['nprim']

def plot_single_range(ax1,ct):
    for i in range(len(ct['ct']['data'])):
        x,y,fo=ct['ct']['x'],ct['ct']['data'][i],ct['ct']['falloff'][i]
        ax1.step(x, y, label=ct['name']+'ct', color='steelblue', lw=1, where='mid',clip_on=False, alpha=0.5)
        ax1.axvline(fo, color='steelblue', ls='-',lw=1, alpha=0.5)
        break

    ax1.set_xlabel('Depth [mm]', fontsize=FONTSIZE)
    ax1.set_ylabel('PG detected [counts]', fontsize=FONTSIZE)
    ax1.set_title(plot.sn(ct['nprim'],0)+' primaries', fontsize=FONTSIZE)
    plot.texax(ax1)

    for i in range(len(ct['rpct']['data'])):
        x,y,fo=ct['rpct']['x'],ct['rpct']['data'][i],ct['rpct']['falloff'][i]
        ax1.step(x, y, label=ct['name']+'ct', color='indianred', lw=1, where='mid',clip_on=False, alpha=0.5)
        ax1.axvline(fo, color='indianred', ls='-',lw=1, alpha=0.5)
        break

    ax1.set_title('PG detection for '+plot.sn_mag(ct['nprim'])+'primaries', fontsize=FONTSIZE)
    ax1.set_ylim(bottom=0)
    plot.texax(ax1)


def plotfodiffdist(ax1,ct,zs,emisfops=None,labels=["$10^9$","$10^8$","$10^7$","$10^6$"],axlabel='Primaries [nr]',center=0):
    ax1.set_ylabel(axlabel, fontsize=FONTSIZE)

    (mu, sigma) = scipy.stats.norm.fit(ct['fodiff'])

    if not emisfops == None:
        fopshifts=[]
        for fopset in emisfops:
            fopshifts.append( fopset[-1]-fopset[0] )
        ax1.set_xlim3d(np.mean(fopshifts)-20,np.mean(fopshifts)+20)
    elif zs==0:
        #ax1.set_xlim3d(mu-20,mu+20)
        ax1.set_xlim3d(int(center-20),int(center+20))

    y,bins=np.histogram(ct['fodiff'], np.arange(int(center-20),int(center+20),1))
    #print mu, sigma
    bincenters = 0.5*(bins[1:]+bins[:-1])
    c = ['grey']*len(y)
    ax1.bar(bincenters,y, color=c,lw=0.2, zs=zs, zdir='y',label=labels[zs]+' primaries')

    ax1.set_xlabel('Detected Shifts [mm]', fontsize=FONTSIZE)
    ax1.set_zlabel('[counts]', fontsize=FONTSIZE)
    ax1.locator_params(axis='y',nbins=len(labels)-1)
    ax1.set_yticklabels(labels, va='baseline', ha='left',fontsize=Fontsize)
    #ax1.tick_params(axis='y',which='minor',bottom='off')
    #zs/10.

    label_extra=''
    if emisfops is not None and len(emisfops) == len(labels):
        label_extra=', $Shift_{em}$ = '+str(emisfops[zs][1]-emisfops[zs][0])
    else: #prob of RPCT FOP is within mu_{FOP,CT}\pm2sigma_{FOP,CT}
        #label_extra=', $P_{cr}$ = '+str(1-scipy.stats.norm(mu, sigma).cdf(mu-1))[:4] #old P_cr
        label_extra+='$\pm$'+str(sigma/sqrt(2*(len(ct['fodiff'])-1)))[:4]
        label_extra+=', P$_\Delta$ = '+str((1-scipy.stats.norm(ct['rpct']['fopmu'], ct['rpct']['fopsigma']).cdf(ct['ct']['fopmu']+2*ct['ct']['fopsigma']))*100.)[:3].rstrip('.')+'\%' #assume always forward shifted!!!
    plot.figtext(0.01, 0.95-zs/20.,labels[zs]+": $\mu_\Delta$ = "+str(mu)[:4]+", $\sigma_\Delta$ = "+str(sigma)[:4]+label_extra, ha='left', va='center', fontsize=Fontsize, transform=ax1.transAxes)
    #plot.figtext(0.05, 0.9-zs/40.,labels[zs]+": $\mu_{shift}$ = "+str(mu)[:4]+", $\sigma_{shift}$ = "+str(sigma)[:4]+label_extra, ha='left', va='center', fontsize=Fontsize, transform=ax1.transAxes)


def plotfodist(ax1,ct,zs,emisfops=None,labels=["$10^9$","$10^8$","$10^7$","$10^6$"],axlabel='Primaries [nr]',center=0):
    ax1.set_ylabel(axlabel, fontsize=FONTSIZE)

    fo_ct=[]
    fo_rpct=[]

    for i in range(len(ct['ct']['data'])):
        x,y,fo=ct['ct']['x'],ct['ct']['data'][i],ct['ct']['falloff'][i]
        fo_ct.append(fo)
    (ctmu, ctsigma) = scipy.stats.norm.fit(fo_ct)

    for i in range(len(ct['rpct']['data'])):
        x,y,fo=ct['rpct']['x'],ct['rpct']['data'][i],ct['rpct']['falloff'][i]
        fo_rpct.append(fo)
    (rpctmu, rpctsigma) = scipy.stats.norm.fit(fo_rpct)

    #if zs==0:
        #print (ctmu+rpctmu)
        #print ct['ct']['fopmu'], ct['rpct']['fopmu']
        #centr = (ctmu+rpctmu)/2.
        #ax1.set_xlim3d(centr-20,centr+20)
    ax1.set_xlim3d(int(center-20),int(center+20))

    y,bins=np.histogram(fo_ct, np.arange(int(center-20),int(center+20),1))
    bincenters = 0.5*(bins[1:]+bins[:-1])
    c = ['steelblue']*len(y)
    ax1.bar(bincenters,y, color=c,lw=0.2, zs=zs, zdir='y', alpha=0.5, label=labels[zs]+' primaries')

    y,bins=np.histogram(fo_rpct, np.arange(int(center-20),int(center+20),1))
    bincenters = 0.5*(bins[1:]+bins[:-1])
    c = ['indianred']*len(y)
    ax1.bar(bincenters,y, color=c,lw=0.2, zs=zs, zdir='y', alpha=0.5, label=labels[zs]+' primaries')

    ax1.set_xlabel('Falloff Position [mm]', fontsize=FONTSIZE)
    ax1.set_zlabel('[counts]', fontsize=FONTSIZE)
    ax1.locator_params(axis='y',nbins=len(labels))
    ax1.set_yticklabels(labels, va='baseline', ha='left',fontsize=Fontsize)
    ax1.set_ylabel('Primaries [nr]', fontsize=FONTSIZE)

    labelCT_extra=''
    labelRPCT_extra=''
    if emisfops is not None and len(emisfops) == len(labels):
        labelCT_extra+=', $FOP_{em}$ = '+str(emisfops[zs][0])
        labelRPCT_extra+=', $FOP_{em}$ = '+str(emisfops[zs][1])
    else:
        labelCT_extra+='$\pm$'+str(ctsigma/sqrt(2*(len(fo_ct)-1)))[:4]
        labelRPCT_extra+='$\pm$'+str(rpctsigma/sqrt(2*(len(fo_rpct)-1)))[:4]
    #elif len(emisfops) == 1:
        #labelCT_extra=', $FOP_{em}$ = '+str(emisfops[0][0])
        #labelRPCT_extra=', $FOP_{em}$ = '+str(emisfops[0][1])

    plot.figtext(0.01, 0.95-zs/10.,labels[zs]+ct['ct']['label']+": $\mu_{FOP}$ = "+str(ctmu)[:4]+", $\sigma_{FOP}$ = "+str(ctsigma)[:4]+labelCT_extra, ha='left', va='center', fontsize=Fontsize, transform=ax1.transAxes)
    plot.figtext(0.01, 0.90-zs/10.,labels[zs]+ct['rpct']['label']+": $\mu_{FOP}$ = "+str(rpctmu)[:4]+", $\sigma_{FOP}$ = "+str(rpctsigma)[:4]+labelRPCT_extra, ha='left', va='center', fontsize=Fontsize, transform=ax1.transAxes)

def plotfodist_CTONLY(ax1,ct,zs,emisfops=None,labels=["$10^9$","$10^8$","$10^7$","$10^6$"],axlabel='Primaries [nr]',center=0):
    ax1.set_ylabel(axlabel, fontsize=FONTSIZE)

    fo_ct=[]

    for i in range(len(ct['ct']['data'])):
        x,y,fo=ct['ct']['x'],ct['ct']['data'][i],ct['ct']['falloff'][i]
        fo_ct.append(fo)
    (ctmu, ctsigma) = scipy.stats.norm.fit(fo_ct)

    ax1.set_xlim3d(int(center-20),int(center+20))

    y,bins=np.histogram(fo_ct, np.arange(int(center-20),int(center+20),1))
    bincenters = 0.5*(bins[1:]+bins[:-1])
    c = ['steelblue']*len(y)
    ax1.bar(bincenters,y, color=c,lw=0.2, zs=zs, zdir='y', label=labels[zs]+' primaries')

    ax1.set_xlabel('Falloff Position [mm]', fontsize=FONTSIZE)
    ax1.set_zlabel('[counts]', fontsize=FONTSIZE)
    ax1.locator_params(axis='y',nbins=len(labels))
    ax1.set_yticklabels(labels, va='baseline', ha='left',fontsize=Fontsize)
    ax1.set_ylabel('Primaries [nr]', fontsize=FONTSIZE)

    labelCT_extra=''
    if emisfops is not None and len(emisfops) == len(labels):
        labelCT_extra+=', $FOP_{em}$ = '+str(emisfops[zs][0])
    else:
        labelCT_extra+='$\pm$'+str(ctsigma/sqrt(2*(len(fo_ct)-1)))[:4]
    plot.figtext(0.01, 0.95-zs/10.,labels[zs]+ct['ct']['label']+": $\mu_{FOP}$ = "+str(ctmu)[:4]+", $\sigma_{FOP}$ = "+str(ctsigma)[:4]+labelCT_extra, ha='left', va='center', fontsize=Fontsize, transform=ax1.transAxes)
