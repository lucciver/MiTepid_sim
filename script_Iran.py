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
                    'Kids_Elderly_stay_home',
                    'Uncontained',
                    ]
    policy_definition = dict(zip(list_t_switch, all_policies))
    x0_vec=[x00, x00, x00, x00, x00, x00, x00, x00, x00,]
    policy_name = 'Current_status_then_Lockdown_for2months_then_Kids_Elderly_stay_home'
    dict_current = main(country, policy_name, policy_definition,
                            dir_save_plots_main, t_end=t_end, x0_vec=x0_vec)

