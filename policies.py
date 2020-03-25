#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Fri Mar 20 13:03:03 2020

@author: vbokharaie
"""

def str_policy_info():
    """
    Return a string with info about defined basic policies.

    Returns
    -------
    str_out : str
        info on basic policies.

    """
    # text should be manually updated based on policies defined in get_Bopt
    str_out = """
    ***************************************************************************************
    HOW EACH POLICY IS DEFINED?
    ***************************************************************************************
    ---------------------------------------------------------------------------------------
    Below you can see the policies I have defined.

    Obviously, any other polciy can be easily defined in the code,
        when you find where they are defined.

    list_scales shows the scale for contacts rates in each group as compared to uncontained
        hence the values are in [0,1] range.

    Age groups are 0-10, 10-20, ..., 70-80 and 80+
    ---------------------------------------------------------------------------------------

    # these policies are defined intuitively,
    # all suggestions to make them more accurate are welcome
    #------------------------
    'Schools_closed':
        w_kids = 0.1
        list_scales = [w_kids, w_kids, 1, 1, 1, 1, 1, 1, 1, ]
    #------------------------
    'Adults_self_isolate':
        w_adults = 0.4
        list_scales = [1, 1, w_adults, w_adults, w_adults, w_adults, w_adults, 1, 1, ]
    #------------------------
    'Lockdown':
        w_kids = 0.1
        w_adults = 0.2
        w_old = 0.25
        list_scales = [w_kids, w_kids, w_adults, w_adults, w_adults, w_adults, w_adults, w_old, w_old, ]
    #------------------------
    'Elderly_stay_home':
        w_kids = 1.0
        w_adults = 1.0
        w_old = 0.25
        list_scales = [w_kids, w_kids, w_adults, w_adults, w_adults, w_adults, w_adults, w_old, w_old, ]
    #------------------------
    'All_self_isolate':
        w_kids = 0.2
        w_adults = 0.2
        w_old = 0.5
        list_scales = [w_kids, w_kids, w_adults, w_adults, w_adults, w_adults, w_adults, w_old, w_old, ]
    #------------------------
    'All_s_isolate_but_kids':
        w_kids = 1
        w_adults = 0.2
        w_old = 0.5
        list_scales = [w_kids, w_kids, w_adults, w_adults, w_adults, w_adults, w_adults, w_old, w_old, ]
    #------------------------
    'Lockdown_but_kids':
        w_kids = 1
        w_adults = 0.2
        w_old = 0.25
        list_scales = [w_kids, w_kids, w_adults, w_adults, w_adults, w_adults, w_adults, w_old, w_old, ]

    """
    return str_out

def get_Bopt(file_data_opt, country='Germany', policy='Uncontained', ):
    """
    Return the contact rates for the specified model (SIS/SIR), country, pre-defined policy.

    Parameters
    ----------
    file_data_opt : TYPE
        DESCRIPTION.
    country : TYPE, optional
        DESCRIPTION. The default is 'Germany'.
    policy : TYPE, optional
        DESCRIPTION. The default is 'Uncontained'.
     : TYPE
        DESCRIPTION.

    Returns
    -------
    B_opt : TYPE
        DESCRIPTION.

    """
    # load original (uncontained) Bopt obtained from optimisation performed in matlab
    # variable names in saved files is 'B_opt_' + country, example: B_opt_Germany
    from utils import load_mat, scale_B_opt
    varname = 'B_opt_' + country
    B_opt_orig = load_mat(file_data_opt, varname)


    # these policies are defined intuitively,
    # all suggestions to make them more accurate are welcome
    #------------------------
    if policy == 'Schools_closed':
        w_kids = 0.1
        list_scales = [w_kids, w_kids, 1, 1, 1, 1, 1, 1, 1, ]
    #------------------------
    elif policy == 'Schools_Offices_closed':
        w_kids = 0.1
        w_adults = 0.5
        w_old = 1
        list_scales = [w_kids, w_kids, w_adults, w_adults, w_adults, w_adults, w_adults, w_old, w_old, ]
    #------------------------
    elif policy == 'Adults_self_isolate':
        w_adults = 0.4
        list_scales = [1, 1, w_adults, w_adults, w_adults, w_adults, w_adults, 1, 1, ]
    #------------------------
    elif policy == 'Lockdown':
        w_kids = 0.1
        w_adults = 0.1
        w_old = 0.25
        list_scales = [w_kids, w_kids, w_adults, w_adults, w_adults, w_adults, w_adults, w_old, w_old, ]
    #------------------------
    elif policy == 'Kids_Elderly_stay_home':
        w_kids = 0.1
        w_adults = 1.0
        w_old = 0.25
        list_scales = [w_kids, w_kids, w_adults, w_adults, w_adults, w_adults, w_adults, w_old, w_old, ]
    #------------------------
    elif policy == 'Social_Distancing':
        w_kids = 0.2
        w_adults = 0.2
        w_old = 0.5
        list_scales = [w_kids, w_kids, w_adults, w_adults, w_adults, w_adults, w_adults, w_old, w_old, ]
    #------------------------
    elif policy == 'All_s_isolate_but_kids':
        w_kids = 1
        w_adults = 0.2
        w_old = 0.5
        list_scales = [w_kids, w_kids, w_adults, w_adults, w_adults, w_adults, w_adults, w_old, w_old, ]
    #------------------------
    elif policy == 'Lockdown_but_kids':
        w_kids = 1
        w_adults = 0.2
        w_old = 0.25
        list_scales = [w_kids, w_kids, w_adults, w_adults, w_adults, w_adults, w_adults, w_old, w_old, ]
    elif not policy == 'Uncontained':
        raise('Policy was not recognized.')
    if policy == 'Uncontained':
        B_opt = B_opt_orig
    else:
        B_opt = scale_B_opt(B_opt_orig, list_scales)

    return B_opt

def get_pop_distr(country):
    """
    Return population distribution in each country.

    in age ranges of each 10 years till 80 and 80+
    obtained from www.populationpyramid.net

    Parameters
    ----------
    country : str
        name of the country.

    Returns
    -------
    list_out : list of floats
    percentage of popultaion in each age-group.
        age groups are 0-10, 10-20, ..., 70-80, 80+

    """
    dict_pop = {}
    dict_pop['China'] = [11.9, 11.6, 13.5, 15.6, 15.6, 15.0, 10.4, 4.7, 1.7]
    dict_pop['Italy'] = [8.4, 9.5, 10.1, 11.8, 15.3, 15.7, 12.3, 9.8, 7.3]
    dict_pop['Iran'] = [17.4, 13.9, 15.5, 20.0, 13.6, 9.7, 6.2, 2.7, 1.0]
    dict_pop['SouthKorea'] = [8.4, 9.5, 13.3, 14.0, 16.3, 16.4, 12.1, 6.6, 3.5]
    dict_pop['Germany'] = [9.2, 9.6, 11.2, 12.8, 12.5, 16.2, 12.4, 9.1, 6.9]

    list_out = dict_pop[country]
    return list_out

def Bopt_normalised_2_country(Bopt, list_age_distr):
    """
    Convert the general optimised B matrix to one adapted for a certain country.

    Parameters
    ----------
    Bopt : 2D numpy array
        A Ng x Ng matrix of normalised contact rates obtained from optimisation scheme.
    list_age_distr : list of floats
        population distribution for each age range in each country.

    Returns
    -------
    Bopt_country : 2D numpy array
        Matrix of contact rates

    """
    import numpy as np
    Ng = Bopt.shape[0]
    Bopt_country = Bopt.copy()
    assert len(list_age_distr) != Ng, 'Look at this: dimension mismatch!!! :/'
    for cc in np.arange(Ng):
        Bopt_country[cc,:] = Bopt_country[cc,:] * list_age_distr[cc]
    return Bopt_country