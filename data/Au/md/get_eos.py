import sys
import os
import numpy as np

def msstData(filename):
    data = np.loadtxt(filename,skiprows=1)
    #[time,temp,rho,vol,pzz,tau tauvm dhug dray lgr_vel lgr_pos msst]
    TimeData = {'time': data[:,0],       \
                'temp': data[:,1],       \
                'rho' : data[:,2],       \
                'vol' : data[:,3],       \
                'pzz' : data[:,4]/1e4,   \
                'tau' : data[:,5]/1e4,   \
                'tauvm' : data[:,6]/1e4, \
                'dhug' : data[:,7]/1e4,  \
                'dray' : data[:,8],      \
                'up' : data[:,9],        \
                'pos' : data[:,10],      \
                'Emsst' : data[:,11]     \
                }
    
    cols = len(TimeData['time'])
    Nstat = round(2*cols/3)

    aveData = { 'temp': np.mean(np.array(data[Nstat:,1])),       \
                'rho' : np.mean(np.array(data[Nstat:,2])),       \
                'vol' : np.mean(np.array(data[Nstat:,3])),       \
                'pzz' : np.mean(np.array(data[Nstat:,4]))/1e4,   \
                'tau' : np.mean(np.array(data[Nstat:,5]))/1e4,   \
                'tauvm' : np.mean(np.array(data[Nstat:,6]))/1e4, \
                'dhug' : np.mean(np.array(data[Nstat:,7]))/1e4,  \
                'dray' : np.mean(np.array(data[Nstat:,8])),      \
                'up' : np.mean(np.array(data[Nstat:,9])),        \
                'pos' : np.mean(np.array(data[Nstat:,10])),      \
                'Emsst' : np.mean(np.array(data[Nstat:,11]))     \
                }

    return TimeData,aveData


def get_eos(dataPATH='./'):
    """ 获取状态方程
    """
    us = np.arange(40,75+5,5)
    outputfile = dataPATH+'/EOS.dat'
    with open(outputfile, "w") as f:
        f.write('# pzz temp rho vol up\n')
        # f.write('# pzz temp rho vol up\r\n')
    for i in range(0,len(us)):
        TimeData,aveData=msstData(dataPATH + 'output_' + str(us[i]) + '.txt')
        avePress = aveData['pzz']
        avetemp = aveData['temp']
        averho = aveData['rho']
        avevol = aveData['vol']
        aveup = aveData['up']
        with open(outputfile, "a") as f:
            f.write('%f %f %f %f %f \n' %(avePress,avetemp,averho,avevol,aveup))
            # f.write('%f %f %f %f %f\r\n' %(avePress,avetemp,averho,avevol,aveup))

