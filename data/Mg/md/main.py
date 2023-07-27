
from plot_cmp import plot_all

dirs = [
    './deepmd/SF/plot/',
    './nvnmd/SF/plot/'
]
labels = ['MLMD', 'NVNMD']

# dirs = [
#     '/home/mph/WorkSpace/nvnmd/benchmark/ws-MgZnY/ws-1/md1/ref/SF/plot/',
#     '/home/mph/WorkSpace/nvnmd/benchmark/ws-MgZnY/ws-1/md1/deepmd/SF/plot/',
#     '/home/mph/WorkSpace/nvnmd/benchmark/ws-MgZnY/ws-0/md1/nvnmd/SF/plot/'
# ]
# labels = ["DP Bigger Net", 'DP','NVNMD']

plot_all(dirs, labels)
