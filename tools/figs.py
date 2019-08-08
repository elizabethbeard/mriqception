#!/usr/bin/env python

# test

### IMPORTS GO HERE ###
import pandas as pd
import plotly.graph_objects as go
from ipywidgets import widgets
import sys

#def make_vio_plot(data, IQM_to_plot, data_descriptors):
def make_vio_plot(data, IQM_to_plot):
    ''' Make a violion plot of the api and user QC metrics.
    
    Args:
        data (dataframe): a dataframe including the API and USER data. Must have a column labeled 'source' with USER or API defined.
        IQM_to_plot (list): list of IQMs to plot. If you want to view all the IQMs, leave the list empty.
        data_descriptors (path-to-csv): the path to read in a csv of variable descriptions
    
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
    
    # data descriptor stuff
    print('Loading in data descriptors...')
    
    #descriptors = pd.read_csv(data_descriptors)
    
    #if not outliers:
    #    print('Please specify whether you want api outliers in your visualization or not')
    
    # source: user/api
    # change the file from short format to long format
    df_long = pd.melt(data, id_vars=['bids_name','SOURCE'],var_name='var',value_name='values')

    # make plotting dictionary for family colors
    # mediumpurple - lightskyblue - red is #A52A2A - orange is #D2691E - yellow is #DAA520 - lightseafoamgreen - 
    plot_dict = {'tsnr': ('#D2691E'), 'gcor': ('#D2691E'), 'dvars_vstd': ('#D2691E'), 'dvars_std': ('#D2691E'), # temporal
                 'dvars_nstd': ('#D2691E'), 
                 'fwhm_x': ('#DAA520'), 'fwhm_y': ('#DAA520'), 'fwhm_z': ('#DAA520'), 'fwhm_avg': ('#DAA520'), #spatial
                 'fber': ('#DAA520'), 'efc': ('#DAA520'), 
                 'cjv': ('#A52A2A'), 'cnr': ('#A52A2A'), 'qi_2': ('#A52A2A'), 'snr': ('#A52A2A'), # noise
                 'snr_csf': ('#A52A2A'), 'snr_gm': ('#A52A2A'), 'snr_wm': ('#A52A2A'), 'snr_total': ('#A52A2A'),
                 'snrd_csf': ('#A52A2A'), 'snrd_gm': ('#A52A2A'), 'snrd_wm': ('#A52A2A'), 
                 'fd_mean': ('lightseafoamgreen'), 'fd_num': ('lightseafoamgreen'), 'fd_perc': ('lightseafoamgreen'), # motion IQMs
                 'inu_med': ('lightskyblue'), 'inu_range': ('lightskyblue'), 'wm2max': ('lightskyblue'), # artifact IQMs
                 'aor': ('mediumpurple'), 'aqi': ('mediumpurple'), 'dummy_trs': ('mediumpurple'), 'gsr_x': ('mediumpurple'), # other
                 'gsr_y': ('mediumpurple'), 'qi_1': ('mediumpurple'), 'rpve_csf': ('mediumpurple'), 'rpve_gm': ('mediumpurple'),
                 'rpve_wm': ('mediumpurple'), 'tpm_overlap_csf': ('mediumpurple'), 'tpm_overlap_gm': ('mediumpurple'),
                 'tpm_overlap_wm': ('mediumpurple'), 
                 'icvs_csf': ('#00008B'), 'icvs_gm': ('#00008B'), 'icvs_wm': ('#00008B'), # descriptive
                 'summary_bg_k': ('#00008B'), 'summary_bg_mad': ('#00008B'), 'summary_bg_mean': ('#00008B'),
                 'summary_bg_median': ('#00008B'), 'summary_bg_n': ('#00008B'), 'summary_bg_p05': ('#00008B'),
                 'summary_bg_p95': ('#00008B'), 'summary_bg_stdv': ('#00008B'), 
                 'summary_csf_k': ('#00008B'), 'summary_csf_mad': ('#00008B'), 'summary_csf_mean': ('#00008B'),
                 'summary_csf_median': ('#00008B'), 'summary_csf_n': ('#00008B'), 'summary_csf_p05': ('#00008B'),
                 'summary_csf_p95': ('#00008B'), 'summary_csf_stdv': ('#00008B'), 
                 'summary_fg_k': ('#00008B'), 'summary_fg_mad': ('#00008B'), 'summary_fg_mean': ('#00008B'),
                 'summary_fg_median': ('#00008B'), 'summary_fg_n': ('#00008B'), 'summary_fg_p05': ('#00008B'),
                 'summary_fg_p95': ('#00008B'), 'summary_fg_stdv': ('#00008B'), 
                 'summary_gm_k': ('#00008B'), 'summary_gm_mad': ('#00008B'), 'summary_gm_mean': ('#00008B'),
                 'summary_gm_median': ('#00008B'), 'summary_gm_n': ('#00008B'), 'summary_gm_p05': ('#00008B'),
                 'summary_gm_p95': ('#00008B'), 'summary_gm_stdv': ('#00008B'), 
                 'summary_wm_k': ('#00008B'), 'summary_wm_mad': ('#00008B'), 'summary_wm_mean': ('#00008B'),
                 'summary_wm_median': ('#00008B'), 'summary_wm_n': ('#00008B'), 'summary_wm_p05': ('#00008B'),
                 'summary_wm_p95': ('#00008B'), 'summary_wm_stdv': ('#00008B') 
                 }
    
    
    var_name = variables[0] # the default first variable
   
    # create a split violin plot for a single variable
    fig = go.Figure()
    
    fig.add_trace(go.Violin(x=df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='USER'),'var'],
                    y=df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='USER'),'values'],
                    legendgroup='user data', scalegroup='user data', name='user data',
                    side='negative',
                    points='all',
                    pointpos=-0.5, # where to position points
                    jitter=0.1,
                    line_color=plot_dict.get(var_name, 'red')) # plot same-family IQMs in same color
         )
    fig.add_trace(go.Violin(x=df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='API'),'var'],
                    y=df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='API'),'values'],
                    legendgroup='api', scalegroup='api', name='api',
                    side='positive',
                    line_color='rgb(58,54,54)')
         )
    # update characteristics shared by all traces
    fig.update_traces(meanline_visible=True,
              box_visible=True)
    fig.update_layout(autosize=False,
                     width=600,
                     height=600)
    fig.update_layout(template="plotly_white") # make background white
    
    # create a figure widget in order to show the dropdown menu
    fig_widget = go.FigureWidget(fig)
    
    
    # create a dropdown menu widget for the variable name
    dropdown_widget = widgets.Dropdown(
            options=list(df_long['var'].unique()),
            value=var_name,
            description='IQM:',
            )
        
    def response(change):
        var_name = dropdown_widget.value
        with fig_widget.batch_update():
            fig_widget.data[0].x = df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='USER'),'var']
            fig_widget.data[0].y = df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='USER'),'values']
            fig_widget.data[0].line = {'color': plot_dict.get(var_name, 'red')}
            fig_widget.data[1].x = df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='API'),'var']
            fig_widget.data[1].y = df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='API'),'values']
            

    dropdown_widget.observe(response, names="value")
    
    return(dropdown_widget, fig_widget)

        #print description of figure
        #print(dictionary.get(var_name))
