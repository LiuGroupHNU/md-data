#!/usr/bin/env python
# coding: utf-8


import os,sys
import numpy as np
import glob
import copy
import matplotlib as mpl
import matplotlib.pyplot as plt
from skimage.transform import resize

plt.rc('font', family='Arial')
plt.rcParams.update({'font.size': 24})
# plt.rcParams['xtick.direction'] = 'in'
# plt.rcParams['ytick.direction'] = 'in'


def plot_rdf(dir):
    cs = [[0.12, 0.6, 0.6], [0.9, 0.18, 0.396], [0.18, 0.396, 0.9]]
    d1 = np.loadtxt(dir + '/aimd/rdf/total.txt')
    d2 = np.loadtxt(dir + '/deepmd/rdf/total.txt')
    d3 = np.loadtxt(dir + '/this_work/rdf/total.txt')
    plt.figure()
    ax1 = plt.axes([0.15, 0.15, 0.8, 0.8])
    ax1.plot(d1[:, 0], d1[:, 1], '-' , c=cs[0], label='AIMD', linewidth=8)
    ax1.plot(d2[:, 0], d2[:, 1], '-' , c=cs[1], label='MLMD', linewidth=4)
    ax1.plot(d3[:, 0], d3[:, 1], '--', c=cs[2], label='this_work', linewidth=2)
    plt.xlabel('${\it r} \quad ({\AA})$')
    plt.ylabel('${\it g}({\it r})$')
    plt.xlim([2, 8])
    plt.ylim([0, 4])
    plt.xticks([2, 3, 4, 5, 6, 7, 8], [2, 3, 4, 5, 6, 7, 8])
    plt.yticks([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
    plt.legend()
    plt.grid()
    plt.savefig(dir+"/rdf.png")
    # plt.show()
    plt.close()

def plot_adf(dir):
    cs = [[0.12, 0.6, 0.6], [0.9, 0.18, 0.396], [0.18, 0.396, 0.9]]
    d1 = np.loadtxt(dir+'/aimd/adf/total.txt')
    d2 = np.loadtxt(dir+'/deepmd/adf/total.txt')
    d3 = np.loadtxt(dir+'/this_work/adf/total.txt')
    plt.figure()
    ax1 = plt.axes([0.15, 0.15, 0.8, 0.8])
    ax1.plot(d1[:, 0], d1[:, 1], '-' , c=cs[0], label='AIMD', linewidth=8)
    ax1.plot(d2[:, 0], d2[:, 1], '-' , c=cs[1], label='MLMD', linewidth=4)
    ax1.plot(d3[:, 0], d3[:, 1], '--', c=cs[2], label='this_work', linewidth=2)
    plt.xlabel(r'${\it \theta} \quad ({\degree})$')
    plt.ylabel('Distribution (%)')
    plt.xlim([0, 180])
    plt.ylim([0, 4])
    plt.xticks([30, 60, 90, 120, 150, 180], [30, 60, 90, 120, 150, 180])
    plt.yticks([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
    plt.legend()
    plt.grid()
    plt.savefig(dir+"/adf.png")
    # plt.show()
    plt.close()

def plot_cn(dir):
    cs = [[0.12, 0.6, 0.6], [0.9, 0.18, 0.396], [0.18, 0.396, 0.9]]
    d1 = np.loadtxt(dir + '/aimd/cn/total.txt')
    d2 = np.loadtxt(dir + '/deepmd/cn/total.txt')
    d3 = np.loadtxt(dir + '/this_work/cn/total.txt')
    d1 = d1[:,1] / np.sum(d1[:,1]) * 100
    d2 = d2[:,1] / np.sum(d2[:,1]) * 100
    d3 = d3[:,1] / np.sum(d3[:,1]) * 100
    width = 0.3
    x = np.arange(len(d1))
    plt.figure()
    ax1 = plt.axes([0.15, 0.15, 0.8, 0.8])
    ax1.bar(x+0*width, d1, width, color=cs[0], label='AIMD')
    ax1.bar(x+1*width, d2, width, color=cs[1], label='MLMD')
    ax1.bar(x+2*width, d3, width, color=cs[2], label='this_work')
    plt.xlabel('Coordination Number')
    plt.ylabel('Distribution (%)')
    plt.xlim([1.5, 7.5])
    plt.ylim([0, 50])
    plt.xticks([2, 3, 4, 5, 6], [2, 3, 4, 5, 6])
    # plt.yticks([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
    plt.legend()
    plt.grid()
    plt.savefig(dir+"/cn.png")
    # plt.show()
    plt.close()

def load_altbc(_dir):
    d = [
        np.loadtxt(_dir+'/altbc/x.txt'),
        np.loadtxt(_dir+'/altbc/y.txt'),
        np.loadtxt(_dir+'/altbc/z.txt')
    ]
    return d

def sub_plot_altbc(dd, ax):
    x, y, z = dd[0], dd[1], dd[2]
    z = z / np.max(z)
    k = 10
    xx = np.linspace(np.min(x), np.max(x), len(z[0,:]) * k)
    yy = np.linspace(np.min(y), np.max(y), len(z[:,0]) * k)
    zz = resize(z, np.array(np.shape(z)) * k)
    ax.pcolor(xx, yy, zz, cmap='jet')

def plot_altbc(dir, idx=[0, 1, 2], dirs=['aimd', 'deepmd', 'this_work']):
    ds = []
    for d in dirs:
        ds.append(load_altbc(dir+'/'+d))
    labs = ['AIMD', 'MLMD', 'this_work']
    #
    n = len(idx)
    fig = plt.figure(figsize=[4*1.2*n, 3*1.6])
    tik = [2.5, 3.0, 3.5, 4.0]
    for i in range(n):
        ii = idx[i]
        ax1 = plt.axes([0.08+0.28*ii, 0.20, 0.25, 0.76])
        sub_plot_altbc(ds[i], ax1)
        ax1.set_xlabel(r'${\it r}_{\rm 1} \enspace {\rm (\AA)} $')
        if (ii==0):
            ax1.set_ylabel(r'${\it r}_{\rm 2} \enspace {\rm (\AA)}$')
            ax1.yaxis.set_ticks(tik)
        else:
            ax1.yaxis.set_ticks(tik, [])
        ax1.xaxis.set_ticks(tik)
        # opt plot
        plt.tick_params(pad=8)
        plt.tick_params(length=4, width=2, which="major", top='on', right='on')
        plt.tick_params(length=3, width=1, which="minor", top='on', right='on')
        for d in ['top', 'bottom', 'left', 'right']: plt.gca().spines[d].set_linewidth(2)

    # plt.colorbar()
    #*https://blog.csdn.net/weixin_43257735/article/details/121831188
    cmap1 = copy.copy(mpl.cm.jet)
    norm1 = mpl.colors.Normalize(vmin=0, vmax=1)
    im1 = mpl.cm.ScalarMappable(norm=norm1, cmap=cmap1)
    ax1 = plt.axes([0.08+0.28*n, 0.20, 0.01, 0.76])
    cbar1 = fig.colorbar(
        im1, cax=ax1, orientation='vertical',
        ticks = np.linspace(0, 1, 6), label = '')
    plt.savefig(dir+"/altbc.png")
    # plt.show()
    plt.close()

def plot_altbc_one(dir):
    d = load_altbc(dir)
    #
    fig = plt.figure(figsize=[4*1.6, 3*1.6])
    ax1 = plt.axes([0.19, 0.20, 0.65, 0.76])
    tik = [2.5, 3.0, 3.5, 4.0]
    sub_plot_altbc(d, ax1)
    ax1.set_xlabel(r'${\it r}_{\rm 1} \enspace {\rm (\AA)} $')
    ax1.set_ylabel(r'${\it r}_{\rm 2} \enspace {\rm (\AA)}$')
    ax1.yaxis.set_ticks(tik)
    ax1.xaxis.set_ticks(tik)
    # opt plot
    plt.tick_params(pad=8)
    plt.tick_params(length=4, width=2, which="major", top='on', right='on')
    plt.tick_params(length=3, width=1, which="minor", top='on', right='on')
    for d in ['top', 'bottom', 'left', 'right']: plt.gca().spines[d].set_linewidth(2)

    # plt.colorbar()
    #*https://blog.csdn.net/weixin_43257735/article/details/121831188
    cmap1 = copy.copy(mpl.cm.jet)
    norm1 = mpl.colors.Normalize(vmin=0, vmax=1)
    im1 = mpl.cm.ScalarMappable(norm=norm1, cmap=cmap1)
    ax1 = plt.axes([0.88, 0.20, 0.01, 0.76])
    cbar1 = fig.colorbar(
        im1, cax=ax1, orientation='vertical',
        ticks = np.linspace(0, 1, 6), label = '')
    plt.savefig(dir+"/altbc.png")
    # plt.show()
    plt.close()

