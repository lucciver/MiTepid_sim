#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 12:27:48 2020

@author: vbokharaie
"""



def load_mat(filename, var_name=None):
    """
    Load data from mat files.

    Parameters
    ----------
    filename : pathlib Path
        filename including possibly multiple variable in matlab mat format.
    var_name : str, optional
        variable to be loaded. The default is None.

    Returns
    -------
    my_data : TYPE
        DESCRIPTION.

    """
    from scipy.io import loadmat
    data_struct = loadmat(filename)
    if not var_name:
        var_name = [x for x in data_struct.keys() if not '__' in x][0]
    my_data = data_struct[var_name]
    return my_data


def save_mat(filename, var):
    """
    Save data to mat files.

    Parameters
    ----------
    filename : pathlib Path
        filename.
    var : str
        variable name.

    Returns
    -------
    None.

    """
    folder = filename.parent
    folder.mkdir(parents=True, exist_ok=True)
    my_dict = {'var_name': var}
    from scipy.io import savemat
    savemat(filename, my_dict)

def sol_aggregate(sol_in, pop_country):
    """
    Calculate the aggregate trajectory of the whole population.

    Each age groups is weighted based on its ratio of the whol population.

    Parameters
    ----------
    sol_in : numpy array
        solution to epid model. shape (N_time x N_groups)
    pop_country : list of floats
        list of relative ratio of each age group in the population.

    Returns
    -------
    sol_out : numpy array
        aggregate trajectory. shape (N_time x 1)

    """
    import numpy as np
    sol = sol_in.copy()
    Ng = sol.shape[1]
    for cc in np.arange(Ng):
        sol[:,cc] = sol[:,cc] * pop_country[cc]/100
    sol_out = np.sum(sol, axis=1)
    sol_out = sol_out.reshape(sol_out.size,1)
    return sol_out

def scale_B_opt(B_opt_in, list_scales=None):
    """
    Scale matrix of contact ratios for a given policy.

    Parameters
    ----------
    B_opt_in : numpy 2D array
        matrix of contact rates.
    list_scales : list floats, optional
        how each row of B_opt_in should be scaled.
        The default is None, in which case return B_opt_in.

    Returns
    -------
    B_opt_out : numpy 2D array
        scaled contact rates.
    """
    list_scales = list(list_scales)
    Ng = B_opt_in.shape[0]
    if len(list_scales)==1:
        list_scales = [list_scales[0]] * Ng
    elif not len(list_scales) == Ng:
        return

    B_opt_out = B_opt_in.copy()
    for idx, el in enumerate(list_scales):
        B_opt_out[idx, :] = B_opt_out[idx, :] * list_scales[idx]

    return B_opt_out
