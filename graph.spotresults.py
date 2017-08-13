#!/usr/bin/env python
# -*- coding: utf-8 -*-
import plot

# MPS, KES, (ABC)
f, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plot.subplots(nrows=2, ncols=3, sharex=True, sharey=True)


X = [10**9,10**8,2.7*10**7,10**7]
#dX = {'$10^9$','$10^8$','$2.7\cdot 10^7$','$10^7$'}
Y = [2.68,2.83,2.51,4.43]
Yd = [0.77,1.90,4.05,32.9]
ax1.errorbar(X,Y,yerr=Yd,color='black',fmt='.',lw=1.)
ax1.semilogx()
ax1.set_xlim(8*10**6,1.2*10**9)
ax1.set_ylim(-30,30)
ax1.set_title('MPS Spot A')


X = [10**9,10**8,2.7*10**7,10**7]
Y = [3.23,3.12,3.76,2.91]
Yd = [0.77,2.14,4.36,17.4]
ax2.errorbar(X,Y,yerr=Yd,color='black',fmt='.',lw=1.)
ax2.semilogx()
ax2.set_xlim(8*10**6,1.2*10**9)
ax2.set_title('MPS Spot B')


X = [10**9,10**8,4.7*10**7,10**7]
Y = [12.6,11.6,12.5,7.31]
Yd = [1.15,3.25,4.73,58.9]
ax3.errorbar(X,Y,yerr=Yd,color='black',fmt='.',lw=1.)
ax3.semilogx()
ax3.set_xlim(8*10**6,1.2*10**9)
ax3.set_title('MPS Spot C')

X = [10**9,10**8,2.7*10**7,10**7]
#dX = {'$10^9$','$10^8$','$2.7\cdot 10^7$','$10^7$'}
Y = [2.56,3.90,-1.2,4.54]
Yd = [1.93,9.71,28.9,27.1]
ax4.errorbar(X,Y,yerr=Yd,color='black',fmt='.',lw=1.)
ax4.semilogx()
ax4.set_xlim(8*10**6,1.2*10**9)
ax4.set_title('KES Spot A')


X = [10**9,10**8,2.7*10**7,10**7]
Y = [3.27,2.90,-0.2,9.58]
Yd = [2.24,13.3,23.7,24.6]
ax5.errorbar(X,Y,yerr=Yd,color='black',fmt='.',lw=1.)
ax5.semilogx()
ax5.set_xlim(8*10**6,1.2*10**9)
ax5.set_title('KES Spot B')


X = [10**9,10**8,4.7*10**7,10**7]
Y = [9.79,7.01,4.30,-3.8]
Yd = [2.25,16.2,18.2,26.2]
ax6.errorbar(X,Y,yerr=Yd,color='black',fmt='.',lw=1.)
ax6.semilogx()
ax6.set_xlim(8*10**6,1.2*10**9)
ax6.set_title('KES Spot C')


ax1.axhline(2.77, color='indianred', ls='-',lw=1, alpha=0.5)
ax4.axhline(2.77, color='indianred', ls='-',lw=1, alpha=0.5)
ax2.axhline(4.08, color='indianred', ls='-',lw=1, alpha=0.5)
ax5.axhline(4.08, color='indianred', ls='-',lw=1, alpha=0.5)
ax3.axhline(12.4, color='indianred', ls='-',lw=1, alpha=0.5)
ax6.axhline(12.4, color='indianred', ls='-',lw=1, alpha=0.5)



f.savefig('spotresults.pdf', bbox_inches='tight')
plot.close('all')

