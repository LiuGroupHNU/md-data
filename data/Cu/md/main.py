
from plot_strain_stress import plot_cmp

dirs = [
    "ref/[0-9]/strainstress.log",
    "[0-9]/strainstress.log"
]

labels = ["MLMD", "this_work"]

plot_cmp(dirs, labels)
