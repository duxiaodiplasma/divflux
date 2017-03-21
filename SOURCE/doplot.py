import numpy as np
import matplotlib
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
import savitzky_golay


def fitting(a,t_nb,nb,radius,wl,fn='dummy.pdf'):
    """PLOT FITTING DETAILS"""
    plt.rcParams['figure.figsize'] = (8,8)
    fig = plt.figure(1,figsize=(8,8))
    gs = gridspec.GridSpec(100,100)
    ax1 = plt.subplot(gs[20:50,10:45])
    ax1_1 = ax1.twinx()
    ax2 = plt.subplot(gs[20:50,50:90])
    ax3 = plt.subplot(gs[53:90,10:45])
    ax4 = plt.subplot(gs[53:90,50:90])
    ax4_1 = ax4.twinx()

    ax1.plot(a['t_sig'],a['sig'])
    ax1_1.plot(t_nb,nb,color='blue',alpha=0.2)

    for i in range(0,a['d'].shape[0]):
        ax2.plot(a['t'][i,:],a['d'][i,:],alpha=0.5)
        ax3.plot(a['nt'][i,:],a['d'][i,:],alpha=0.5)
    ax3.scatter(a['nt'][0,:],np.mean(a['d'],axis=0),marker='x',s=50,linewidth=2,color='black')
    ax3.plot(a['nt'][0,:],a['condi_sig_fit'])

    gn = a['gn']
    coeff=a['coeff']
    condi_coeff=a['condi_coeff']
    for i in range(0,gn):
        ax2.plot(a['t'][i,:],a['sig_fit'][i,:])

    ax4.scatter(np.arange(gn),coeff[:,1],color='r',s=50)
    ax4.plot([0,6],[condi_coeff[1],condi_coeff[1]],color='r')
    ax4_1.scatter(np.arange(gn),coeff[:,0],marker='x',s=50,color='black')
    ax4_1.plot([0,6],[condi_coeff[0],condi_coeff[0]],color='black')
    ax4.set_yscale('log')
    ax4.set_ylim(1e0,1e3)
    ax4_1.set_yscale('log')
    ax4_1.set_ylim(1e10,1e15)
    ax4.set_ylabel('$\\tau [ms]$ (red)')
    ax4_1.set_ylabel('$\\tilde S_0 [a.u.]$ (black)')
    ax4.set_xlabel('PERIODS')
    ax2.set_xlabel('TIME[S]')

    ax3.set_xlabel('RELATIVE TIME[ms]')
    ax3.set_ylabel('MODULATED FIDA[a.u.]')
    ax1.set_xlabel('TIME [s]')
    ax1.set_ylabel('FIDA INTENSITY')
    ax1_1.set_ylabel('$P_{NBI} [kW]$')

    import time
    comment0 = 'INTEPRETATION OF NBI MODULATION FOR FIDA BY X.D.DU'
    comment1 =  time.strftime("%c")
    comment2 = '$R$ = '+ np.str(radius) + ' [m]'
    comment3 = '$\\tau$ = ' + np.str(a['condi_coeff'][1]) + ' [ms]'
    comment4 = '$\\tilde{S}$ = ' + np.str(a['condi_coeff'][0])
    comment5 = 'wavelength from ' + np.str(wl[0])+' to '+np.str(wl[1]) + ' [nm]'
    plt.text(1.0, 1.8,comment0, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)
    plt.text(1.0, 1.7,comment1, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)
    plt.text(1.0, 1.55,comment2, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)
    plt.text(1.0, 1.45,comment3, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)
    plt.text(1.0, 1.35,comment4, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)
    plt.text(1.0, 1.25,comment5, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)

    fig.savefig(fn,dpi=fig.dpi)

    return 'PLOTTED'


def compare(a,b,fn='dummy.ps'):
    """PLOT FITTING DETAILS"""
    plt.rcParams['figure.figsize'] = (8,8)
    fig = plt.figure(figsize=(8,8))
    gs = gridspec.GridSpec(100,100)
    ax1 = plt.subplot(gs[20:50,10:45])
    ax1_1 = ax1.twinx()
    ax2 = plt.subplot(gs[20:50,50:90])
    ax3 = plt.subplot(gs[53:90,10:45])
    ax4 = plt.subplot(gs[53:90,50:90])
    ax4_1 = ax4.twinx()

    ax1.plot(a.time,a.data)
    ax1.plot(b.time,b.data[b.ch])
    ax1_1.plot(a.t_nb,a.nb,color='blue',alpha=0.2)


    for i in range(0,a.gn):
        amax = np.max(savitzky_golay.main(a.ddata[i,:],11,3))
        bmax = np.max(b.ddata[i,:])
        ax2.plot(a.t_ddata[i,:],a.ddata[i,:]/amax,alpha=0.5,color='red')
        ax2.plot(a.t_ddata[i,:],a.ddatafit[i,:]/amax,color='green')

        ax2.plot(b.t_ddata[i,:],b.ddata[i,:]/bmax,alpha=0.5,color='blue')
        ax2.plot(b.t_ddata[i,:],b.ddatafit[i,:]/bmax,color='black')

        ax3.plot(a.ntime[i,:],a.ddata[i,:]/amax,alpha=1,color='red')
        ax3.plot(b.ntime[i,:],b.ddata[i,:]/bmax,alpha=1,color='blue')

    ax3.plot(a.ntime[0,:],a.condfit/np.max(a.condfit),
            alpha=0.5,color='green',linewidth=10.0)
    ax3.plot(b.ntime[0,:],b.condfit/np.max(b.condfit),
            alpha=0.5,color='black',linewidth=10.0)

    ax4.scatter(np.arange(a.gn),a.Tau,color='r',s=50)
    ax4.plot(np.arange(a.gn),[a.condTau,a.condTau],color='r')

    ax4.scatter(np.arange(b.gn),b.Tau,color='b',s=50)
    ax4.plot(np.arange(b.gn),[b.condTau,b.condTau],color='b')

    ax4_1.scatter(np.arange(a.gn),a.S,marker='x',s=50,color='black')
    ax4_1.plot(np.arange(a.gn),np.repeat(a.condS,2),color='black')

    ax4_1.scatter(np.arange(a.gn),b.S,marker='x',s=50,color='black')
    ax4_1.plot(np.arange(a.gn),np.repeat(b.condS,2),color='black')

    ax1.set_xlim(a.tr[0],a.tr[1])
    ax4.set_yscale('log')
    ax3.set_ylim(-1.2,1.2)
    ax4.set_ylim(1e0,1e3)
    ax4_1.set_yscale('log')
    ax4_1.set_ylim(1e10,1e15)
    ax4.set_ylabel('$\\tau [ms]$ (red)')
    ax4_1.set_ylabel('$\\tilde S_0 [a.u.]$ (black)')
    ax4.set_xlabel('PERIODS')
    ax2.set_xlabel('TIME[S]')

    ax3.set_xlabel('RELATIVE TIME[ms]')
    ax3.set_ylabel('MODULATED FIDA[a.u.]')
    ax1.set_xlabel('TIME [s]')
    ax1.set_ylabel('FIDA INTENSITY')
    ax1_1.set_ylabel('$P_{NBI} [kW]$')

    import time
    comment0 = 'INTEPRETATION OF FIDA MODULATIONSIGNAL IN SHOT '+np.str(a.shot)+' BY X.D.DU'
    comment1 =  time.strftime("%c")
    plt.text(0.3, 1.8,comment0, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)
    plt.text(0.3, 1.7,comment1, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)

    c_title1 = 'EXPERIMENT'
    comment2 = '$R$ = '+ np.str(a.radius) + ' [m]'
    comment3 = '$\\tau$ = ' + np.str(a.Tau) + ' [ms]'
    comment4 = '$\\tilde{S}$ = ' + np.str(a.S)
    comment5 = 'wavelength from ' + np.str(a.wavelength[0])+' to '+np.str(a.wavelength[1]) + ' [nm]'
    plt.text(0., 1.55,c_title1, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)
    plt.text(0., 1.45,comment2, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)
    plt.text(0., 1.35,comment3, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)
    plt.text(0., 1.25,comment4, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)
    plt.text(0., 1.15,comment5, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)

    c_title2 = 'SIMULATION'
    comment6 = '$R$ = '+ np.str(b.radius[b.ch]) + ' [m]'
    comment7 = '$\\tau$ = ' + np.str(b.condTau) + ' [ms]'
    comment8 = '$\\tilde{S}$ = ' + np.str(b.condS)
    comment9 = 'wavelength from ' + np.str(b.wavelength[0])+' to '+np.str(b.wavelength[1]) + ' [nm]'
    ax2.text(1.6, 1.55,c_title2, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)
    ax2.text(1.6, 1.45,comment6, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)
    ax2.text(1.6, 1.35,comment7, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)
    ax2.text(1.6, 1.25,comment8, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)
    ax2.text(1.6, 1.15,comment9, ha='left', va='center', transform=ax1.transAxes,fontsize=10.0)


    fig.savefig(fn,dpi=fig.dpi)

    return 'COMPARE'

def divflux(a):
    dsigdt = a.dsigdt
    sig_tau = a.sig_tau
    divf = a.divf
    S = a.S
    t = a.time
    sig = a.data

    plt.rcParams['figure.figsize'] = (8,8)
    fig = plt.figure(figsize=(8,8))
    gs = gridspec.GridSpec(100,100)
    ax0 = plt.subplot(gs[10:35,10:60])
    ax1 = plt.subplot(gs[35:65,10:60])
    ax2 = plt.subplot(gs[65:90,10:60])

    ax0.plot(t,sig,label='CONDITIONAL AVERAGED DATA')
    ax1.plot(t,-dsigdt,label='$-\\partial \\tilde{n}/\\partial t$')
    ax1.plot(t,-sig_tau,label='$-\\tilde{n}/\\tau$')
    ax1.plot(t,S,label='$\\tilde{S}$')
    ax1.plot([np.min(t),60],[0,0],alpha=0.2,color='black')

    ax2.plot(t,divf,linewidth=10.0)
    ax2.plot([np.min(t),60],[0,0],alpha=0.2,color='black')


    ax0.set_xlabel('RELATIVE TIME [ms]')
    ax0.set_ylabel('FIDA INTENSITY')

    ax2.set_xlabel('RELATIVE TIME [ms]')
    ax2.set_ylabel('$\\nabla \cdot \Gamma$')

    ax1.set_xlabel('RELATIVE TIME [ms]')
    ax1.set_ylabel('$-\\partial \\tilde{n}/\\partial t$, $-\\tilde{n}/\\tau$, $\\tilde{S}$')

    ax2.set_xlabel('RELATIVE TIME [ms]')
    ax2.set_ylabel('$\\nabla \cdot \Gamma$')

    ax0.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0,frameon=False)
    ax1.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0,frameon=False)

    import time
    comment0 = 'PHASE SPACE FLOW CALC. '
    comment1 =  time.strftime("%c")+'BY X.D. DU'
    comment2 = 'shot : ' + np.str(a.shot)
    comment3 = '$R$ = '+ np.str(a.radius) + ' [m]'
    comment4 = '$\\tau$ = ' + np.str(a.Tau) + ' [ms]'
    comment5 = '$\\tilde{S}$ = ' + np.str(np.abs(a.S[0]))
    #comment6 = 'wavelength from ' + np.str(wl[0]/10.)+' to '+np.str(wl[1]/10.) + ' [nm]'
    plt.text(1.05, 0.8, comment0, ha='left', va='center', transform=ax2.transAxes,fontsize=9.0)
    plt.text(1.05, 0.7, comment1, ha='left', va='center', transform=ax2.transAxes,fontsize=9.0)
    plt.text(1.05, 0.5, comment2, ha='left', va='center', transform=ax2.transAxes,fontsize=10.0)
    plt.text(1.05, 0.4,comment3, ha='left', va='center', transform=ax2.transAxes,fontsize=10.0)
    plt.text(1.05, 0.3, comment4, ha='left', va='center', transform=ax2.transAxes,fontsize=10.0)
    plt.text(1.05, 0.2,comment5, ha='left', va='center', transform=ax2.transAxes,fontsize=10.0)
    #plt.text(1.05, 0.1, comment6, ha='left', va='center', transform=ax2.transAxes,fontsize=10.0)
    return 'div flux'






