#!/usr/bin/env python

import argparse,datetime,os,sys,time

import pandas as pd

from tools import load_groupfile, query_api, filterIQM, merge_dfs, make_vio_plot

here = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))

group_file = os.path.join(here,'test_data', 'group2_bold.tsv')
filter_list = ['TR > 2.0','FD < .3']
modality = 'bold'

T1apicsv = os.path.join(here, 'demo_api', 'T1w_demo.csv')
T2apicsv = os.path.join(here, 'demo_api', 'T2w_demo.csv')
boldapicsv = os.path.join(here, 'demo_api', 'bold_demo.csv')

if modality == 'T1w':
    api_file = T1apicsv
elif modality == 'T2w':
    api_file = T1apicsv
elif modality == 'bold':
    api_file = boldapicsv

# load user csv as df #
userdf = load_groupfile(group_file)

# load and filter api csv as df #
apidf = pd.read_csv(api_file)
filtered_apidf = filterIQM(apidf,filter_list)

# merge dataframes together #
vis_ready_df = merge_dfs(userdf, filtered_apidf)

IQM_to_plot = ['fwhm_avg','fber']

v = make_vio_plot(vis_ready_df, IQM_to_plot)

# print(vis_ready_df.head)

# for col in userdf.columns:
#     print(col)
# print(list(userdf.columns))
# # print(userdf.head)


# for col in apidf.columns:
#     print(col)
# print(list(apidf.columns))
# # print(apidf.head)

# for col in filtered_apidf.columns:
#     print(col)
# print(list(filtered_apidf.columns))
# # print(filtered_apidf.head)