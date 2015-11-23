import numpy as np
import pylab
import scipy.cluster.hierarchy as sch

# Generate random features and distance matrix.
#x = scipy.rand(40)
#D = scipy.zeros([40,40])
#for i in range(40):
#    for j in range(40):
#        D[i,j] = abs(x[i] - x[j])
D=np.loadtxt('count')


# Compute and plot first dendrogram.
fig = pylab.figure(figsize=(8,8))
ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
Y = sch.linkage(D, method='complete') #
Z1 = sch.dendrogram(Y, orientation='right')
ax1.set_xticks([])
ax1.set_yticks([])

# Compute and plot second dendrogram.
ax2 = fig.add_axes([0.3,0.71,0.6,0.2])
Y = sch.linkage(D.T, method='complete')
Z2 = sch.dendrogram(Y)
ax2.set_xticks([])
ax2.set_yticks([])


# Plot distance matrix.
axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
idx1 = Z1['leaves']
idx2 = Z2['leaves']
D = D[idx1,:]
D = D[:,idx2]
im = axmatrix.matshow(D, aspect='auto', origin='lower')#, cmap=pylab.cm.Reds)
#pylab.pcolor(D)
#pylab.colorbar(im,shrink=0.5, pad = 0.05)#,orientation='horizontal')
# Axis Labels
#xt=sorted('Actin Ch Cofilin Gelsolin Myosin Fh2 Profilin CapA WH2 WH1 I_LWEQ Annexin RPEL Filamin Tropomyosin Vinculin ERM Fascin Thymosin Tropomodulin HS1'.split())
#print idx2
yt='Actin AIP3 WH2'.split()
yt1=[yt[i] for i in idx1]


xt='Alveolata Amoebozoa Euglenozoa Fornicata Fungi Metazoa Stramenopiles Viridiplantae'.split()
xt1=[xt[i] for i in idx2]
#print xt1

#axmatrix.invert_yaxis()
axmatrix.set_xticks(np.arange(0.1,len(idx2),1), minor=False)

axmatrix.set_yticks(np.arange(0.1,len(idx1),1), minor=False)

axmatrix.set_xticklabels(xt1,fontsize=6, rotation =90)
axmatrix.set_yticklabels(yt1,fontsize=6)
#axmatrix.set_xticks([])

# Plot colorbar.
#axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
#pylab.colorbar(im, cax=axcolor)
#fig.show()
fig.savefig('dendrogram.pdf')
fig.savefig('dendrogram.svg')

