
from get_eos import get_eos
from plot_eos import get_data, plot

get_eos('ws/')

dat1 = get_data('ws/EOS.dat')
dat2 = get_data('ref/EOS.dat')
plot(dat1, dat2)
