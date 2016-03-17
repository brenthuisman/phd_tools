#!/usr/bin/env python
import sys,matplotlib.pyplot as plt,math,pickle,numpy as np,graph,image

tle_prims = 1e3
an_prims = 1e6

# ------------------------------------------------------
print "Loading..."

plt.style.use('ggplot')

# -------------------------------------------- zzzzzzzz

depth = np.linspace(0,690,69)

tlez = pickle.load(open("source.x.list"))
tlevarz = pickle.load(open("source-tlevar.x.list"))
analogz = pickle.load(open("analog.x.list"))
# -------------------------------------------- spect

spectbins = np.linspace(0,10,250)

tlespect = pickle.load(open("source.spect.list"))
tlevarspect = pickle.load(open("source-tlevar.spect.list"))
analogspect = pickle.load(open("analog.spect.list"))
print analogspect[0],analogspect[1],analogspect[2]
print tlespect[0],tlespect[1],tlespect[2]

# ------------------------------------------------------
print "Loaded. Prepping data..."

# ------------------------------------------------------
# From yield to counts

tlez_abs = [i*tle_prims for i in tlez]
analogz_abs = [i*an_prims for i in analogz]
# spect
tlespect_abs = [i*tle_prims for i in tlespect]
analogspect_abs = [i*an_prims for i in analogspect]

# ------------------------------------------------------
# Get uncertainties and uncertainty bands

tleuncz = [math.sqrt(item) for item in tlevarz]
analoguncz = [math.sqrt( item/an_prims ) if item!=0 else math.sqrt( 1/an_prims ) for item in analogz]

tlez_minus, tlez_plus = graph.geterrorbands(tleuncz, tlez)
analoguncz_minus, analoguncz_plus = graph.geterrorbands(analoguncz, analogz)

# spect
tleuncspect = [math.sqrt(item) for item in tlevarspect]
analoguncspect = [math.sqrt( item/an_prims ) if item!=0 else math.sqrt( 1/an_prims ) for item in analogspect]

tlespect_minus,tlespect_plus = graph.geterrorbands(tleuncspect, tlespect)
analoguncspect_minus,analoguncspect_plus = graph.geterrorbands(analoguncspect, analogspect)


# ------------------------------------------------------
# Get relative uncertainties
# multiply by 100 to get a percentage

tleuncz_rel = [unc/sig*100 if sig != 0 else unc*100 for unc,sig in zip(tleuncz,tlez)]
analoguncz_rel = [unc/sig*100 if sig != 0 else unc*100 for unc,sig in zip(analoguncz,analogz)]

# spect
tleuncspect_rel = [unc/sig*100 if sig != 0 else unc*100 for unc,sig in zip(tleuncspect,tlespect)]
analoguncspect_rel = [unc/sig*100 if sig != 0 else unc*100 for unc,sig in zip(analoguncspect,analogspect)]

# ------------------------------------------------------
# Get analog-relative plots for analog unc, and tle+tle unc
# get signal/unc weighted by analog signal, so that we can plot the relative error bands.
# multiply by 100 to get a percentage

analogz_anrel = [0 for i in analogz] #relative to analog, is ofc 1
analoguncz_anrel_low = [(unc/an-1) if an != 0. else unc for unc,an in zip(analoguncz_minus, analogz)]
analoguncz_anrel_high = [(unc/an-1) if an != 0. else unc for unc,an in zip(analoguncz_plus, analogz)]

tlez_anrel = [100*(tle/an-1) if an != 0. else 100*tle for tle,an in zip(tlez, analogz)]
tleuncz_anrel_low = [(unc/an-1) if an != 0. else unc for unc,an in zip(tlez_minus, analogz)]
tleuncz_anrel_high = [(unc/an-1) if an != 0. else unc for unc,an in zip(tlez_plus, analogz)]

# spect
analogspect_anrel = [0 for i in analogspect] #relative to analog, is ofc 1
analoguncspect_anrel_low = [(unc/an-1) if an != 0. else unc for unc,an in zip(analoguncspect_minus, analogspect)]
analoguncspect_anrel_high = [(unc/an-1) if an != 0. else unc for unc,an in zip(analoguncspect_plus, analogspect)]

tlespect_anrel = [100*(tle/an-1) if an != 0. else 100*tle for tle,an in zip(tlespect, analogspect)]
tleuncspect_anrel_low = [(unc/an-1) if an != 0. else unc for unc,an in zip(tlespect_minus, analogspect)]
tleuncspect_anrel_high = [(unc/an-1) if an != 0. else unc for unc,an in zip(tlespect_plus, analogspect)]

# ------------------------------------------------------
print "Prep complete. Making plots..."

# ------------------------------------------------------
# Yield plot

f, (ax1, ax2) = plt.subplots(ncols=2,figsize=(16, 9), dpi=200, sharex=False, sharey=False)
ax1.step(depth,analogz, where='mid', label="analogz", color='red')
ax1.step(depth,tlez, where='mid', label="tlez", color='green')
ax1.fill_between(depth, analoguncz_minus, analoguncz_plus, alpha=0.25, color='red')
ax1.fill_between(depth, tlez_minus, tlez_plus, alpha=0.25, color='green')
ax1.set_xlabel('Depth [mm]')
ax1.set_ylabel('PG yield + uncertainty')

ax2.step(spectbins,analogspect, where='mid', label="analogspect", color='red')
ax2.step(spectbins,tlespect, where='mid', label="tlespect", color='green')
ax2.fill_between(spectbins, analoguncspect_minus, analoguncspect_plus, alpha=0.25, color='red')
ax2.fill_between(spectbins, tlespect_minus, tlespect_plus, alpha=0.25, color='green')
ax2.set_xlabel('PG Energy [MeV]')
ax2.set_ylabel('PG yield + uncertainty')
ax2.set_ylim([-.001,.005])

plt.legend(prop={'size':10},loc='best')
plt.tight_layout()
plt.savefig("yield.png")
plt.close('all')

# ------------------------------------------------------
# Error plot
# wont use.

f, (ax1, ax2) = plt.subplots(ncols=2,figsize=(16, 9), dpi=200, sharex=False, sharey=False)
ax1.step(depth,analoguncz, where='mid', label="analoguncz", color='red')
ax1.step(depth,tleuncz, where='mid', label="tleuncz", color='green')
ax1.set_ylim([0.,0.00007])
ax1.set_xlabel('Depth [mm]')
ax1.set_ylabel('Absolute PG uncertainty')

ax2.step(spectbins,analoguncspect, where='mid', label="analoguncspect", color='red')
ax2.step(spectbins,tleuncspect, where='mid', label="tleuncspect", color='green')
ax2.set_ylim([0.,0.00007])
ax2.set_xlabel('PG Energy [MeV]')
ax2.set_ylabel('Absolute PG uncertainty')

plt.legend(prop={'size':10},loc='best')
plt.tight_layout()
plt.savefig("abs-uncertainty.png")
plt.close('all')

# ------------------------------------------------------
# Relative yield + Relative Error plot

f, ((ax1, ax4), (ax2, ax5)) = plt.subplots(nrows=2, ncols=2,figsize=(16, 9), dpi=200, sharex=False, sharey=False)
ax1.step(depth,analogz_anrel, where='mid', label="analogz_anrel", color='red')
ax1.step(depth,tlez_anrel, where='mid', label="tlez_anrel", color='green')
ax1.set_ylabel('TLE / Analog [%]')
ax1.set_xlim([0,170])

ax4.step(spectbins,analogspect_anrel, where='mid', label="analogspect_anrel", color='red')
ax4.step(spectbins,tlespect_anrel, where='mid', label="tlespect_anrel", color='green')

ax2.step(depth,analoguncz_rel, where='mid', label="analoguncz_rel", color='red')
ax2.step(depth,tleuncz_rel, where='mid', label="tleuncz_rel", color='green')
ax2.set_ylabel('Rel. Unc. [%]')
ax2.semilogy()
ax2.grid(color='#cccccc')
ax2.set_xlim([0,170])

ax5.step(spectbins,analoguncspect_rel, where='mid', label="analoguncspect_rel", color='red')
ax5.step(spectbins,tleuncspect_rel, where='mid', label="tleuncspect_rel", color='green')
ax5.semilogy()
ax5.grid(color='#cccccc')

plt.legend(prop={'size':10},loc='best')
plt.tight_layout()
plt.savefig("relyield-relerror.png")
plt.close('all')

# ------------------------------------------------------
# Analog-Relative plots
# Useless plot, wont use.

plt.step(depth,analogz_anrel, where='mid', label="analogz_anrel", color='red')
plt.step(depth,tlez_anrel, where='mid', label="tlez_anrel", color='green')
plt.fill_between(depth, analoguncz_anrel_low, analoguncz_anrel_high, alpha=0.25, color='red')
plt.fill_between(depth, tleuncz_anrel_low, tleuncz_anrel_high, alpha=0.25, color='green')

axes = plt.gca()
axes.set_ylim([-.5,.5])
plt.xlabel('Depth [mm]')
plt.ylabel('PG yield / Analog yield')
plt.legend(prop={'size':10},loc='best')
#plt.savefig("analog-relative.png")
plt.close('all')
