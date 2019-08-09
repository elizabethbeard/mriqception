#!/usr/bin/env python

### IMPORTS GO HERE ###
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from ipywidgets import widgets
import sys

def make_vio_plot(data, IQM_to_plot, data_descriptors, outliers=False):
    ''' Make a violin plot of the api and user QC metrics.

    Args:
        data (dataframe): a dataframe including the API and USER data. Must have a column labeled 'source' with USER or API defined.
        IQM_to_plot (list): list of IQMs to plot. If you want to view all the IQMs, leave the list empty.
        data_descriptors (path-to-csv): the path to read in a csv of variable descriptions
        outliers (Boolean): if True, remove outliers. Default is to leave outliers in

    Returns: A violin plot of each MRIQC metric, comparing the user-level data to
    the API data.

    '''
    print('Loading in dataframe...')

    # variable names we might want to list
    qc_var_list = ["aor",
"aqi",
"cjv",
"cnr",
"dummy_trs",
"dvars_nstd",
"dvars_std",
"dvars_vstd",
"efc",
"fber",
"fber",
"fd_mean",
"fd_num",
"fd_perc",
"fwhm_avg",
"fwhm_avg",
"fwhm_x",
"fwhm_y",
"fwhm_z",
"gcor",
"gsr_x",
"gsr_y",
"icvs_csf",
"icvs_gm",
"icvs_wm",
"inu_med",
"inu_range",
"qi_1",
"qi_2",
"rpve_csf",
"rpve_gm",
"rpve_wm",
"snr",
"snr_csf",
"snr_gm",
"snr_total",
"snr_wm",
"snrd_csf",
"snrd_gm",
"snrd_total",
"snrd_wm",
"summary_bg_k",
"summary_bg_mad",
"summary_bg_mean",
"summary_bg_median",
"summary_bg_n",
"summary_bg_p05",
"summary_bg_p95",
"summary_bg_stdv",
"summary_csf_k",
"summary_csf_mad",
"summary_csf_mean",
"summary_csf_median",
"summary_csf_n",
"summary_csf_p05",
"summary_csf_p95",
"summary_csf_stdv",
"summary_fg_k",
"summary_fg_mad",
"summary_fg_mean",
"summary_fg_median",
"summary_fg_n",
"summary_fg_p05",
"summary_fg_p95",
"summary_fg_stdv",
"summary_gm_k",
"summary_gm_mad",
"summary_gm_mean",
"summary_gm_median",
"summary_gm_n",
"summary_gm_p05",
"summary_gm_p95",
"summary_gm_stdv",
"summary_wm_k",
"summary_wm_mad",
"summary_wm_mean",
"summary_wm_median",
"summary_wm_n",
"summary_wm_p05",
"summary_wm_p95",
"summary_wm_stdv",
"tpm_overlap_csf",
"tpm_overlap_gm",
"tpm_overlap_wm",
"tsnr",
"wm2max"]

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

    descriptors = pd.read_csv('./tools/iqm_descriptions.csv')

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
                 'fd_mean': ('#66CDAA'), 'fd_num': ('#66CDAA'), 'fd_perc': ('#66CDAA'), # motion IQMs
                 'inu_med': ('#6495ED'), 'inu_range': ('#6495ED'), 'wm2max': ('#6495ED'), # artifact IQMs
                 'aor': ('#9932CC'), 'aqi': ('#9932CC'), 'dummy_trs': ('#9932CC'), 'gsr_x': ('#9932CC'), # other
                 'gsr_y': ('#9932CC'), 'qi_1': ('#9932CC'), 'rpve_csf': ('#9932CC'), 'rpve_gm': ('#9932CC'),
                 'rpve_wm': ('#9932CC'), 'tpm_overlap_csf': ('#9932CC'), 'tpm_overlap_gm': ('#9932CC'),
                 'tpm_overlap_wm': ('#9932CC'),
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
    API_data = df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='API'),'values']


    def remove_outliers_from_api(API_data,outliers):

        # identify some outliers
        if outliers:
            q75, q25 = np.percentile(API_data, [75 ,25])
            iqr = q75 - q25
            min_out = q25-1.5*iqr
            max_out = q75+1.5*iqr

            #if outliers are present, replace them with NaN
            API_data[API_data > max_out] = np.nan
            API_data[API_data < min_out] = np.nan

        return API_data

    API_data = remove_outliers_from_api(API_data,outliers)

    def make_range(data, variable):
        mini_data = data.loc[(data['var']==variable)]
        max_point = mini_data.max().values[3]
        min_point = mini_data.min().values[3]
        spread = max_point-min_point
        point_range = [(min_point-(.2*spread)), (max_point+(.2*spread))]
        return point_range
                    
    # create a split violin plot for a single variable
    fig = go.Figure()

    fig.add_trace(go.Violin(x=df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='USER'),'var'],
                    y=df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='USER'),'values'],
                    legendgroup='user data', scalegroup='user data', name='user data',
                    side='negative',
                    points='all',
                    pointpos=-0.5, # where to position points
                    jitter=0.1,
                    hovertext=df_long['bids_name'],
                    line_color=plot_dict.get(var_name, 'red')) # plot same-family IQMs in same color)
         )
    fig.add_trace(go.Violin(x=df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='API'),'var'],
                    y=API_data,
                    legendgroup='api', scalegroup='api', name='api',
                    side='positive',
                    line_color='rgb(58,54,54)')
         )
    # update characteristics shared by all traces
    definition = descriptors.loc[(descriptors['iqm_name']==var_name),"iqm_definition"].tolist()[0]
    fig.update_traces(meanline_visible=True,
              box_visible=True)
    fig.update_layout(autosize=False,
                     width=700,
                     height=700,
                     margin=go.layout.Margin(t=0),
                     xaxis=go.layout.XAxis(title = go.layout.xaxis.Title(text=definition,font=dict(size=12))))
    fig.update_yaxes(range=make_range(df_long, var_name))
    fig.update_layout(template="plotly_white") # make background white

    # create a figure widget in order to show the dropdown menu
    fig_widget = go.FigureWidget(fig)

    # create a dropdown menu widget for the variable name
    dropdown_widget = widgets.Dropdown(
            options=variables,
            value=var_name,
            description='IQM:',
            )
    # define the changes that occur based on the choice in the dropdown menu
    def response(change):
        var_name = dropdown_widget.value

        API_data = df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='API'),'values']
        API_data = remove_outliers_from_api(API_data,outliers)
        user_data = df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='USER'),'values']

        with fig_widget.batch_update():
            fig_widget.data[0].x = df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='USER'),'var']
            fig_widget.data[0].y = user_data
            fig_widget.data[0].line = {'color': plot_dict.get(var_name, 'red')}
            fig_widget.data[1].x = df_long.loc[(df_long['var']==var_name)&(df_long['SOURCE']=='API'),'var']
            fig_widget.data[1].y = API_data
            definition = descriptors.loc[(descriptors['iqm_name']==var_name),"iqm_definition"].tolist()[0]
            fig_widget.layout.xaxis.title = {'text': definition, 'font': {'size':12}}
            fig_widget.layout.yaxis.range = make_range(df_long, var_name)

    dropdown_widget.observe(response, names="value")

    return(dropdown_widget, fig_widget)


    #print description of figure

    #print(dictionary.get(var_name))
