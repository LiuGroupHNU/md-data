#!/usr/bin/env python
# coding: utf-8

import numpy as np
import glob
import os
import matplotlib.pyplot as plt

plt.rc('font', family='Arial')
plt.rcParams.update({'font.size': 24})
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

def plots(dat_dir, key):
    """ all data in dat_dir are ploted at two images:
    1. all lines
    2. mean line with error bar
    """
    ### Get data and plot All
    print(key)
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    plt.subplots(dpi=150)
    names=locals()
    names["flow_stress_collect"]=[]
    ct = 0
    for idx, i in enumerate(sorted(glob.glob(dat_dir))):
        i = i.replace("\\","/")
        i = i.replace("strainstress.log","")
        ct += 1
        num = i.split("/")[-2]
        # data
        names["true_strain_"+num] = np.loadtxt(i+"strainstress.log", dtype=float, skiprows=0, usecols=(2), comments='#')
        names["stress_"+num] = np.loadtxt(i+"strainstress.log", dtype=float, skiprows=0, usecols=(3), comments='#')
        # plot
        plt.plot(names["true_strain_"+num], -names["stress_"+num], label = "Sample " + num, color=colors[idx])
        # 0.07 to 0.10
        ii = np.where(names["true_strain_"+num] > 0.07) 
        jj = np.where(names["true_strain_"+num] < 0.10)
        idx_7 = ii[0][0]
        idx_10 = jj[0][-1]
        # avg and std
        names["flow_stress"+num] = -np.average(names["stress_"+num][idx_7:idx_10])
        names["flow_stress_std"+num] = np.std(names["stress_"+num][idx_7:idx_10])
        # print
        print("flow stress [sample",num,"]",names["flow_stress"+num],"    err_std [sample",num,"]:", names["flow_stress_std"+num])
        names["flow_stress_collect"].append(names["flow_stress"+num])
    # plot
    plt.xlim(0,0.1)
    plt.ylim(0,2.5)
    plt.xlabel('True strain')
    plt.ylabel('True stress (GPa)')
    plt.grid()
    plt.legend()
    # plt.savefig(key+"-all.png")
    plt.close()

    ### sample std for flow_stress
    flow_stress_samples_mean = np.mean(names["flow_stress_collect"])
    flow_stress_samples_std = np.std(names["flow_stress_collect"])
    ######### OUTPUT OF FLOW STRESS
    print("flow stress samples mean",flow_stress_samples_mean,"   flow stress samples err_std",flow_stress_samples_std)
    
    ### stress curve average
    for ii in range(ct):
        starin_i = names["true_strain_%d"%(ii+1)]
        stress_i = names["stress_%d"%(ii+1)]
        if ii == 0:
            strain_ave = starin_i
            stress_ave = stress_i
        else:
            strain_ave += starin_i
            stress_ave += stress_i
    strain_ave /= ct
    stress_ave /= ct
    names["true_strain_ave"] = strain_ave
    names["stress_ave"] = stress_ave

    ### plot error bar
    names["stress_std"]=[]
    for idx,v in enumerate(names["stress_ave"]):
        stds = [names["stress_%d"%(ii+1)][idx] for ii in range(ct)]
        std=np.std(stds)
        names["stress_std"].append(std)

    plt.subplots(dpi=150) #mean curve with errbar
    plt.plot(names["true_strain_ave"],-names["stress_ave"],label=key,color="black")
    # plt.plot(names["true_strain_ave"],-names["stress_ave"],label=key+" samples mean",color="black")
    plt.errorbar(x=names["true_strain_ave"],y=-names["stress_ave"],yerr=[names["stress_std"],names["stress_std"]],color="pink",alpha=0.3)
    plt.xlim(0,0.1)
    plt.ylim(0,2.5)
    plt.grid()
    plt.xlabel('True strain')
    plt.ylabel('True stress (GPa)')
    plt.legend()
    # plt.savefig(key+"-mean.png")
    plt.close()
    #
    return [names["true_strain_ave"], -names["stress_ave"], [names["stress_std"], names["stress_std"]]]


def plot_cmp(dirs, labels):
    data = []
    for ii in range(len(dirs)):
        dat = plots(dirs[ii], labels[ii])
        data.append(dat)
    #
    fig = plt.figure(figsize=[4*1.6, 3*1.6])
    ax1 = plt.axes([0.16, 0.16, 0.80, 0.80])
    colors = [[0.12, 0.6, 0.6], [0.9, 0.18, 0.396], [0.18, 0.396, 0.9]]
    # colors = ['r', 'g', 'b', 'm', 'k']
    for ii in range(len(dirs)):
        x, y, z = data[ii]
        x *= 100
        plt.plot(x, y, label=labels[ii], color=colors[ii])
        plt.errorbar(x, y, yerr=z, color=colors[ii], alpha=0.1)
    # plt.xlim(0, 0.1)
    plt.xlim(0, 10)
    plt.ylim(0, 2.5)
    plt.grid(which='both', linestyle='--', color=[0.9, 0.9, 0.9])
    # plt.xlabel('True strain')
    plt.xlabel('Strain (%)')
    plt.ylabel('Stress (GPa)')
    plt.legend(frameon=False, markerscale=2, handlelength=1, handletextpad=1, loc="upper center", ncol=2)
    # opt plot
    plt.tick_params(length=4, width=2, which="major", top='on', right='on')
    plt.tick_params(length=3, width=1, which="minor", top='on', right='on')
    for d in ['top', 'bottom', 'left', 'right']: plt.gca().spines[d].set_linewidth(2)

    plt.savefig("img.png")
    plt.show()
    plt.close()


