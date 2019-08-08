#!/usr/bin/env python
"""
Call this program with:
    -g full path to your group csv or tsv you want to compare to API data.)
    -t scan type (modality) to compare to: bold, T1w, or T2w)
    -? filter/search phrase - argument in unknown format...
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
                                         argparse.ArgumentDefaultsHelpFormatter)
    # Check for arguments. #
    if len(sys.argv[1:]) == 0:
        print('\nArguments required. Use -h option to print FULL usage.\n')

    arg_parser.add_argument('-g', metavar='GROUP_FILE', action='store',
                            type=os.path.abspath, required=True,
                            help=('FULL path to your group csv/tsv file - '
                                  'the output from MRIQC.'),
                            dest='group_file'
                            )
    # arg_parser.add_argument('-s', metavar='SEARCH_PHRASE', action='store', type=str,
    #                         required=True, help=('Search phrase to filter API query.'
    #                                              'Format: xxxx xxxxx xxxxxx xxxxxx'),
    #                         dest='search_phrase'
    #                         )
    # arg_parser.add_argument('-t', metavar='SCAN_TYPE', action='store', type=str,
    #                         choices=['bold', 'T1w', 'T2w'], required=False,
    #                         default='T1w',
    #                         help=('Scan type to query. Can choose from bold,'
    #                               ' T1w, or T2w.'),
    #                         dest='scan_type'
                            # )
    args = arg_parser.parse_args()

    #################################################
    ## Script Argument Verification and Assignment ##
    #################################################
    if os.path.isfile(args.group_file):
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


    filter_list = ['TR > 1.0','FD < .3']
    modality = 'bold'

    here = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
    T1apicsv = os.path.join(here, 'demo_api', 'T1w_demo.csv')
    T2apicsv = os.path.join(here, 'demo_api', 'T2w_demo.csv')
    boldapicsv = os.path.join(here, 'demo_api', 'bold_demo.csv')

    if modality == 'T1w':
        group_file = T1apicsv
    elif modality == 'T2w':
        group_file = T1apicsv
    elif modality == 'bold':
        group_file = boldapicsv

    # load user csv as df #
    userdf = load_groupfile(group_file)

    # load and filter api csv as df #
    apidf = pd.read_csv(group_file)
    filtered_apidf = filterIQM(,apidf,filter_list)

    # merge dataframes together #
    vis_ready_df = merge_dfs(userdf, filtered_apidf)







    # result_df = query_api(args.scan_type,'MultibandAccelerationFactor>3','RepetitionTime>1')
    # # result_df = query_api(args.scan_type, ['MultibandAccelerationFactor>3', 'EchoTime>1'])
    # result_df = query_api(args.scan_type, 'MultibandAccelerationFactor>3&EchoTime>1')

    ## Scater plot/visualization functions would go below here and pass result_df as well as loaded_df pandas dataframes
    # something like this:
    # scatter(loaded_df, result_df)


    full_runtime = time.time() - start_time
    print('\nFull Script Runtime: ', datetime.timedelta(seconds=full_runtime), '\n')
if __name__ == '__main__':
    sys.exit(main())
