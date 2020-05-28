#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 11:25:16 2020

@author: vbokharaie
"""


class epid_sim:
    """
    A class as a container for all relvant data of an epidemilogical model.

    All the relevant info for a simulation should pass through this class.
    """

    #  a variable to keep track of all created objects
    total_created_objects = 0
    """ keeps track of total number of objects"""

    ###
    def __init__(self,
                 model_type,
                 dir_save_plots_main,
                 country,
                 policy_list,
                 policy_switch_times,
                 x0,
                 t_end,
                 str_policy,
                 group_labels,
                 B,
                 Gamma=None,
                 Mu=None,
                 Sigma=None,
                 t_step=0.1,
                 ref_class=None,
                 xternal_inputs={},
                 ):

        import numpy as np
        from pathlib import Path

        # main variables
        self.B = B
        self.Ng = self.B.shape[0]  # number of age groups
        dir_save_plots_country = Path(dir_save_plots_main, country)
        self.dir_save_plots = Path(dir_save_plots_country, Path(str_policy))
        self.dir_save_plots.mkdir(exist_ok = True, parents=True)
        self.country = country
        self.ref_class = ref_class
        self.model_type = model_type
        self.str_policy = str_policy
        self.policy_switch_times = policy_switch_times
        self.policy_list = policy_list
        self.group_labels = group_labels
        if Gamma is None:
            self.Gamma = np.zeros((self.Ng, self.Ng))
        else:
            self.Gamma = Gamma

        if Mu is None:
            self.Mu = np.zeros((self.Ng, self.Ng))
        else:
            self.Mu = Mu
        self.Sigma = Sigma
        self.D = self.Gamma + self.Mu
        if np.count_nonzero(self.D) == 0:
            print('Warning: matrix D is all zeros!')

        self.x0 = self.correct_x0(x0)
        self.xternal_inputs = xternal_inputs
        self.t_end = t_end
        self.t_step = t_step
        self.t = np.arange(0, t_end+.01, step=t_step)
        self.model_type = model_type
        self.policy_definition = dict(zip(policy_switch_times, policy_list))

        self.calc_sol()


    def calc_sol(self, ):
        from pathlib import Path
        import numpy as np
        from numpy.linalg import inv, eigvals
        from scipy.integrate import odeint

        from mitepid.utils import sort_out_t_policy_x0
        from mitepid.models import SIS, SIR, SEIR
        from mitepid.utils import sol_aggregate, load_mat
        from mitepid.policies import get_B_policy, str_policy_info, get_pop_distr

        list_t1, list_t2, list_policies, list_x0, list_t_switch, list_all_policies = \
                    sort_out_t_policy_x0(self.policy_definition,
                                         self.xternal_inputs,
                                         self.t_end,
                                         self.Ng)
        file_policy = Path(self.dir_save_plots, 'policy_details.txt')

        x0_step = self.x0
        for idx in np.arange(len(list_t1)):
            t_switch1 = list_t1[idx]
            t_switch2 =  list_t2[idx]
            policy = list_policies[idx]
            x0_xtrnal = list_x0[idx]
            with open(file_policy, 'a') as my_tex:
                my_tex.write('\n %10.1f    --->  %s'%(t_switch1, policy))  # remove previous contents
            B_step = get_B_policy(B=self.B, country=self.country,
                                  policy=policy, )

            #%% R_0 policy
            rho = np.max(np.abs(eigvals(np.matmul(-inv(self.D), B_step))))  # spectral radius of -inv(D)*B
            print('%s   ---> R_0 = %2.2f'% (policy, rho))

            t_step = np.arange(t_switch1, t_switch2, step=0.1)
            x0_xtrnal = self.correct_x0(x0_xtrnal)
            x0_step = np.array(x0_step) + x0_xtrnal
            # solve the ODE
            if self.model_type == 'SIS':
                sol_step = odeint(SIS, x0_step, t_step, args=(B_step, self.Gamma, self.Mu))
            elif self.model_type == 'SIR':
                sol_step = odeint(SIR, x0_step, t_step, args=(B_step, self.Gamma, self.Mu))
            elif self.model_type == 'SEIR':
                sol_step = odeint(SEIR, x0_step, t_step, args=(B_step, self.Gamma, self.Mu,
                                                               self.Sigma))

            # update x0
            x0_step = sol_step[-1]

            if idx == 0:
                sol_all = sol_step
            else:
                sol_all = np.concatenate((sol_all, sol_step))

        country = self.country
        sol_dict = {}
        sol_agg_dict = {}
        Ng = self.Ng
        if self.model_type == 'SIS':
            sol_dict['I'] = sol_all[:,:Ng]
            sol_agg_dict['I'] = sol_aggregate(sol_dict['I'], get_pop_distr(country))
        elif self.model_type == 'SIR':
            sol_dict['I'] = sol_all[:,:Ng]
            sol_agg_dict['I'] = sol_aggregate(sol_dict['I'], get_pop_distr(country))
            sol_dict['R'] = sol_all[:,Ng:2*Ng]
            sol_agg_dict['R'] = sol_aggregate(sol_dict['R'], get_pop_distr(country))
        elif self.model_type == 'SEIR':
            sol_dict['I'] = sol_all[:,:Ng]
            sol_agg_dict['I'] = sol_aggregate(sol_dict['I'], get_pop_distr(country))
            sol_dict['R'] = sol_all[:,Ng:2*Ng]
            sol_agg_dict['R'] = sol_aggregate(sol_dict['R'], get_pop_distr(country))
            sol_dict['E'] = sol_all[:,2*Ng:3*Ng]
            sol_agg_dict['E'] = sol_aggregate(sol_dict['E'], get_pop_distr(country))

        self.sol_dict = sol_dict
        self.sol_agg_dict = sol_agg_dict

    #################################################################################################
    #%%
    def correct_x0(self, x0):
        import numpy as np
        model_type = self.model_type
        Ng = self.Ng

        if model_type == 'SIS':
            if len(x0) == 1:
                x0 = np.ones(Ng)*x0
            elif len(x0) == Ng:
                x0 = x0
            else:
                raise('Something wrong with initial conditions vector!')
        elif model_type == 'SIR':
            if len(x0) == 1:
                x0 = np.concatenate((np.ones(Ng)*x0, np.zeros(Ng)))
            elif len(x0) == Ng:
                x0 = np.concatenate((x0, np.zeros(Ng)))
            elif len(x0) == 2*Ng:
                x0 = x0
            else:
                raise('Something wrong with initial conditions vector!')
        elif model_type == 'SEIR':
            if len(x0) == 1:
                x0 = np.concatenate((np.ones(Ng)*x0, np.zeros(Ng), np.zeros(Ng)))
            elif len(x0) == Ng:
                x0 = np.concatenate((x0, np.zeros(Ng), np.zeros(Ng)))
            elif len(x0) == 3*Ng:
                x0 = x0
            else:
                raise('Something wrong with initial conditions vector!')
        return x0

    def plot(self, suptitle = '', multi_ax=False, cmap='viridis'):
        from mitepid.plots import bplot
        from pathlib import Path
        import numpy as np

        if multi_ax:
            plot_type=1
            str_multi = '_multi_ax'
        else:
            plot_type=2
            str_multi = ''
        for key in self.sol_dict.keys():

            if not self.ref_class is None:
                sol_plot = np.concatenate((self.sol_dict[key],
                                           self.ref_class.sol_dict[key]), axis=1)
            else:
                sol_plot = self.sol_dict[key]
            str_file_name = self.model_type + '_' + key + '_groups' + str_multi
            filesave = Path(self.dir_save_plots, str_file_name + '_' +
                            self.str_policy+'_tf_'+str(int(self.t_end))+'.png')
            bplot(self.t,
                  sol_plot,
                  plot_type=plot_type,
                  filesave=filesave,
                  labels=self.group_labels,
                  suptitle=suptitle,
                  list_vl=self.policy_switch_times,
                  list_all_policies=self.policy_list,
                  ylabel=key,
                  Ng=self.Ng,
                  cmap=cmap)

    def plot2(self, suptitle = 'standard', multi_ax=False, cmap='viridis'):
        from pathlib import Path
        import numpy as np
        from mitepid.plots import bplot
        for key in self.sol_dict.keys():

            if not self.ref_class is None:
                sol_plot = np.concatenate((self.sol_agg_dict[key],
                                           self.ref_class.sol_agg_dict[key]), axis=1)
                str2 = ", {:2.2f}".format(np.max(self.ref_class.sol_agg_dict[key])*100)+ '%'
                plot_labels = ['policy',
                               'Uncontained',]
            else:
                sol_plot = self.sol_agg_dict[key]
                str2 = ''
                plot_labels = ['policy',]
            str_save = self.model_type + '_' + key + '_AGG_'
            filesave = Path(self.dir_save_plots,
                            str_save + self.str_policy+'_tf_'+str(int(self.t_end))+'.png')

            str1 = "{:2.2f}".format(np.max(self.sol_agg_dict[key])*100)+ '%'

            if suptitle=='standard':
                suptitle_text = '\nPeak/Maximum of Infectious Ratio in the population: '\
                    + str1 + str2
            else:
                suptitle_text = suptitle
            bplot(self.t,
                  sol_plot,
                  plot_type=1,
                  filesave=filesave,
                  suptitle=suptitle_text,
                  labels=plot_labels,
                  list_vl=self.policy_switch_times,
                  list_all_policies=self.policy_list,
                  ylabel='Compartment '+key,
                  cmap='Dark2')


