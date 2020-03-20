#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:04:50 2020

@author: vbokharaie

You can use this script as a template to run the simulations of the epidemilogicla model.
For more info of what exactly is the model and what you can get from it, look at:
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
    subfolder = Path('outputs')
    dir_save_plots_main = Path(Path(__file__).resolve().parent, subfolder)

    # run policies for the country
    country = 'Germany'
    list_t_switch = [0, 60, 90, 120]
    all_policies = ['Lockdown',
                    'Uncontained',
                    'All_s_isolate_but_kids',
                    'Uncontained',]
    policy_definition = dict(zip(list_t_switch, all_policies))
    policy_name = 'policy1'
    main(country, policy_name, policy_definition, dir_save_plots_main)

    # run policies for the country
    country = 'Iran'
    list_t_switch = [0, 60, 90, 120]
    all_policies = ['All_s_isolate_but_kids',
                    'Uncontained',
                    'All_s_isolate_but_kids',
                    'Uncontained',]
    policy_definition = dict(zip(list_t_switch, all_policies))
    policy_name = 'policy2'
    main(country, policy_name, policy_definition, dir_save_plots_main)

    # run policies for the country
    country = 'Italy'
    list_t_switch = [0, 60, 90,]
    all_policies = ['All_self_isolate',
                    'Lockdown',
                    'Uncontained',]
    policy_definition = dict(zip(list_t_switch, all_policies))
    policy_name = 'policy3'
    main(country, policy_name, policy_definition, dir_save_plots_main)
