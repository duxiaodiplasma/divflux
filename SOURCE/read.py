from scipy.io.idl import readsav
import numpy as np
import savitzky_golay
from gadat import *

def fidaexp(obj,fn):
    fidafile   = readsav(fn)['data']
    fd = get_fida(fidafile,obj)
    time = fd['t_sig']
    data   = fd['sig']
    radius  = fd['radius']

    obj.time = time
    obj.data = data
    obj.radius = radius

    return obj

def fidasim(obj,fn):
    fidafile = readsav(fn)
    t_sig = fidafile['times']*1e3
    sig = fidafile['signal1']+fidafile['signal2']
    radius = fidafile['radius']/1e2
    obj.time = t_sig
    obj.data = sig
    obj.radius = radius
    return obj


def nb(obj,shot):

    nb = gadat("PINJ",shot)
    mask = np.where((nb.xdata>obj.tr[0]) & (nb.xdata<obj.tr[1]))
    nbpwr = nb.zdata[mask]
    t_nb = nb.xdata[mask]
    t_period = NBI_period(t_nb,nbpwr)
    t_period = np.fix(t_period)

    obj.period = t_period
    obj.t_nb = t_nb
    obj.nb = nbpwr

    return obj



def NBI_period(t_nb,nb):
    """FIND TIME WINDOW FOR CONDI.AVERAGE"""
    nb_mean = (np.max(nb)+np.min(nb))/2.
    mask_low  = np.where(nb<nb_mean)[0]
    index = np.where(np.diff(mask_low)>1)[0]

    return t_nb[mask_low[index]+1]



def get_fida(fida,obj):

    ch = obj.ch
    wr = obj.wavelength
    xr = obj.tr

    """READ FIDA DATA ch by ch"""
    time = fida[ch][0].DATATIME[0]
    data = fida[ch][0].DATA[0]
    wl   = fida[ch][0].WAVELENGTH[0]
    radius = fida[ch][0].radius[0]
    mask_wl = np.where((wl>wr[0]) & (wl<wr[1]))[0]
    mask_t = np.where((time>xr[0]) & (time<xr[1]))[0]

    sig = np.mean(data[:,mask_wl],axis=1)
    sig_smooth = savitzky_golay.main(sig,11,3)

    sig = np.copy(sig[mask_t])
    t_sig = np.copy(time[mask_t])
    sig_smooth = np.copy(sig_smooth[mask_t])
    radius = np.copy(radius)

    return{
           'sig':sig,
           't_sig':t_sig,
           'sig_smooth':sig_smooth,
           'radius':radius,
            }

