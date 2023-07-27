

import numpy as np
import matplotlib.pyplot as plt

plt.rc('font', family='Arial')
plt.rcParams.update({'font.size': 24})
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

def get_data(fn):
    data = np.loadtxt(fn, skiprows=1)
    return data


def plot(dat1, dat2):
    cs = [[0.12, 0.6, 0.6], [0.9, 0.18, 0.396]]
    p1, t1, r1 = dat1[:, 0], dat1[:, 1], dat1[:, 2]
    p2, t2, r2 = dat2[:, 0], dat2[:, 1], dat2[:, 2]
    #
    fig = plt.figure(figsize=[4*1.6, 3*1.6])
    ax1 = plt.axes([0.19, 0.16, 0.77, 0.80])
    ax1.plot(p2, t2, '-s', c=cs[0], label="MLMD", linewidth=2.5, markerfacecolor=cs[0], markersize=12)
    ax1.plot(p1, t1, '-o', c=cs[1], label="NVNMD", linewidth=2.5, markerfacecolor='w', markersize=9)
    # A/ps -> 0.1 km/s
    # 40 -> 4.0
    # 75 -> 7.5
    plt.yticks([0, 5000, 10000, 15000], ['0', '5K', '10K', '15K'])
    plt.xlabel('$\it{P}$ (GPa)')
    plt.ylabel('$\it{T}$ (K)')
    plt.grid(which='both', linestyle='--', color=[0.8, 0.8, 0.8])
    plt.legend(frameon=False, markerscale=1, handlelength=1, handletextpad=0.5, loc="upper left", ncol=1, columnspacing=0.5)
    # opt plot
    plt.tick_params(length=4, width=2, which="major", top='on', right='on')
    plt.tick_params(length=3, width=1, which="minor", top='on', right='on')
    for d in ['top', 'bottom', 'left', 'right']: plt.gca().spines[d].set_linewidth(2)

    plt.savefig('eos_pt.png')
    # plt.show()
    plt.close()
    #
    fig = plt.figure(figsize=[4*1.6, 3*1.6])
    ax1 = plt.axes([0.19, 0.16, 0.77, 0.80])
    ax1.plot(p2, r2, '-s', c=cs[0], label="MLMD", linewidth=2.5, markerfacecolor=cs[0], markersize=12)
    ax1.plot(p1, r1, '-o', c=cs[1], label="NVNMD", linewidth=2.5, markerfacecolor='w', markersize=9)
    plt.xlabel('$\it{P}$ (GPa)')
    plt.ylabel('$\it \\rho$ (g/m$^3$)')
    # plt.legend(frameon=False, markerscale=1, handlelength=1, handletextpad=0.5, loc="upper center", ncol=2, columnspacing=0.5)
    plt.grid(which='both', linestyle='--', color=[0.8, 0.8, 0.8])
    # opt plot
    plt.tick_params(length=4, width=2, which="major", top='on', right='on')
    plt.tick_params(length=3, width=1, which="minor", top='on', right='on')
    for d in ['top', 'bottom', 'left', 'right']: plt.gca().spines[d].set_linewidth(2)

    plt.savefig('eos_pr.png')
    # plt.show()
    plt.close()

