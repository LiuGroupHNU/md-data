#!/usr/bin/env python
# coding: utf-8


import os,sys
import numpy as np
import glob
import matplotlib.pyplot as plt

plt.rc('font', family='Arial')
plt.rcParams.update({'font.size': 24})
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


def load_data(path):
    x1=np.loadtxt(path+'basal.txt')
    x2=np.loadtxt(path+'prismatic.txt')
    x3=np.loadtxt(path+'pyramidalI.txt')
    x4=np.loadtxt(path+'pyramidalII.txt')
    TYPE=np.loadtxt(path+'title.txt',dtype=str)
    Step=np.loadtxt(path+'step.txt')

    SF=[]
    SF.append(x1)
    SF.append(x2)
    SF.append(x3)
    SF.append(x4)

    return TYPE, Step, SF

def plot_all(dirs, labels):
    n = len(dirs)
    cs = [[0.12, 0.6 , 0.6 ], [0.9, 0.18 , 0.396], 'green', 'red', 'blue']
    ms = ['','','']
    lss = ['-', '--',':']
    lws = [5.0, 2.5, 2.5]
    mss = [5.0, 2.5, 2.5]
    #
    datas = []
    for ii in range(n):
        TYPE1, Step1, SF1 = load_data(dirs[ii])
        datas.append([TYPE1, Step1, SF1])

    for ii in range(4):
        fig = plt.figure(figsize=[4*1.2, 4*1.2])
        ax1 = plt.axes([0.16, 0.16, 0.80, 0.80])
        for jj in range(n):
            data = datas[jj]
            TYPE, Step, SF = data
            if len(SF[ii]) < 41:
                continue
            #
            plt.plot(Step[0:41], SF[ii][0:41], color=cs[jj], label=labels[jj], 
                marker=ms[jj], linestyle=lss[jj], linewidth=lws[jj], markersize=mss[jj])
        #
        plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        if np.max(SF[ii][0:41]) > 250:
            plt.ylim([0, 500])
            plt.yticks([0, 100, 200, 300, 400, 500])
        else:
            plt.ylim([0, 250])
            plt.yticks([0, 50, 100, 150, 200, 250])
        plt.grid()

        plt.xlabel('Normalized Coordinates')
        # plt.ylabel('Stacking Fault Energy (mJ/m$^{2}$)')
        if ii == 1:
            # plt.legend(borderaxespad=0)
            plt.legend(frameon=False, markerscale=2, handlelength=1, handletextpad=1, loc="lower center")
        # opt plot
        plt.tick_params(length=4, width=2, which="major", top='on', right='on')
        plt.tick_params(length=3, width=1, which="minor", top='on', right='on')
        for d in ['top', 'bottom', 'left', 'right']: plt.gca().spines[d].set_linewidth(2)
        plt.savefig("%s.png"%TYPE[ii])
        plt.close()


