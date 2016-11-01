#!/usr/bin/env python
import matplotlib.pyplot as plt,numpy as np,plot


## first barplot setup
barf, (barax1,barax2,barax3) = plt.subplots(nrows=1, ncols=3, sharex=False, sharey=False)
N = 4 #3 outputs
ind = np.arange(N)                # the x locations for the groups
width = 0.4                      # the width of the bars

labelbar = ('2nd order','3rd order','4th order','5th order')
full = [5.65,3.30,3.30,3.01,2.51,2.51]
layer = [-1.88,-0.94,-0.94,-1.00,-0.50,-0.50]
spot = [-1.88,-1.41,-3.77,-2.51,-3.51,-3.01]


## finish barplot
rects1 = barax1.bar(ind, full[:3]+[0], width, color='red')
rects2 = barax1.bar(ind+width, [0]+full[3:], width, color='blue')
rects3 = barax2.bar(ind, layer[:3]+[0], width, color='red')
rects4 = barax2.bar(ind+width, [0]+layer[3:], width, color='blue')
rects5 = barax3.bar(ind, spot[:3]+[0], width, color='red')
rects6 = barax3.bar(ind+width, [0]+spot[3:], width, color='blue')

# axes and labels
barax1.set_xlim(-width,len(ind)+width)
barax1.set_ylabel('Shift [mm]')
barax1.set_title('Full field')
xTickMarks = labelbar
barax1.set_xticks(ind+width)
xtickNames = barax1.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=45, fontsize=10)
plot.texax(barax1)

# axes and labels2
barax2.set_xlim(-width,len(ind)+width)
barax2.set_ylabel('Shift [mm]')
barax2.set_title('Layer')
xTickMarks = labelbar
barax2.set_xticks(ind+width)
xtickNames = barax2.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=45, fontsize=10)
plot.texax(barax2)

barax3.set_xlim(-width,len(ind)+width)
barax3.set_ylabel('Shift [mm]')
barax3.set_title('Spot')
xTickMarks = labelbar
barax3.set_xticks(ind+width)
xtickNames = barax3.set_xticklabels(xTickMarks)
plt.setp(xtickNames, rotation=45, fontsize=10)
plot.texax(barax3)

## add a legend

barax3.legend( (rects5[0], rects6[0]), ('Rebinned','Smoothed') )

barf.savefig('fitprocs.png', bbox_inches='tight',dpi=300)
