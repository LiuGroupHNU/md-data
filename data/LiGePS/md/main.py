
import numpy as np
import matplotlib.pyplot as plt

plt.rc('font', family='Arial')
plt.rcParams.update({'font.size': 24})
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

def div(x):
    return [1000/xi for xi in x]

def load_data(fn, nt):
    lines = open(fn, 'r').readlines()
    tmp = []
    msd = []
    for line in lines:
        if line.startswith('Temp:'):
            pars = line.split()
            tmp.append(float(pars[1]))
            msd.append(float(pars[4]))
    tmp = np.array(tmp)
    tmp = np.reshape(tmp, [-1, nt])
    tmp = np.mean(tmp, axis=1)
    msd = np.array(msd)
    msd = np.reshape(msd, [-1, nt])
    return tmp, msd

def load_ref(fn):
    lines = open(fn, 'r').readlines()
    ct = -1
    xs = []
    ds = []
    for line in lines:
        if line.startswith("#"):
            xs.append([])
            ds.append([])
            ct += 1
        else:
            pars = line.split()
            xs[ct].append(float(pars[0]))
            ds[ct].append(float(pars[1]))
    return xs, ds


t, data = load_data('hist_this_work.txt', 3)
avg = np.mean(data, axis=1)
std = np.std(data, axis=1)
x = div(t)

t2, data2 = load_data('hist_dp.txt', 3)
avg2 = np.mean(data2, axis=1)
std2 = np.std(data2, axis=1)
x2 = div(t2)

xs, datas = load_ref("ref_MSD3.txt")

# plot
fig = plt.figure(figsize=[4*1.6, 3*1.6])
ax1 = plt.axes([0.21, 0.16, 0.78, 0.80])

x0 = [1000/300, 1000/400, 1000/500, 1000/666]
print(x)
print(avg)
print(std)
plt.plot(x0, datas[0], 'o-', color='orange', label="MLMD 2021")
plt.errorbar(x0, avg2, yerr=std2, fmt='bh-', capsize=6, ecolor=[0.0, 0.0, 0.8], label="MLMD")
plt.errorbar(x0, avg, yerr=std, fmt='rs-', capsize=6, ecolor=[0.8, 0.0, 0.0], label="this_work")
plt.yscale('log')
plt.xticks([1.0, 1.5, 2.0, 2.5, 3.0])
plt.grid(which='both', linestyle='--')
handles, labels = plt.gca().get_legend_handles_labels()
order = [2, 1, 0]
plt.legend([handles[idx] for idx in order], [labels[idx] for idx in order], frameon=False, markerscale=1, handlelength=0.5, handletextpad=0.5, loc="lower left", ncol=1)
# plt.legend(frameon=False, markerscale=1, handlelength=0.5, handletextpad=0.5, loc="upper right", ncol=1)
plt.ylabel("D ($\\rm m^2/s$)")
plt.xlabel("1000/T  (K)")

# opt plot
plt.tick_params(length=4, width=2, which="major", top='on', right='on')
plt.tick_params(length=3, width=1, which="minor", top='on', right='on')
for d in ['top', 'bottom', 'left', 'right']: plt.gca().spines[d].set_linewidth(2)

plt.savefig('msd.png', dpi=300)
# plt.show()
# plt.close()

