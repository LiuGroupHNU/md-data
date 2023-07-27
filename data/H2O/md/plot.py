
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.colors as cs

plt.rc('font', family='Arial')
plt.rcParams.update({'font.size': 24})
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

def load_data(fn):
    lines = open(fn,'r').readlines()
    lines = lines[4:]
    lines = [line.replace('\n','') for line in lines]
    datas = []
    for ii in range(len(lines)):
        data = [float(p) for p in lines[ii].split()]
        datas.append(data)
    datas = np.array(datas)
    return datas 

def read_rdf_data(file):
    with open(file) as fp: 
        x = []
        y = []
        z = []
        w = []
        lines = fp.readlines()
        for line in lines:
            line = line.strip('\n')
            line = line.split(' ')
            if (len(line) == 8):
                x.append(float(line[1]))
                y.append(float(line[2]))
                z.append(float(line[4]))
                w.append(float(line[6]))
        # d = [x, y, z, w]
        d = [x, w, z, y]
        d = np.array(d)
        d = np.reshape(d, [4, -1, 500])
        d = np.mean(d, axis=1)
        d = d.T
        idx = np.argsort(d[:,0])
        d = d[idx]
        return d

def plot_one():
    d = load_data('tmp.rdf')
    # print(d)

    shx = 2
    labels = ['H-H','H-O','O-O']
    for ii in range(3):
        i = shx + ii*2
        plt.plot(d[:,1], d[:,i]/2, label=labels[ii])

    plt.grid()
    plt.legend()
    plt.ylim([0, 4])
    plt.savefig('rdf.png')
    # plt.show()

def plot_all(n, fn, load_aimd, load_mlmd):
    # aimd
    dirs = ["rdf.hh.dft", "rdf.oh.dft", "rdf.oo.dft"]
    # this_work
    ds = []
    for ii in range(n):
        ds.append(load_data('ws%d/tmp.rdf'%(ii+1)))
    # plot this_work
    shx = 2
    idxs = [2, 1, 0]
    labels = ['HH','HO','OO']
    fig = plt.figure(figsize=[4*1.6, 3*1.6])
    for ii in range(3):
        ax1 = plt.axes([0.15, 0.17+0.28*ii, 0.8, 0.25])
        # AIMD
        if load_aimd:
            d = np.loadtxt("ref/"+dirs[ii])
            x = d[:,0] * 10
            y = d[:,1]
            c = cs.hsv_to_rgb([0.5, 0.8, 0.6])
            label = "AIMD" if ii == 2 else None
            ax1.plot(x, y, '-', color=c, label=label, linewidth=5)
        # MLMD
        if load_mlmd:
            # d = np.loadtxt("ref2/"+dirs[ii])
            d = read_rdf_data("ref-ldh/rdf/water-double.rdf")
            x = d[:,0]
            y = d[:,ii+1]
            c = cs.hsv_to_rgb([0.7, 0.8, 0.6])
            # print(x, y)
            label = "MLMD" if ii == 1 else None
            ax1.plot(x, y, '--', color=c, label=label, linewidth=5)
        # this_work
        i = shx + idxs[ii]*2
        x = ds[0][:,1]
        y = [d[:,i]/2 for d in ds]
        y = np.reshape(y, [n, -1])
        y = np.mean(y, axis=0)
        c = cs.hsv_to_rgb([0.95, 0.8, 0.9])
        label = "this_work" if ii == 0 else None
        ax1.plot(x, y, ':', color=c, label=label, linewidth=2.5)
        #
        plt.legend(frameon=False, markerscale=2, handlelength=2, handletextpad=1, loc="upper right", ncol=2, columnspacing=0.5)
        if (ii == 0):
            ax1.set_xlabel(r'${\it r} \rm \enspace (Å)$', labelpad=0.0)
        else:
            ax1.xaxis.set_ticks([0, 1, 2, 3, 4, 5, 6], [])
        ax1.grid()
        ax1.set(xlim=[0, 6], ylim=[0, 4])
        ax1.set_ylabel(r"${\it g}_{\rm %s} {\rm (} {\it r} {\rm )}$" % labels[ii])
        # opt plot
        plt.tick_params(length=4, width=2, which="major", top='on', right='on')
        plt.tick_params(length=3, width=1, which="minor", top='on', right='on')
        for d in ['top', 'bottom', 'left', 'right']: plt.gca().spines[d].set_linewidth(2)

    plt.savefig(fn)
    plt.close()

import sys
if __name__ == "__main__":
    argvs = sys.argv[1:]
    if len(argvs) == 0:
        plot_one(0)
    if len(argvs) == 1:
        plot_all(int(argvs[0]))