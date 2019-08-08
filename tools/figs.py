#!/usr/bin/env python

### IMPORTS GO HERE ###
import pandas as pd
import plotly.graph_objects as go
import sys

def make_vio_plot(data, IQM_to_plot):
    ''' Make a violion plot of the api and user QC metrics.
    
    Args:
        data (dataframe): a dataframe including the API and USER data. Must have a column labeled 'source' with USER or API defined.
        *args (list): the list of variables a user might want displayed, defaults
        to all variables.
    
    Returns: A violin plot of each MRIQC metric, comparing the user-level data to
    the API data.
    
    '''
    print('Loading in dataframe...')
    
    # variable names we might want to list
    qc_var_list = ['aor','aqi','dummy_trs','dvars_nstd','dvars_std','dvars_vstd',
                    'efc','fber','fd_mean','fd_num','fd_perc','fwhm_avg','fwhm_x','fwhm_y',
                    'fwhm_z','gcor','gsr_x','gsr_y','size_t','size_x','size_y','size_z','snr',
                    'spacing_tr','spacing_x','spacing_y','spacing_z','summary_bg_k','summary_bg_mad',
                    'summary_bg_mean','summary_bg_median','summary_bg_n','summary_bg_p05',
                    'summary_bg_p95','summary_bg_stdv','summary_fg_k','summary_fg_mad',
                    'summary_fg_mean','summary_fg_median','summary_fg_n','summary_fg_p05',
                    'summary_fg_p95','summary_fg_stdv','tsnr']
    
    # add stuff about whether or not variables were defined
    if len(IQM_to_plot) == 0:
        variables = qc_var_list
        print('Loading all variables...')
    elif len(IQM_to_plot) > 0:
        for x in IQM_to_plot:
            if str(x) not in qc_var_list:
                print('Variable name not recognized.')
                sys.exit()
            else:
                pass
        variables = IQM_to_plot
        print('Loading variables: %s' %variables)

    # source: user/api
    # change the file from short format to long format
    df_long = pd.melt(data,id_vars=['bids_name','SOURCE'],var_name='var',value_name='values')

    for var_name in variables:
        # create a split violin plot for a single variable
        fig = go.Figure()

        # # the 'my data' variable is a subset of the original df for plotting reasons
        # # replace it with the actual user data
        # user_data = df_long[df_long['var'] == var_name][20:40]
               
        fig.add_trace(go.Violin(x=df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='USER'),'var'],
                        y=df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='USER'),'values'],
                        legendgroup='user data', scalegroup='user data', name='user data',
                        side='negative',
                        points='all',
                        pointpos=-0.5, # where to position points
                        jitter=0.1,
                        line_color='lightseagreen')
             )
        fig.add_trace(go.Violin(x=df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='API'),'var'],
                        y=df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='USER'),'values'],
                        legendgroup='api', scalegroup='api', name='api',
                        side='positive',
                        line_color='mediumpurple')
             )
        # update characteristics shared by all traces
        fig.update_traces(meanline_visible=True,
                  box_visible=True) #scale violin plot area with total count
        fig.show()
        

        #print description of figure
        #print(dictionary.get(var_name))