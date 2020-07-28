# Import functions #
import argparse,datetime,os,sys,time

import pandas as pd

from tools import load_groupfile, query_api, filterIQM, merge_dfs, make_vio_plot

# Arguments #

# laziness helper
here = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))


# path to input of local data from MRIQC on your own dataset
group_file = os.path.join(here,'test_data', 'group2_bold.tsv')

# scan type to query the API for [bold, T1w, T2w]
modality = 'bold'

# any scan parameters that you want to filter the API search results by
"""Current possible filters:
   SNR, TSNR, DVAR, FD,
   FWHM, Tesla, gsr_x, gsr_y, TE, TR
   NOTE: Only working as *and* right now!
"""
filter_list = ['TR > 2.0','FD < .3']

# IQM variables to visualize
IQM_to_plot = ['fwhm_avg','fber']

userdf = load_groupfile(group_file)
T1apicsv = os.path.join(here, 'demo_api', 'T1w_demo.csv')
T2apicsv = os.path.join(here, 'demo_api', 'T2w_demo.csv')
boldapicsv = os.path.join(here, 'demo_api', 'bold_demo.csv')

if modality == 'T1w':
    api_file = T1apicsv
elif modality == 'T2w':
    api_file = T1apicsv
elif modality == 'bold':
    api_file = boldapicsv

# This will return a pandas dataframe with data from all scans of the given scan type
# with the given parameters

apidf = pd.read_csv(api_file)
filtered_apidf = filterIQM(apidf,filter_list)

vis_ready_df = merge_dfs(userdf.copy(), filtered_apidf.copy())


