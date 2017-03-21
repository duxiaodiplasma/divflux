import sys
sys.path.insert(0,'/home/duxiaodi/divflux/SOURCE')
import numpy as np
from scipy.io.idl import readsav
import matplotlib.pylab as plt

# PERSONAL FUNCTIONS
from gadat import *
import stau
import doplot
import read
import creatobj
import divflux

plt.close('all')

# -- GENERAL SETTING --
shot_lp= 159251
shot_hp= 159253
xr = [500,700]
wl   = np.array([6508,6532])
ptn  = ['f03_c2','f03_c4','f03_c6','f04_c1','f04_c3','f04_c5']
ch = ptn[0]

# -- LOWER POWER OBJECT --
lp = creatobj.fida(shot_lp,ch,wl,xr,'LOW POWER REFERENCE SHOT')
fp = './DATA/'+np.str(shot_lp)+'.fida'
lp = read.fidaexp(lp,fp)
lp = read.nb(lp,shot_lp)

# -- HIGH POWER OBJECT --
hp = creatobj.fida(shot_hp,ch,wl,xr,'HIGH POWER SHOT')
fp = './DATA/'+np.str(shot_hp)+'.fida'
hp = read.fidaexp(hp,fp)
hp = read.nb(hp,shot_hp)

# -- LOWER POWER SIMULATION SHOT --
lps = creatobj.fida(shot_lp,ch,wl,xr,'LOW POWER SIMULATION SHOT')
fp = './DATA/mc_fida_signal_'+np.str(shot_lp)+'L01.sav'
lps = read.fidasim(lps,fp)
lps = read.nb(lps,shot_lp)

# -- HIGH POWER SIMULATION SHOT --
hps = creatobj.fida(shot_hp,ch,wl,xr,'LOW POWER SIMULATION SHOT')
fp = './DATA/mc_fida_signal_'+np.str(shot_hp)+'L01.sav'
hps = read.fidasim(hps,fp)
hps = read.nb(hps,shot_hp)

chs = np.argmin(np.abs(lps.radius-lp.radius))
hps.ch = chs
lps.ch = chs

lp = stau.main(lp)
lps = stau.main(lps)
hp = stau.main(hp)
hps = stau.main(hps)

fp = 'dummy.ps'
out = doplot.compare(lp,lps,fp)

S = hps.condS*(lp.condS/lps.condS)
Tau = hps.condTau*(lp.condTau/lps.condTau)
res = creatobj.div(hp.shot,hp.radius,S,Tau,hp.ntime[0],hp.conddata)

res = divflux.main(res)

tmp = doplot.divflux(res)
#
#
#
#
#

#
#
#
