#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:07:11 2020

@author: vbokharaie
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:04:50 2020

@author: vbokharaie

You can use this script as a template to run the simulations of the epidemilogicla model.
This scrip is used to run the simulation used in:
    https://people.tuebingen.mpg.de/vbokharaie/Iran_COVID19.html

For more info on the mathematical basis, look at:
    https://people.tuebingen.mpg.de/vbokharaie/Estimating_Covid19_contact_rates.pdf

"""

if __name__ == '__main__':
    from func_main import main
    from policies import str_policy_info
    from pathlib import Path

    #%% print policy info text?
    if_print_policies_info = False
    if if_print_policies_info:
        print(str_policy_info())
    subfolder = Path('outputs_IRAN')
    dir_save_plots_main = Path(Path(__file__).resolve().parent, subfolder)

    country = 'Iran'
    #%% 1. uncontained
    t_end = 541
    list_t_switch = [0,]
    all_policies = ['Uncontained',]
    policy_definition = dict(zip(list_t_switch, all_policies))
    policy_name = 'Uncontained'
    x00 = 1e-4  # 0.0001 population in Iran = 8500 people
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    dict_uncontained = main(country, policy_name, policy_definition,
                            dir_save_plots_main, t_end=t_end, x0_vec=x0_vec)

    #%% 2. current status
    t_end = 91
    list_t_switch = [0, 54, 77]
    all_policies = ['Uncontained',
                    'Schools_closed',
                    'Schools_Offices_closed',
              ]
    policy_definition = dict(zip(list_t_switch, all_policies))
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    policy_name = 'Current_status'
    dict_current = main(country, policy_name, policy_definition,
                            dir_save_plots_main, t_end=t_end, x0_vec=x0_vec)

    #%% 3. current status then uncontained
    t_end = 541
    list_t_switch = [0, 54, 77, 84, 100]
    all_policies = ['Uncontained',
                    'Schools_closed',
                    'Schools_Offices_closed',
                    'Schools_closed',
                    'Uncontained',
              ]
    policy_definition = dict(zip(list_t_switch, all_policies))
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    policy_name = 'Current_status_then_uncontained'
    dict_current = main(country, policy_name, policy_definition,
                            dir_save_plots_main, t_end=t_end, x0_vec=x0_vec)

    #%% 4. current status then schools closed
    t_end = 541
    list_t_switch = [0, 54, 77, 84,]
    all_policies = ['Uncontained',
                    'Schools_closed',
                    'Schools_Offices_closed',
                    'Schools_closed',
                    ]
    policy_definition = dict(zip(list_t_switch, all_policies))
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    policy_name = 'Current_status_then_SchoolsClosed'
    dict_current = main(country, policy_name, policy_definition,
                            dir_save_plots_main, t_end=t_end, x0_vec=x0_vec)

    #%% 5. current status then social distancing
    t_end = 541
    list_t_switch = [0, 54, 77, 90]
    all_policies = ['Uncontained',
                    'Schools_closed',
                    'Schools_Offices_closed',
                    'Social_Distancing'
              ]
    policy_definition = dict(zip(list_t_switch, all_policies))
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    policy_name = 'Current_status_then_SocialDistancing'
    dict_current = main(country, policy_name, policy_definition,
                            dir_save_plots_main, t_end=t_end, x0_vec=x0_vec)

    #%% 5b. current status then social distancing for 3 month
    t_end = 541
    list_t_switch = [0, 54, 77, 90, 180]
    all_policies = ['Uncontained',
                    'Schools_closed',
                    'Schools_Offices_closed',
                    'Social_Distancing',
                    'Uncontained',
                    ]
    policy_definition = dict(zip(list_t_switch, all_policies))
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    policy_name = 'Current_status_then_SocialDistancing_for3months'
    dict_current = main(country, policy_name, policy_definition,
                            dir_save_plots_main, t_end=t_end, x0_vec=x0_vec)

    #%% 6. current status then Lock-down
    t_end = 541
    list_t_switch = [0, 54, 77, 90]
    all_policies = ['Uncontained',
                    'Schools_closed',
                    'Schools_Offices_closed',
                    'Lockdown'
              ]
    policy_definition = dict(zip(list_t_switch, all_policies))
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    policy_name = 'Current_status_then_Lockdown'
    dict_current = main(country, policy_name, policy_definition,
                            dir_save_plots_main, t_end=t_end, x0_vec=x0_vec)

    #%% 7. current status then Lock-down for only two months
    t_end = 541
    list_t_switch = [0, 54, 77, 90, 150,]
    all_policies = ['Uncontained',
                    'Schools_closed',
                    'Schools_Offices_closed',
                    'Lockdown',
                    'Uncontained',
                    ]
    policy_definition = dict(zip(list_t_switch, all_policies))
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    policy_name = 'Current_status_then_Lockdown_for2months'
    dict_current = main(country, policy_name, policy_definition,
                            dir_save_plots_main, t_end=t_end, x0_vec=x0_vec)

    #%% 8. current status then Lock-down fir only two months and then kids elderly stay home
    t_end = 541
    list_t_switch = [0, 54, 77, 90, 150, 180, 270]
    all_policies = ['Uncontained',
                    'Schools_closed',
                    'Schools_Offices_closed',
                    'Lockdown',
                    'Uncontained',
                    'Kids_Elderly_self_isolate',
                    'Uncontained',
                    ]
    policy_definition = dict(zip(list_t_switch, all_policies))
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    policy_name = 'Current_status_then_Lockdown_for2months_then_Kids_Elderly_self_isolate'
    dict_current = main(country, policy_name, policy_definition,
                            dir_save_plots_main, t_end=t_end, x0_vec=x0_vec)

    #%% 8. current status then Lock-down fir only two months and then kids elderly stay home
    t_end = 541
    list_t_switch = [0, 54, 77, 90, 120,]
    all_policies = ['Uncontained',
                    'Schools_closed',
                    'Schools_Offices_closed',
                    'Lockdown',
                    'R0_is_1',
                   ]
    policy_definition = dict(zip(list_t_switch, all_policies))
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    policy_name = 'Current_status_then_Lockdown_then_R0_1'
    dict_current = main(country, policy_name, policy_definition,
                            dir_save_plots_main, t_end=t_end, x0_vec=x0_vec)


    #%% 9.
    t_end = 541
    list_t_switch = [0, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360, ]
    all_policies = ['Uncontained',
                    'R0_is_1',
                    'Uncontained',
                    'R0_is_1',
                    'Uncontained',
                    'R0_is_1',
                    'Uncontained',
                    'R0_is_1',
                    'Uncontained',
                    'R0_is_1',
                    'Uncontained',
                   ]
    policy_definition = dict(zip(list_t_switch, all_policies))
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    policy_name = 'Uncontained_then_switching_R0'
    dict_current = main(country, policy_name, policy_definition,
                            dir_save_plots_main, t_end=t_end, x0_vec=x0_vec)


    #%% 10.
    t_end = 541
    list_t_switch = [0, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360,]
    all_policies = ['Uncontained',
                    'Lockdown',
                    'Uncontained',
                    'Lockdown',
                    'Uncontained',
                    'Lockdown',
                    'Uncontained',
                    'Lockdown',
                    'Uncontained',
                    'Lockdown',
                    'Uncontained',
                   ]
    policy_definition = dict(zip(list_t_switch, all_policies))
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    policy_name = 'Uncontained_then_switching_Lockdown'
    dict_current = main(country, policy_name, policy_definition,
                            dir_save_plots_main, t_end=t_end, x0_vec=x0_vec)


    #%% 11. current status then Lock-down for only two months and then kids elderly stay home
    t_end = 541
    list_t_switch = [0, 90, 120, 150, 180, 210, 240, 270, 300, 330,]
    all_policies = ['Uncontained',
                    'Lockdown',
                    'R0_is_1',
                    'Uncontained',
                    'Lockdown',
                    'R0_is_1',
                    'Uncontained',
                    'Lockdown',
                    'R0_is_1',
                    'Uncontained',

                     ]
    policy_definition = dict(zip(list_t_switch, all_policies))
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    policy_name = 'Uncontained_then_switching_Lockdown_R0'
    dict_current = main(country, policy_name, policy_definition,
                            dir_save_plots_main, t_end=t_end, x0_vec=x0_vec)


    #%% 11. current status then Lock-down for only two months and then kids elderly stay home
    t_end = 541
    list_t_switch = [0, 90]
    policy_list = ['Uncontained',
                   'Schools_closed',
                   'Elderly_self_isolate',
                   'Kids_Elderly_self_isolate',
                   'Schools_Offices_closed',
                   'Adults_Elderly_Self_isolate',
                   'Social_Distancing',
                   'Lockdown',
                   ]
    policy_labels = ['UN',
                   'KI',
                   'EL',
                   'KIEL',
                   'KIOF',
                   'ADEL',
                   'SD',
                   'LD',
                   ]
    dict_I = {}
    dict_R = {}
    for policy in policy_list:
        all_policies = ['Uncontained',]
        all_policies.append(policy)
        policy_definition = dict(zip(list_t_switch, all_policies))
        x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
        policy_name = 'Uncontained_then_' + policy
        dict_current = main(country, policy_name, policy_definition,
                            dir_save_plots_main, t_end=t_end, x0_vec=x0_vec)

        dict_I[policy] = dict_current['sol_agg_SIR_I']
        dict_R[policy] = dict_current['sol_agg_SIR_R']

    import numpy as np
    for idx, policy in enumerate(dict_I.keys()):

        if idx == 0:
            sol_agg_SIR_R_plot = dict_R[policy]
            sol_agg_SIR_I_plot = dict_I[policy]
        else:
            sol_agg_SIR_R_plot = np.concatenate((sol_agg_SIR_R_plot,
                                                 dict_R[policy]), axis=1)
            sol_agg_SIR_I_plot = np.concatenate((sol_agg_SIR_I_plot,
                                                 dict_I[policy]), axis=1)

    dir_save_plots_country = Path(dir_save_plots_main, country)
    dir_save_plots = Path(dir_save_plots_country, '00_OVERALL')
    dir_save_plots.mkdir(exist_ok=True, parents=True)
    filesave_I = Path(dir_save_plots, 'SIR_I_AGG_ALL_policies.png')
    filesave_R = Path(dir_save_plots, 'SIR_R_AGG_ALL_policies.png')

    from plots import bplot
    t = np.arange(0, t_end+.01, step=0.1)
    list_all_policies = ['Uncontained']
    list_all_policies.extend(['Policy Imposed']*(len(policy_list)-1))
    bplot(t, sol_agg_SIR_R_plot, plot_type=1, filesave=filesave_R,
      suptitle='', labels=policy_labels, list_vl=list_t_switch,
      list_all_policies=list_all_policies, ylabel='Recovered Ratio')
    bplot(t, sol_agg_SIR_I_plot, plot_type=1, filesave=filesave_I,
      suptitle='', labels=policy_labels, list_vl=list_t_switch,
      list_all_policies=list_all_policies, ylabel='Infectious Ratio')
