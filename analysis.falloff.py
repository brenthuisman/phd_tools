#!/usr/bin/env python
import numpy as np,plot,auger
import scipy.stats
from numpy import sqrt

#OPT: quickly get sorted rundirs
# zb autogen | sort -k1.13 -r

#OPT: fix seed
#np.random.seed(65983247)

#we dont know what the added or reduced noise level is when changing energy windows, so we cant compare performance for ipnl3 and iba1.
typs=['ipnl-auger-tof-1.root','iba-auger-notof-3.root']

def megaplot(ctsets,studyname,emisfops=None,labels=["$10^9$","$10^8$","$10^7$","$10^6$"],axlabel='Primaries [nr]'):
    #if emisfops is not None:
        #for emisfop in emisfops:
            #emisfop[0]+=15.863
            #emisfop[1]+=15.863
    print 'FOP shift all overlaid'
    
    #if len(ctsets) == 3:
        #f, (ax1,ax2,ax3) = plot.subplots(nrows=1, ncols=3, sharex=False, sharey=False)
        #auger.plot_all_ranges(ax1,ctsets[0])
        #auger.plot_all_ranges(ax2,ctsets[1])
        #auger.plot_all_ranges(ax3,ctsets[2])
        #f.savefig(studyname+'-'+typ+'-FOP.pdf', bbox_inches='tight')
        #plot.close('all')
        #f.subplots_adjust(hspace=.5)
        #ax2.set_ylabel('')
        #ax3.set_ylabel('')

    if len(ctsets) > 2:
        f, ((ax1,ax2),(ax3,ax4)) = plot.subplots(nrows=2, ncols=2, sharex=False, sharey=False)
        ax1.set_xlabel('')
        ax2.set_xlabel('')
        ax2.set_ylabel('')
        ax4.set_ylabel('')
    elif len(ctsets) == 2:
        f, (ax1,ax2) = plot.subplots(nrows=1, ncols=2, sharex=False, sharey=False)
        ax2.set_xlabel('')
        
    f.subplots_adjust(hspace=0.7,wspace=0.5)
    
    auger.plot_all_ranges(ax1,ctsets[0])
    auger.plot_all_ranges(ax2,ctsets[1])
    if len(ctsets) > 2:
        try:
            auger.plot_all_ranges(ax3,ctsets[2])
        except:
            ax3.axis('off')
        try:
            auger.plot_all_ranges(ax4,ctsets[3])
        except:
            ax4.axis('off')
    
    #auger.plot_single_range(ax1,ctsets[0])
    #auger.plot_single_range(ax2,ctsets[1])
    #auger.plot_single_range(ax3,ctsets[2])
    #auger.plot_single_range(ax4,ctsets[3])
    
    if not 'Primaries' in axlabel:
        ax1.set_title(labels[0])
        ax2.set_title(labels[1])
        #ax3.set_title(labels[2])
        #ax4.set_title(labels[3])
    
    #if 'waterbox' in studyname:
        #import matplotlib
        #matplotlib.pyplot.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        #f.subplots_adjust(wspace=.3)
        
        #x0 = []
        #y1 = []
        #y1std = []
        #y2 = []
        #y2std = []
        #for ct in ctsets:
            #x0.append(1./sqrt(ct['nprim']))
            #y1.append(ct['ct']['fopsigma'])
            #y2.append(ct['rpct']['fopsigma'])
            #y1std.append( ct['ct']['fopsigma']/sqrt(2*(len(ct['ct']['falloff'])-1)) )
            #y2std.append( ct['rpct']['fopsigma']/sqrt(2*(len(ct['rpct']['falloff'])-1)) )
        #plot.plot_errorbands(ax4,x0,y1,y1std,color='steelblue')
        #plot.plot_errorbands(ax4,x0,y2,y2std,color='indianred')
        ##ax4.set_xlim(x[0],x[-1])
        ##ax4.set_ylim(y[0],y[-1])
        #ax4.set_title('CNR check', fontsize=8)
        #ax4.set_xlabel('1/sqrt(N$_{prim}$)', fontsize=8)
        ##ax4.set_ylabel('sqrt(background)/signal', fontsize=8)
        #ax4.set_ylabel('$\sigma_{FOP} [mm]$', fontsize=8)
        #plot.texax(ax4)
    
    f.savefig(studyname+'-'+typ+'-FOP.pdf', bbox_inches='tight')
    plot.close('all')

    #############################################################################################

    print 'FOP shift distributions'

    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax1 = plt.axes(projection='3d')
    ax1.view_init(30, -50)

    tmpprim=0
    center=0
    for ctset in ctsets:
        if ctset['nprim'] > tmpprim:
            tmpprim = ctset['nprim']
            center= ctset['fodiffmu']
    
    for i,ctset in enumerate(ctsets):
        auger.plotfodiffdist(ax1,ctset,i,emisfops,labels,axlabel,center)
        if not emisfops == None:
            fopshifts=[]
            for fopset in emisfops:
                fopshifts.append( fopset[-1]-fopset[0] )
            ax1.set_xlim3d(np.mean(fopshifts)-20,np.mean(fopshifts)+20)
    if emisfops is not None and len(emisfops) == 1:
        ax1.set_title(studyname+', $Shift_{em}$ = '+str(emisfops[0][-1]-emisfops[0][0]), y=1.08)
        pass
        
    #fig.suptitle('FOP shifts', fontsize=10)
    #plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
    fig.savefig(studyname+'-'+typ+'-FOP-shift.pdf')#, bbox_inches='tight')
    plt.close('all')

    #############################################################################################

    print 'FOP distributions'

    fig = plt.figure()
    ax1 = plt.axes(projection='3d')
    ax1.view_init(30, -50)
    
    tmpprim=0
    center=0
    for ctset in ctsets:
        if ctset['nprim'] > tmpprim:
            tmpprim = ctset['nprim']
            center= ( ctset['ct']['fopmu'] + ctset['rpct']['fopmu'] ) /2.
    
    for i,ctset in enumerate(ctsets):
        auger.plotfodist(ax1,ctset,i,emisfops,labels,axlabel,center)
    if emisfops is not None and len(emisfops) == 1:
        ax1.set_title(studyname+', $CT_{FOP_{em}}$ = '+str(emisfops[0][0])[:5]+', $RPCT_{FOP_{em}}$ = '+str(emisfops[0][1])[:5], y=1.08)

    #plt.legend()#shadow = True,frameon = True,fancybox = True,ncol = 1,fontsize = 'x-small',loc = 'lower right')

    #plt.tight_layout(rect = [-0.1, 0.0, 1.0, 1.1])#L,B,R,T
    #fig.suptitle('FOP distributions', fontsize=10)
    plt.savefig(studyname+'-'+typ+'-FOP-dist.pdf')#, bbox_inches='tight')
    plt.close('all')
    
#############################################################################################

# DOOS WATER

#for typ in typs:
    #ctsetsets = []
    #################### DOOS WATER
    
    #ctsetsets.append( auger.getctset(1e9,'run.8ZQJ','run.ahDK',typ) )
    #ctsetsets.append( auger.getctset(1e8,'run.fhf7','run.XKeV',typ) )
    #ctsetsets.append( auger.getctset(1e7,'run.aNz9','run.NnKH',typ) )
    #megaplot(ctsetsets,'waterbox',emisfops=None,labels=["$10^9$","$10^8$","$10^7$"])
    
#quit()


#############################################################################################

typ = 'ipnl-auger-tof-1.root'

#shift = 13.76-19.44
#ctsetsets = []
#ctsetsets.append( auger.getctset(1e9,'run.pMSA','run.gwKk',typ,manualshift=shift) )
#ctsetsets.append( auger.getctset(1e8,'run.GJHJ','run.9BY9',typ,manualshift=shift) )
#ctsetsets.append( auger.getctset(27500000,'run.aZp5','run.13px',typ,manualshift=shift) )
#ctsetsets.append( auger.getctset(1e7,'run.EPjL','run.jNjK',typ,manualshift=shift) )
#megaplot(ctsetsets,'spot29',emisfops=None,labels=["$10^9$","$10^8$","$2.7\cdot10^7$","$10^7$"])

#shift = 4.89-8.53
#ctsetsets = []
#ctsetsets.append( auger.getctset(1e9,'run.TtIT','run.SmHn',typ,manualshift=shift) )
#ctsetsets.append( auger.getctset(1e8,'run.t4Fb','run.w9Te',typ,manualshift=shift) )
#ctsetsets.append( auger.getctset(27200000,'run.YtND','run.SQy4',typ,manualshift=shift) )
#ctsetsets.append( auger.getctset(1e7,'run.WQUJ','run.JJQQ',typ,manualshift=shift) )
#megaplot(ctsetsets,'spot40',emisfops=None,labels=["$10^9$","$10^8$","$2.7\cdot10^7$","$10^7$"])

#shift = 22.20-29.04
#ctsetsets = []
#ctsetsets.append( auger.getctset(1e9,'run.EYBe','run.6HvZ',typ,manualshift=shift) )
#ctsetsets.append( auger.getctset(1e8,'run.W3sR','run.q7v2',typ,manualshift=shift) )
#ctsetsets.append( auger.getctset(47300000,'run.R9KU','run.rTUp',typ,manualshift=shift) )
#ctsetsets.append( auger.getctset(1e7,'run.1jXf','run.8NDz',typ,manualshift=shift) )
#megaplot(ctsetsets,'spot61',emisfops=None,labels=["$10^9$","$10^8$","$4.7\cdot10^7$","$10^7$"])

ctsetsets = []
ctsetsets.append( auger.getctset(840964615,'run.CKCH','run.lrnj',typ) )#elay
ctsetsets.append( auger.getctset(848710335,'run.3At2','run.Ydep',typ) )#geolay
megaplot(ctsetsets,'layer29',emisfops=None,labels=['Iso-Energy Layer','Iso-Depth Layer'],axlabel='Grouping Method')

ctsetsets = []
ctsetsets.append( auger.getctset(1068263318,'run.7coj','run.ptEe',typ) )#elay, same as elay61
ctsetsets.append( auger.getctset(1071596684,'run.KXRm','run.jTj9',typ) )#geolay
megaplot(ctsetsets,'layer40',emisfops=None,labels=['Iso-Energy Layer','Iso-Depth Layer'],axlabel='Grouping Method')

ctsetsets = []
ctsetsets.append( auger.getctset(1068263318,'run.7coj','run.ptEe',typ,manualshift=15.37-19.00) )#elay
ctsetsets.append( auger.getctset(979533764,'run.8aMd','run.wM5z',typ,manualshift=18.57-23.51) )#geolay
megaplot(ctsetsets,'layer61',emisfops=None,labels=['Iso-Energy Layer','Iso-Depth Layer'],axlabel='Grouping Method')

#############################################################################################

typ = 'iba-auger-notof-3.root'

#ctsetsets = []
#ctsetsets.append( auger.getctset(1e9,'run.k0Zs','run.Y1My',typ) )
#ctsetsets.append( auger.getctset(1e8,'run.ELdW','run.7IAj',typ) )
#ctsetsets.append( auger.getctset(27500000,'run.Z8xA','run.4dwm',typ) )
#ctsetsets.append( auger.getctset(1e7,'run.p6RP','run.DVrS',typ) )
#megaplot(ctsetsets,'spot29',emisfops=None,labels=["$10^9$","$10^8$","$2.7\cdot10^7$","$10^7$"])

#ctsetsets = []
#ctsetsets.append( auger.getctset(1e9,'run.tsUO','run.TUEA',typ) )
#ctsetsets.append( auger.getctset(1e8,'run.biax','run.JVt7',typ) )
#ctsetsets.append( auger.getctset(27200000,'run.hsED','run.MHBk',typ) )
#ctsetsets.append( auger.getctset(1e7,'run.2dJ0','run.eUzn',typ) )
#megaplot(ctsetsets,'spot40',emisfops=None,labels=["$10^9$","$10^8$","$2.7\cdot10^7$","$10^7$"])

#ctsetsets = []
#ctsetsets.append( auger.getctset(1e9,'run.tf1u','run.cDeA',typ) )
#ctsetsets.append( auger.getctset(1e8,'run.XkzK','run.5m0c',typ) )
#ctsetsets.append( auger.getctset(47300000,'run.vF4V','run.NjV4',typ) )
#ctsetsets.append( auger.getctset(1e7,'run.6GoN','run.KAN5',typ) )
#megaplot(ctsetsets,'spot61',emisfops=None,labels=["$10^9$","$10^8$","$4.7\cdot10^7$","$10^7$"])

ctsetsets = []
ctsetsets.append( auger.getctset(840964615,'run.e8ai','run.96ra',typ) )#elay
ctsetsets.append( auger.getctset(848710335,'run.m4RU','run.tLiY',typ) )#geolay
megaplot(ctsetsets,'layer29',emisfops=None,labels=['Energy Layer','Geometric Layer'],axlabel='Grouping Method')

ctsetsets = []
ctsetsets.append( auger.getctset(1068263318,'run.E2tF','run.qE8o',typ) )#elay, same as elay61
ctsetsets.append( auger.getctset(1071596684,'run.r48i','run.c0rg',typ) )#geolay
megaplot(ctsetsets,'layer40',emisfops=None,labels=['Energy Layer','Geometric Layer'],axlabel='Grouping Method')

ctsetsets = []
ctsetsets.append( auger.getctset(1068263318,'run.E2tF','run.qE8o',typ) )#elay
ctsetsets.append( auger.getctset(979533764,'run.c4UF','run.bj2R',typ) )#geolay
megaplot(ctsetsets,'layer61',emisfops=None,labels=['Energy Layer','Geometric Layer'],axlabel='Grouping Method')

#############################################################################################




#for typ in typs[:-1]: #alleen IPNL
    #ctsetsets = []
    
    
    ##################### mysterspot
    
    #ctsetsets.append( auger.getctset(1e9,'run.tf4M','run.Ag4Z',typ) )
    #ctsetsets.append( auger.getctset(1e9,'run.OZPS','run.4U1m',typ) )
    #ctsetsets.append( auger.getctset(1e9,'run.sq6A','run.sXI3',typ) )
    #megaplot(ctsetsets,'shiftedspotandair',emisfops=None,labels=["spot29","spot40","spot61"])
    
    #################### DOOS WATER
    
    #ctsetsets.append( auger.getctset(1e9,'run.8ZQJ','run.ahDK',typ) )
    #ctsetsets.append( auger.getctset(1e8,'run.fhf7','run.XKeV',typ) )
    #ctsetsets.append( auger.getctset(1e7,'run.aNz9','run.NnKH',typ) )
    #megaplot(ctsetsets,'waterbox')
    
    #ctsetsets.append( auger.getctset(1e9,'run.8ZQJ','run.DeJf',typ) )
    #ctsetsets.append( auger.getctset(1e8,'run.fhf7','run.yS7a',typ) )
    #ctsetsets.append( auger.getctset(1e7,'run.aNz9','run.gKIX',typ) )
    #megaplot(ctsetsets,'waterboxshifted')
    
    ###################### SPOTS TO SHIFT OR NOT TO SHIFT
    
    #ctsetsets.append( auger.getctset(1e9,'run.pMSA','run.gwKk',typ) )
    #ctsetsets.append( auger.getctset(1e9,'run.pMSA','run.Ogb8',typ) )
    #ctsetsets.append( auger.getctset(27500000,'run.aZp5','run.13px',typ) )
    #ctsetsets.append( auger.getctset(27500000,'run.aZp5','run.RKsb',typ) )
    #megaplot(ctsetsets,'spot29-shiftcomp',emisfops=None,labels=["Unaligned $4.7\cdot10^7$","Aligned $4.7\cdot10^7$","Unaligned $10^9$","Aligned $10^9$"])
    
    #ctsetsets.append( auger.getctset(1e9,'run.TtIT','run.',typ) )
    #ctsetsets.append( auger.getctset(1e8,'run.t4Fb','run.',typ) )
    #ctsetsets.append( auger.getctset(27200000,'run.YtND','run.',typ) )
    #ctsetsets.append( auger.getctset(1e7,'run.WQUJ','run.',typ) )
    #megaplot(ctsetsets,'spot40',emisfops=None,labels=["$10^9$","$10^8$","$2.7\cdot10^7$","$10^7$"])
    
    #ctsetsets.append( auger.getctset(47300000,'run.R9KU','run.rTUp',typ) )
    #ctsetsets.append( auger.getctset(47300000,'run.R9KU','run.TOku',typ) )
    #ctsetsets.append( auger.getctset(1e9,'run.EYBe','run.6HvZ',typ) )
    #ctsetsets.append( auger.getctset(1e9,'run.EYBe','run.9fc1',typ) )
    #megaplot(ctsetsets,'spot61-shiftcomp',emisfops=None,labels=["Unaligned $4.7\cdot10^7$","Aligned $4.7\cdot10^7$","Unaligned $10^9$","Aligned $10^9$"])
    
    ##################### SPOTS ZONDER RPCT SHIFT
    
    #ctsetsets.append( auger.getctset(1e9,'run.pMSA','run.gwKk',typ) )
    #ctsetsets.append( auger.getctset(1e8,'run.GJHJ','run.9BY9',typ) )
    #ctsetsets.append( auger.getctset(27500000,'run.aZp5','run.13px',typ) )
    #ctsetsets.append( auger.getctset(1e7,'run.EPjL','run.jNjK',typ) )
    #megaplot(ctsetsets,'spot29',emisfops=None,labels=["$10^9$","$10^8$","$2.7\cdot10^7$","$10^7$"])
    
    #ctsetsets.append( auger.getctset(1e9,'run.TtIT','run.SmHn',typ) )
    #ctsetsets.append( auger.getctset(1e8,'run.t4Fb','run.w9Te',typ) )
    #ctsetsets.append( auger.getctset(27200000,'run.YtND','run.SQy4',typ) )
    #ctsetsets.append( auger.getctset(1e7,'run.WQUJ','run.JJQQ',typ) )
    #megaplot(ctsetsets,'spot40',emisfops=None,labels=["$10^9$","$10^8$","$2.7\cdot10^7$","$10^7$"])
    
    #ctsetsets.append( auger.getctset(1e9,'run.EYBe','run.6HvZ',typ) )
    #ctsetsets.append( auger.getctset(1e8,'run.W3sR','run.q7v2',typ) )
    #ctsetsets.append( auger.getctset(47300000,'r8675un.R9KU','run.rTUp',typ) )
    #ctsetsets.append( auger.getctset(1e7,'run.1jXf','run.8NDz',typ) )
    #megaplot(ctsetsets,'spot61',emisfops=None,labels=["$10^9$","$10^8$","$4.7\cdot10^7$","$10^7$"])
    
    ##FOP SINGLE REAL IN FOP plot
    #ctsetsets.append( auger.getctset(1e9,'run.EYBe','run.6HvZ',typ) )
    #ctsetsets.append( auger.getctset(1e8,'run.W3sR','run.q7v2',typ) )
    ##ctsetsets.append( auger.getctset(47300000,'run.R9KU','run.rTUp',typ) )
    #ctsetsets.append( auger.getctset(1e7,'run.1jXf','run.8NDz',typ) )
    #megaplot(ctsetsets,'spot61')#,emisfops=None,labels=["$10^9$","$10^8$","$4.7\cdot10^7$","$10^7$"])
    
    ################## LAGEN NIEUW
    
    #ctsetsets.append( auger.getctset(1068263318,'run.7coj','run.ptEe',typ) )#elay
    #ctsetsets.append( auger.getctset(979533764,'run.8aMd','run.wM5z',typ) )#geolay
    #megaplot(ctsetsets,'laygroup3',emisfops=None,labels=['Energy Layer','Geometric Layer'],axlabel='Grouping Method')
    
    ################## LAGEN OUD
    
    #ctsetsets.append( auger.getctset(27500000,'run.LUBP','run.hRZn',typ) )#spot29#
    #ctsetsets.append( auger.getctset(47300000,'run.7WZC','run.3Zs9',typ) )#spot61# 3 , 11 # s3aB, 4gLD+TWZQ		:done
    #megaplot(ctsetsets,'realspots',[[-1.75,0.291],[6.715,20.58]],['Spot 29','Spot 61'],'Spot Nr')
    
    #elay fopshift 4.3359375, geolay fopshift 6.359375
    #ctsetsets.append( auger.getctset(513093255,'run.Gi7J','run.aSej',typ) )#elay	# 0,6 # , F3gZ # +UROr 7x (4x)
    #ctsetsets.append( auger.getctset(537825202,'run.WfRk','run.F4bu',typ) )#geolay# 0,2 # , bvJG # +XJ8V 3x
    #megaplot(ctsetsets,'laygroup',[[0,4.33],[0,6.35]],['Energy Layer','Geometric Layer'],'Grouping Method')
    
    #########################################################
    
    #print 'Mean detection yield in',typ,'study over',sum([ctset['totnprim'] for ctset in ctsetsets]),'primaries in',sum([ctset['nreal'] for ctset in ctsetsets]),'realisations:',np.mean([ctset['meandetyield'] for ctset in ctsetsets])
    




#for typ in typs[1:]: #alleen IBA, 20x
    #ctsetsets = []
    
    #ctsetsets.append( auger.getctset(1e9,'run.sY3D','run.9cmS',typ) )
    #ctsetsets.append( auger.getctset(1e8,'run.1TXU','run.j5lq',typ) )
    #ctsetsets.append( auger.getctset(27500000,'run.ehp9','run.lrlL',typ) )
    #ctsetsets.append( auger.getctset(1e7,'run.uQhk','run.ICSw',typ) )
    #megaplot(ctsetsets,'spot29',emisfops=None,labels=["$10^9$","$10^8$","$2.7\cdot10^7$","$10^7$"])
    
    #ctsetsets.append( auger.getctset(1e9,'run.0062','run.d5DD',typ) )
    #ctsetsets.append( auger.getctset(1e8,'run.RhZs','run.eau7',typ) )
    #ctsetsets.append( auger.getctset(27200000,'run.nmvW','run.Ksi3',typ) )
    #ctsetsets.append( auger.getctset(1e7,'run.xVLD','run.YQVO',typ) )
    #megaplot(ctsetsets,'spot40',emisfops=None,labels=["$10^9$","$10^8$","$2.7\cdot10^7$","$10^7$"])
    
    #ctsetsets.append( auger.getctset(1e9,'run.0WTh','run.IKqq',typ) )
    #ctsetsets.append( auger.getctset(1e8,'run.3k90','run.IetF',typ) )
    #ctsetsets.append( auger.getctset(47300000,'run.Qek9','run.xdFW',typ) )
    #ctsetsets.append( auger.getctset(1e7,'run.Jvi1','run.tV26',typ) )
    #megaplot(ctsetsets,'spot61',emisfops=None,labels=["$10^9$","$10^8$","$4.7\cdot10^7$","$10^7$"])
    
    #ctsetsets.append( auger.getctset(1068263318,'run.E2tF','run.qE8o',typ) )#elay
    #ctsetsets.append( auger.getctset(979533764,'run.c4UF','run.bj2R',typ) )#geolay
    #megaplot(ctsetsets,'laygroup3',emisfops=None,labels=['Energy Layer','Geometric Layer'],axlabel='Grouping Method')
    
    #print 'Mean detection yield in',typ,'study over',sum([ctset['totnprim'] for ctset in ctsetsets]),'primaries in',sum([ctset['nreal'] for ctset in ctsetsets]),'realisations:',np.mean([ctset['meandetyield'] for ctset in ctsetsets])
    
