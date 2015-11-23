#!/usr/bin/env python

import numpy as np
import sys, re, math
import matplotlib.pyplot as plt
import pylab as pylab
import scipy.ndimage as ndimage


def main():
	# Reading data file
	x, y = read_data_file(sys.argv[1])
	
	#Start frame index for density; example "start = 5" means first 5 frame will be discarded
	start = 5

	# Limit of the x and yaxis in plots
	ylim = [0.1, 0.4]
	xlim = [2.34, 2.44]

	# Generating 2D probablity density plot
	hist, extent = make_histogram2d(x[start:], y[start:], xbin=20, ybin=10)

	# Plotting 2D density
	plot_density2d(hist, extent, xlim, ylim, xlabel='Rg (nm)', ylabel='RMSD (nm)', cmap='brg')
	
	# Plotting energy
	plot_energy2d(hist, extent, xlim, ylim, xlabel='Rg (nm)', ylabel='RMSD (nm)', cmap='brg')

def plot_energy2d(hist, extent, xlim, ylim, xlabel, ylabel, cmap='brg'):
	fig = plt.figure()
	plt.subplots_adjust(bottom=0.15, right=1, left=0.15)

	log_z = masked_log_zero(hist)
	
	#Smoothing of histogram
	#z = ndimage.gaussian_filter(log_z, sigma=0.2, order=0)

	masked_hist = np.multiply(log_z, -2.5)
	masked_hist = np.subtract(masked_hist, np.amin(masked_hist)-0.001)
	
	#Plotting contour
	CS = plt.contour(masked_hist, extent=extent, linewidths=1, ls='solid', colors='k', zorder=1000)
	CS = plt.contourf(masked_hist, extent=extent, cmap=cmap, ls='solid')
	
	# Inline contour label
	#P.clabel(CS,inline=1,fmt='%1.1f',fontsize=16,fontname="Times new roman")

	plt.tick_params(axis='both',which='major',width=2,length=15)
	plt.tick_params(axis='both',which='minor',width=2,length=10)
	plt.xlabel(xlabel,fontsize="24", fontname="Times new roman")
	plt.ylabel(ylabel, fontsize="24", fontname = "Times new roman")
	ax = plt.gca()
	plt.xticks(ax.get_xticks()[::2], fontsize="24", fontname = "Times new roman")
	plt.yticks(ax.get_yticks(), fontsize="24", fontname = "Times new roman")
	plt.xlim(extent[0],extent[1])	
	plt.ylim(extent[2],extent[3])
	
	# Color bar
	cb = plt.colorbar()	
	cb_yticks = plt.getp(cb.ax.axes, 'yticklabels')
	plt.setp(cb_yticks, fontsize=24, fontname = "times new roman")
	
	# Saving plot as a figure
	plt.savefig('{0}_energy.png' .format(sys.argv[2]),orientation='landscape',dpi=300, papertype='a4',)

def masked_log_zero(x):
	log_x = []
	for i in range(len(x)):
		temp_r = []
		for j in range(len(x[i])):
			if x[i][j] != 0:
				temp_r.append(math.log(x[i][j]))
			else:
				temp_r.append(0.0)
		log_x.append(temp_r)
	return np.array(log_x)
				

def plot_density2d(hist, extent, xlim, ylim, xlabel, ylabel, cmap='brg'):
	fig = plt.figure()
	plt.subplots_adjust(bottom=0.15, right=1, left=0.15)
	
	#Smoothing of histogram
	#z = ndimage.gaussian_filter(hist, sigma=0.8, order=0)

	#Plotting contour
	CS = plt.contour(hist, extent=extent, linewidths=1,colors='k', zorder=1000)
	CS = plt.contourf(hist, extent=extent, cmap=cmap)
	
	# Inline contour label
	#P.clabel(CS,inline=1,fmt='%1.1f',fontsize=16,fontname="Times new roman")

	plt.tick_params(axis='both',which='major',width=2,length=15)
	plt.tick_params(axis='both',which='minor',width=2,length=10)
	plt.xlabel(xlabel,fontsize="24", fontname="Times new roman")
	plt.ylabel(ylabel, fontsize="24", fontname = "Times new roman")
	ax = plt.gca()
	plt.xticks(ax.get_xticks()[::2], fontsize="24", fontname = "Times new roman")
	plt.yticks(ax.get_yticks(), fontsize="24", fontname = "Times new roman")
	plt.xlim(extent[0],extent[1])	
	plt.ylim(extent[2],extent[3])
	cb = plt.colorbar()	
	
	# Color bar
	cb_yticks = plt.getp(cb.ax.axes, 'yticklabels')
	plt.setp(cb_yticks, fontsize=24, fontname = "times new roman")
	
	plt.savefig('{0}_density.png' .format(sys.argv[2]),orientation='landscape',dpi=300, papertype='a4')
	#plt.show()

def make_histogram2d(x,y,xbin=40,ybin=50):
	hist, xedges, yedges = np.histogram2d(y,x,bins=(xbin,ybin),normed=True)
	extent = [yedges[0], yedges[-1], xedges[0], xedges[-1]]
	return hist, extent

def read_data_file(FileName,cols_equal=True):
	infile = open(FileName,'r')
	data = []
	len_data = 0 
	i=1 
	for line in infile:
		line = line.rstrip('\n')
		if not line.strip():
			continue
		if(re.match('#|@',line)==None):
			temp = map(float,line.split())
			if(cols_equal):
				if (i==1):
					len_data = len(temp)
				if (len(temp) != len_data):
					print 'WARNING: Number of column mis match at line {0} in {1}; skipping remaining part\n' .format(i,FileName)
					break
				data.append(temp)
			i = i+1 
	data = np.array(data).T
	return data


if __name__ == "__main__":
	main()
