#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 13:49:51 2020

@author: vbokharaie
"""

def bplot(t, sol,
          sol2=None,
          plot_type=1,
          ylim=None,
          if_show=False,
          if_save=True,
          filesave='test.png',
          labels=[''],
          suptitle='',
          list_vl=[],
          all_policies=[],
          ylabel='',
          if_plot_in_pc=True):
    """
    Line plots of the solutions to the epidemilogical model.

    Parameters
    ----------
    t : numpy array
        time array
    sol : numpy array
        solution of an SIS or SIR model, or solution of any ODE.
    sol2 : numpy array, optional
        a second solution to an SIR/SIS model, if we want to compare two solutions`.
    plot_type : int, optional
        1: concurrent plots of all age groups, 2: each in a separate subplot. The default is 1.
    ylim : list of floats, optional
        y-axis limits. The default is (0,1).
    if_show : bool, optional
        Should plots be closed or not. The default is False.
    if_save : bool, optional
        save the plots to disk or not. The default is True.
    filesave : pathlib Path, optional
        filename for plots. The default is 'test.png'.
    labels : list of str, optional
        labels for plot legends. The default is [''].
    suptitle : str, optional
        main plot title. The default is ''.
    list_vl : list float, optional
        list of swithing times between policies, marked by red vertical lines. The default is [].
    all_policies : list of str, optional
        list of policies to implement at each switching time. The default is [].
    ylabel : str, optional
        y-axis label. The default is ''.

    Returns
    -------
    None.

    """
    import matplotlib.pyplot as plt
    import matplotlib.pylab as pl
    import matplotlib as mpl
    import numpy as np
    # plt.style.use('seaborn-whitegrid')
    plt.style.use('seaborn-darkgrid')
    # plt.style.use('ggplot')
    # mpl.rcParams['lines.linewidth'] = 3.0
    # mpl.rcParams['font.weight'] = 'bold'
    font = {'family' : 'DejaVu Sans',
                'sans-serif' : 'Tahoma',
                'weight' : 'regular',
                'size'   : 20}
    mpl.rc('grid', color='#316931', linewidth=1, linestyle='dotted')
    mpl.rc('font', **font)
    mpl.rc('lines', lw=3,)
    mpl.rc('xtick', labelsize=20)
    mpl.rc('ytick', labelsize=20)

    if_sol2 = True
    try:
        if sol2==None:
            if_sol2 = False
    except:
        pass
    if len(sol.shape)==2:
        Ng = sol.shape[1]
    else:
        Ng = 1
        sol = sol.reshape(sol.size, 1)
    colors = pl.cm.viridis(np.linspace(0,1,Ng))
    if if_plot_in_pc:
        if ylabel:
            ylabel = ylabel + ' in %'

        y_ax_scale = 100
    else:
        y_ax_scale = 1

    if plot_type == 1:
        fig, ax = plt.subplots(1, 1)
        fig.subplots_adjust(bottom=0.15, top=0.90, left=0.1, right = 0.9)
        for cc in np.arange(Ng):
            # my_label = 'x'+str(cc+1).zfill(2)

            ax.plot(t, sol[:, cc] * y_ax_scale, label=labels[cc], color = colors[cc])
            if if_sol2:
                ax.plot(t, sol2[:, cc] * y_ax_scale, label=labels[cc], color = colors[cc])
            if ylim:
                ax.set_ylim(ylim)
            if not labels==['']:
                ax.legend(bbox_to_anchor=(1.1, 1.06), prop={'size': 12})
            ax.set_xlabel('Time (days)')
            ax.set_xticks(np.arange(0, t[-1], step=30))
            plt.xticks(rotation=90)
            ax.set_ylabel(ylabel)
            ylim_max = ax.get_ylim()[1]
        for idx1, xc in enumerate(list_vl):
            ax.axvline(x=xc, color='r', linestyle='--', linewidth=1)
            bbox = {'fc': '0.9', 'pad': 4}
            props = {'ha': 'center', 'va': 'center', 'bbox': bbox,}
            my_text = all_policies[idx1]
            # make sure policy label does not cover main plot
            idx_xc_in_t = [idx for idx, x in enumerate(t) if x>xc][0]
            if sol[idx_xc_in_t, 0] < 0.9*ylim_max and sol[idx_xc_in_t, 0] < 0.7*ylim_max:
                policy_label_loc = 0.8*ylim_max
            else:
                policy_label_loc = 0.3*ylim_max
            ax.text(xc+10, policy_label_loc, my_text, props, rotation=90, color=colors[0])
        fig.suptitle(suptitle, fontsize=20, fontweight='bold')
    elif plot_type == 2:
        fig, ax = plt.subplots(Ng, 1, figsize=(18,12))
        fig.tight_layout()
        fig.subplots_adjust(bottom=0.05, top=0.95, left = 0.03)
        for cc in np.arange(Ng):
            # my_label = 'x'+str(cc+1).zfill(2)
            ax[cc].plot(t, sol[:, cc] * y_ax_scale, label=labels, color = colors[cc])
            if if_sol2:
                ax[cc].plot(t, sol2[:, cc] * y_ax_scale, label=labels, color = colors[cc])
            if ylim:
                ax[cc].set_ylim(ylim)
            ax[cc].set_ylabel(labels[cc])
            if cc == Ng-1:
                ax[cc].set_xlabel('Time (days)')
        # fig.suptitle(suptitle)
    if not if_show:
        plt.close('all')
    if if_save:
        fig.savefig(filesave)