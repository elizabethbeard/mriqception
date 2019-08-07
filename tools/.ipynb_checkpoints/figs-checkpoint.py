#!/usr/bin/env python

### IMPORTS GO HERE ###
import pandas as pd
import plotly.graph_objects as go
import sys

def make_vio_plot(data, *args):
    ''' Make a violion plot of the api and user QC metrics.
    
    Args:
        data (dataframe): a dataframe including the API and USER data. Must have a column labeled 'source' with USER or API defined.
        *args (list): the list of variables a user might want displayed, defaults
        to all variables.
    
    Returns: A violin plot of each MRIQC metric, comparing the user-level data to
    the API data.
    
    '''
    
    print('Loading in dataframe...')
    
    # add stuff about whether or not variables were defined
    if len(args) > 1:
        for x in args:
            if str(x) not in data.columns:
                print('Variable name not recognized.')
                sys.exit()
        else:
            variables = str(args)
            print('Loading variables: %s' % type(variables))
    else:
        variables = data.columns
        print('Loading all variables...')
    
    sys.exit()
    # source: user/api
    # change the file from short format to long format
    df_long = pd.melt(data,id_vars='bids_name',var_name='var',value_name='values')
    
    for var_name in variables:
         # create a split violin plot for a single variable
        fig = go.Figure()
        
        # the 'my data' variable is a subset of the original df for plotting reasons
        # replace it with the actual user data
        user_data = df_long[df_long['var'] == var_name][20:40]
        
        fig.add_trace(go.Violin(x=user_data[['var']][user_data['var']==var_name]['var'],
                        y=user_data[['values']][user_data['var']==var_name]['values'],
                        legendgroup='user data', scalegroup='user data', name='user data',
                        side='negative',
                        points='all',
                        pointpos=-0.5, # where to position points
                        jitter=0.1,
                        line_color='lightseagreen')
             )
        fig.add_trace(go.Violin(x=df_long[['var']][df_long['var']==var_name]['var'],
                        y=df_long[['values']][df_long['var']==var_name]['values'],
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