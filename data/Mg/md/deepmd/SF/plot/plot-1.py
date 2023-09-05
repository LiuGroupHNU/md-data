#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os,sys
import numpy as np
import glob
import matplotlib.pyplot as plt
from brokenaxes import brokenaxes


# In[6]:


x1=np.loadtxt('basal.txt')
x2=np.loadtxt('prismatic.txt')
x3=np.loadtxt('pyramidalI.txt')
x4=np.loadtxt('pyramidalII.txt')
TYPE=np.loadtxt('title.txt',dtype=str)
Step=np.loadtxt('step.txt')

SF=[]

SF.append(x1)
SF.append(x2)
SF.append(x3)
SF.append(x4)


# In[13]:



plt.figure(figsize=[10,7])
for i in range(0,4):
    if len(SF[i]) < 41:
        continue
    plt.plot(Step[0:41],SF[i][0:41],label='{}'.format(TYPE[i]),marker='o',linestyle='-',linewidth=5.0,markersize=5.0 )
plt.title('SF',fontsize=20)
#plt.ylim([0,18])
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

plt.xlabel('Normalized Coordinates',fontsize=20)
plt.ylabel('SF energy, mJ/m$^{2}$',fontsize=20)
plt.legend(loc='upper right', borderaxespad=0,fontsize=20)
plt.savefig("SF-bench.jpg")


# In[ ]:




