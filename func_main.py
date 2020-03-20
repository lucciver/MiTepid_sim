#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 12:59:33 2020

@author: vbokharaie
"""

def main(country, policy_name, policy_definition, dir_save_plots_main):
    """
    Simulate the epid model.

    Calculate trajectory of an epid model for a country and for a defined policy.

    Parameters
    ----------
    country : str
        Name of the country, for which population distribution is defined in the code.
    policy_name : str
        a given name to oplicy used as subfolder name.
    policy_definition : dict
        a dictionary of {time: basic_policy} format.
    dir_save_plots_main : pathlib Path
        main folder to save plots. Then a subfolder in country/policyname is used to save files.

    Returns
    -------
    None.

    """
    # local imports
    from models import SIS, SIR
    from plots import bplot
    from utils import sol_aggregate, load_mat
    from policies import get_Bopt, str_policy_info

    # external imports
    from scipy.integrate import odeint
    import numpy as np
    from numpy.linalg import inv, eigvals
    from pathlib import Path

    # assuming data files are where the .py file is:
    dir_source_mat = Path(Path(__file__).resolve().parent)
    file_data_opt_SIR = Path(dir_source_mat, 'Optimised_B', 'SIR_B_opt_ALL.mat')
    file_data_opt_SIS = Path(dir_source_mat, 'Optimised_B', 'SIS_B_opt_ALL.mat')

    # population distribution in each country
    # in age ranges of each 10 years till 80 and 80+
    # obtained from www.populationpyramid.net
    dict_pop = {}
    dict_pop['China'] = [11.9, 11.6, 13.5, 15.6, 15.6, 15.0, 10.4, 4.7, 1.7]
    dict_pop['Italy'] = [8.4, 9.5, 10.1, 11.8, 15.3, 15.7, 12.3, 9.8, 7.3]
    dict_pop['Iran'] = [17.4, 13.9, 15.5, 20.0, 13.6, 9.7, 6.2, 2.7, 1.0]
    dict_pop['SouthKorea'] = [8.4, 9.5, 13.3, 14.0, 16.3, 16.4, 12.1, 6.6, 3.5]
    dict_pop['Germany'] = [9.2, 9.6, 11.2, 12.8, 12.5, 16.2, 12.4, 9.1, 6.9]


    # country = 'Iran'  # can be any one of the above
    dir_save_plots_country = Path(dir_save_plots_main, country)


    B_opt_SIS_orig = get_Bopt(file_data_opt_SIS, country, 'Uncontained', )
    B_opt_SIR_orig = get_Bopt(file_data_opt_SIR, country, 'Uncontained', )


    Ng = B_opt_SIS_orig.shape[0]  # number of age groups

    # making the D matrix, alpha represents recovery rate
    alpha = load_mat(file_data_opt_SIR, 'alpha')
    ALPHA = np.ones((Ng, 1)) * alpha
    D = np.zeros((Ng,Ng))
    np.fill_diagonal(D, ALPHA)

    # age groups, used as legends in plots
    age_groups = ['[0-10)',  '[10-20)', '[20-30)', '[30-40)',
                  '[40-50)', '[50-60)', '[60-70)', '[70-80)', '80+',]



    #%% R_0 uncontained
    rho = np.max(np.abs(eigvals(np.matmul(-inv(D),B_opt_SIS_orig))))  # spectral radius of -inv(D)*B
    print('\u03C1 = %2.2f'% rho)

    # initial conditions, t_f
    x00 = 1e-3
    x0_SIS = np.ones(Ng)*x00
    x0_SIR = np.concatenate((np.ones(Ng)*x00, np.zeros(Ng)))
    t_end = 500

    # uncontained solution
    t = np.arange(0, t_end+.01, step=0.1)

    sol_SIS_orig = odeint(SIS, x0_SIS, t, args=(B_opt_SIS_orig, ALPHA))
    sol_SIR_orig = odeint(SIR, x0_SIR, t, args=(B_opt_SIR_orig, ALPHA))
    sol_SIR_I_orig = sol_SIR_orig[:,:Ng]
    sol_SIR_R_orig = sol_SIR_orig[:,Ng:]
    sol_agg_SIS_orig = sol_aggregate(sol_SIS_orig, dict_pop[country])
    sol_agg_SIR_I_orig = sol_aggregate(sol_SIR_I_orig, dict_pop[country])
    sol_agg_SIR_R_orig = sol_aggregate(sol_SIR_R_orig, dict_pop[country])

    # contained solution, possibly with a switching policy
    # In the following example, population starts uncontained, and after 90 days
    # lockdown policy is imposed
    # list_t_switch = [0, 60, 90, 120, 150]
    # all_policies = ['Lockdown',
    #                 'Adults_self_isolate',
    #                 'Schools_closed',
    #                 'Elderly_stay_home',]
    list_t_switch = list(policy_definition.keys())
    all_policies = list(policy_definition.values())

    str_policy = policy_name  # used to make subfolder name
    dir_save_plots = Path(dir_save_plots_country, Path(str_policy))
    dir_save_plots.mkdir(exist_ok = True, parents=True)
    file_policy = Path(dir_save_plots, 'policy_details.txt')
    with open(file_policy, 'w') as f:
        f.write('\n    time (day) --->  Policy')
        f.write('\n    ------------------------------------------')

    for idx, t_switch1 in enumerate(list_t_switch):
        policy = all_policies[idx]
        with open(file_policy, 'a') as my_tex:
            my_tex.write('\n %10.1f    --->  %s'%(t_switch1, policy))  # just to remove previous contents

        B_opt_SIS = get_Bopt(file_data_opt_SIS, country, policy)
        B_opt_SIR = get_Bopt(file_data_opt_SIR, country, policy)

        try:
            t_switch2 = list_t_switch[idx+1]
        except IndexError:
            t_switch2 = t_end + 1e-10

        t_step = np.arange(t_switch1, t_switch2, step=0.1)

        sol_SIS_step = odeint(SIS, x0_SIS, t_step, args=(B_opt_SIS, ALPHA))
        sol_SIR_step = odeint(SIR, x0_SIR, t_step, args=(B_opt_SIR, ALPHA))
        x0_SIS = sol_SIS_step[-1]
        x0_SIR = sol_SIR_step[-1]

        if idx == 0:
            sol_SIR = sol_SIR_step
            sol_SIS = sol_SIS_step
        else:
            sol_SIR = np.concatenate((sol_SIR, sol_SIR_step))
            sol_SIS = np.concatenate((sol_SIS, sol_SIS_step))

    sol_SIR_I = sol_SIR[:,:Ng]
    sol_SIR_R = sol_SIR[:,Ng:]
    with open(file_policy, 'a') as my_tex:
         my_tex.write('\n \n \n ')
         my_tex.write(str_policy_info())  # just to remove previous contents

    #
    plot_type = 1  # can be 1 -> all in one subplots, or 2 -> each age group in one subplot
    if_plot = True
    if if_plot:
        # str_type = 'pt'+str(plot_type)+'_'
        ### SIS
        filesave = Path(dir_save_plots, 'SIS_groups_' + str_policy+'.png')
        suptitle = country + ' --- SIS'
        bplot(t, sol_SIS, plot_type=plot_type, filesave=filesave,
              labels=age_groups, suptitle='', list_vl=list_t_switch,
              all_policies=all_policies, ylabel='Infective Ratio')


        ### SIR_I
        suptitle = ''
        filesave = Path(dir_save_plots, 'SIR_I_groups_' + str_policy+'.png')
        bplot(t, sol_SIR_I, plot_type=plot_type, filesave=filesave,
              labels=age_groups, suptitle=suptitle, list_vl=list_t_switch,
              all_policies=all_policies, ylabel='Infective Ratio')

        ### SIR_R
        suptitle = ''
        filesave = Path(dir_save_plots, 'SIR_R_groups_' + str_policy+'.png')
        bplot(t, sol_SIR_R, plot_type=plot_type, filesave=filesave,
              labels=age_groups, suptitle=suptitle, list_vl=list_t_switch,
              all_policies=all_policies, ylabel='Recoverd Ratio')

        ### diff
        suptitle = ' Difference between solutions to SIS and SIR models'
        filesave = Path(dir_save_plots, 'diff_SIS_SIR_groups_' + str_policy+'.png')
        bplot(t, abs(sol_SIS-sol_SIR_I), plot_type=plot_type, filesave=filesave,
              labels=age_groups, suptitle=suptitle, list_vl=list_t_switch, all_policies=all_policies)
        ### Aggregate
        my_labels_I = ['policy',
                     'Uncontained',]
        my_labels_R = ['policy',
                     'Uncontained',]

        filesave = Path(dir_save_plots, 'SIS_AGG_' + str_policy+'.png')
        sol_agg_SIS = sol_aggregate(sol_SIS, dict_pop[country])

        str_max1 = "{:2.2f}".format((sol_agg_SIS_orig[-1,0])*100)+ '%'+ ', '
        sol_agg_SIS_plot = np.concatenate((sol_agg_SIS, sol_agg_SIS_orig), axis=1)

        str_max2 = "{:2.2f}".format((sol_agg_SIS[-1,0])*100)+ '%'
        suptitle = '\nEventual Ratio of Total Infected: ' \
            + str_max1 + str_max2

        bplot(t, sol_agg_SIS_plot, plot_type=1, filesave=filesave,
              suptitle=suptitle, labels=my_labels_I, list_vl=list_t_switch,
              all_policies=all_policies, ylabel='Infective Ratio')

        # SIR
        filesave_I = Path(dir_save_plots, 'SIR_I_AGG_' + str_policy+'.png')
        filesave_R = Path(dir_save_plots, 'SIR_R_AGG_' + str_policy+'.png')
        sol_agg_SIR_I = sol_aggregate(sol_SIR_I, dict_pop[country])
        sol_agg_SIR_R = sol_aggregate(sol_SIR_R, dict_pop[country])
        str_max_I_1 = "{:2.2f}".format(np.max(sol_agg_SIR_I_orig)*100)+ '%'+ ', '
        str_max_R_1 = "{:2.2f}".format(np.max(sol_agg_SIR_R_orig)*100)+ '%'+ ', '

        sol_agg_SIR_I_plot = np.concatenate((sol_agg_SIR_I,
                                           sol_agg_SIR_I_orig,), axis=1)

        str_max2 = "{:2.2f}".format(np.max(sol_agg_SIR_I)*100)+ '%'
        suptitle = '\nPeak of Infected Ratio in the population: ' + str_max_I_1 + str_max2
        bplot(t, sol_agg_SIR_I_plot, plot_type=1, filesave=filesave_I,
              suptitle=suptitle, labels=my_labels_I, list_vl=list_t_switch,
              all_policies=all_policies, ylabel='InfectivesRatio')
        sol_agg_SIR_R_plot = np.concatenate((sol_agg_SIR_R,
                                            sol_agg_SIR_R_orig), axis=1)

        str_max2 = "{:2.2f}".format(np.max(sol_agg_SIR_R)*100)+ '%'
        suptitle = '\nEventual Ratio of Recovered in the population: ' + str_max_R_1 + str_max2
        bplot(t, sol_agg_SIR_R_plot, plot_type=1, filesave=filesave_R,
              suptitle=suptitle, labels=my_labels_R, list_vl=list_t_switch,
              all_policies=all_policies, ylabel='Recovered Ratio')
