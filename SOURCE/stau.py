import numpy as np
from scipy import signal
from scipy.optimize import curve_fit
from obspy.signal import detrend

def cond_reshape(time,data,t_period):
    """RESHAPE DATA FOR CONDI.AVERAGE"""
    mask = np.where((time>t_period[0]) & (time<t_period[1]))[0]
    num = len(mask)
    d = np.zeros((len(t_period)-1,len(mask)))
    t = np.copy(d)
    nt = np.copy(d)
    gn = len(t_period)-1
    for i in range(0,len(t_period)-1):
        mask = np.where(time>t_period[i])[0]
        d[i,:] = signal.detrend(data[mask[0]:mask[0]+num],type='constant')
        t[i,:] = time[mask[0]:mask[0]+num]
        nt[i,:] = t[i,:]-t_period[i]

    return {
            't':t,
            'd':d,
            'nt':nt,
            'gn':gn,
            }

def model_eq(t,S,tau):
    """MODEL EQUATION"""
    b = np.exp(-0.5*54/tau)
    return np.piecewise(
            t,
            [(t<27),(t>=27)],
            [lambda t: S*tau+(-1.*b*(2*S*tau*(1-b)/b/(1-b**2)))*np.exp(-1.*t/tau), \
             lambda t: -1.*S*tau+(2*S*tau*(1-b)/b/(1-b**2))*np.exp(-1.*t/tau)]
            )

def main(obj):

    t_period = obj.period
    t_sig = obj.time

    try:
       ch = int(obj.ch)
       sig = obj.data[ch,:]

    except:
       sig = obj.data


    # detrending signal
    de_sig = np.copy(sig)

    # detrended by polynominal function
    de_sig = detrend.polynomial(de_sig,order=3)

    # conditioning process
    condi_sig = cond_reshape(t_sig,de_sig,t_period)

    # normalized time
    nt = condi_sig['nt']

    # data,time
    d = condi_sig['d']
    t = condi_sig['t']

    # DATA FITTING
    gn = condi_sig['gn']
    coeff = np.zeros((gn,2))
    sig_fit = np.copy(d)

    for i in range(0,gn):
        # calculate diagnostic slowing-down time and source
        coeff[i,:], pcov = \
             curve_fit(
                     model_eq, nt[i,:], d[i,:], p0=[1e13,10]
                      )
        # get fitting result
        sig_fit[i,:] = \
              model_eq(
                      nt[i,:], coeff[i,0], coeff[i,1]
                      )

    # Calculate the conditional averaged slowing-down time and source
    condi_coeff, pcov  = \
            curve_fit(
                    model_eq, nt[0,:], np.mean(d,axis=0), p0=[1e13,10]
                    )
    # Get fitting result
    condi_sig_fit = \
            model_eq(nt[0,:], condi_coeff[0], condi_coeff[1])

    obj.ddata = d
    obj.ddatafit = sig_fit
    obj.t_ddata = t


    obj.conddata = np.mean(sig_fit,axis=0)
    obj.condfit = condi_sig_fit
    obj.ntime = nt

    obj.S = coeff[:,0]
    obj.Tau = coeff[:,1]

    obj.condS = condi_coeff[0]
    obj.condTau = condi_coeff[1]

    obj.gn = gn


    return obj

