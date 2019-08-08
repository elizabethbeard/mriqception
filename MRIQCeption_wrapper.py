#!/usr/bin/env python
"""
Call this program with:
    -i full path to your group csv or tsv you want to compare to API data.)
    -t scan type (modality) to compare to: bold, T1w, or T2w)
    -f List of filters for query)
__authors__ = [Elizabeth C. Beard, Stephanie Rossi Chen,Stephanie N. DeCross,
               Damion V. Demeter, Sofía Fernández-Lozano, Chris Foulon,
               Helena M. Gellersen, Ayelet Gertsovski, Estée Rubien-Thomas,
               Saren H. Seeley, Catherine R. Walsh]
__version__ = '0.01'
__maintainer__ = '??'
__email__ = '??@??.edu'
__status__ = 'pre-alpha'
"""

import argparse,datetime,os,sys,time
import pandas as pd
from tools import load_groupfile, query_api, filterIQM, merge_dfs, make_vio_plot

#################################################
##             MAIN SCRIPT ENTRY               ##
#################################################

here = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
PROG = 'QCeption'
prog_desc = """%(prog)s:
A utility for doing QC, on your group QC report, using the MRIQC "global" data. Originally written \
during Neurohackademy, 2019.
""" % {'prog': PROG}


def main(argv=sys.argv):
    arg_parser = argparse.ArgumentParser(description=prog_desc,
                                         formatter_class=
                                         argparse.RawTextHelpFormatter)

    arg_parser.add_argument('-i', '--input', metavar='GROUP_FILE', action='store',
            type=os.path.abspath, required=True,
            help=("""
            FULL path to your group csv/tsv file - the output from MRIQC.
            """),
            dest='group_file'
            )

    arg_parser.add_argument('-t', '--type', metavar='SCAN_TYPE', action='store',
            type=str, choices=['bold', 'T1w', 'T2w'], required=True,
            help=("""
            Scan type to query. Can choose from bold, T1w, or T2w.
            """),
            dest='scan_type'
            )

    arg_parser.add_argument('-f', '--filter', metavar='FILTER_LIST', action='append',
            type=str, required=True,
            help=("""
            Strings to filter the queried database.
            Several filters can be given at the same time.
            The string formats should be:
            -f "(VAR) (Operator) (Value)"; Example:
            "-f 'TR == 3.0' " or "-f 'TR > 1.0' -f 'TR < 3.0' -f 'FD < .3' "
            Note: Each element in each string is separated by SPACES
            The IQMs depend on the --type argument given:
            BOLD:
               {SNR; TSNR; DVAR; FD; FWHM; GSR_X; GSR_Y;
                   TESLA; TE; TR}
            T1W | T2W:
               {SNR; SNR_GM; SNR_WM; SNR_CSF; CNR; EFC; FWHM;
                   TESLA; TE; TR}
            """),
            dest='filter_list'
            )

    args = arg_parser.parse_args()

    #################################################
    ## Script Argument Verification and Assignment ##
    #################################################
    # Check for arguments. #
    if len(sys.argv) == 1:
        arg_parser.print_help()
        sys.exit(0)
    elif os.path.isfile(args.group_file):
        pass
    else:
        print('The groupfile you are trying to use was not found. Exiting...')
        sys.exit()

    #################################################
    ##          Global Variable Assignment         ##
    #################################################
    start_time = time.time()
    time.sleep(1)
    today_date = datetime.datetime.now().strftime('%m%d%Y')

    # print('Querying API for ' + args.scan_type + ' scans.')

    #  filter_list = ['TR > 1.0','FD < .3']
    #  modality = 'bold'

    here = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
    T1apicsv = os.path.join(here, 'demo_api', 'T1w_demo.csv')
    T2apicsv = os.path.join(here, 'demo_api', 'T2w_demo.csv')
    boldapicsv = os.path.join(here, 'demo_api', 'bold_demo.csv')

    if args.scan_type.lower() == 't1w':
        group_file = T1apicsv
    elif args.scan_type.lower() == 't2w':
        group_file = T1apicsv
    elif args.scan_type.lower() == 'bold':
        group_file = boldapicsv

    # load user csv as df #
    userdf = load_groupfile(group_file)

    # load and filter api csv as df #
    apidf = pd.read_csv(group_file)

    # Make the filter_list
    filter_list = []
    filtered_apidf = filterIQM(apidf, args.scan_type, args.filter_list)

    # merge dataframes together #
    vis_ready_df = merge_dfs(userdf, filtered_apidf)
    #  return filtered_apidf

if __name__ == '__main__':
    sys.exit(main())
