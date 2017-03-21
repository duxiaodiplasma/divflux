import numpy as np


def main(a):
    S = a.S
    tau = a.Tau
    sig = a.data
    t = a.time
    dt = t[1]-t[0]
    a.dsigdt = np.gradient(sig,dt)
    a.sig_tau = sig/tau
    a.divf = -a.dsigdt+S-a.sig_tau
    return a

