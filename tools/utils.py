import json, os, sys

import pandas as pd

from urllib.request import urlopen
from xml.dom import minidom
from json import load
from pandas.io.json import json_normalize


from pandas import read_csv
import argparse, sys


def filterIQM(df,):
    """ Load your MRIQC group tsv file and return a pandas df to then 
        use for visualizations or any other functions down the line.
    
    Args:
        infile_path (string): Path to your MRIQC tsv that you got
        from running MRIQC on your LOCAL group. However, this can
        be used to load any other downloaded/shared tsv for future 
        integration

    Returns: A pandas dataframe containing data pulled from
        the MRICQ API, but filtered to contain only your match 
        specifications.
    """
    cols = df.columns
    cols = cols.map(lambda x: x.replace(".", "_"))
    df.columns = cols

    parser = argparse.ArgumentParser(description = "Process the IQM's to sort.")

    parser.add_argument('-s', '--snr',
        help='Filter IQM: Signal-to-Noise ratio',
        type=str, metavar="[ == | <= | >=] SNR",
        dest='snr', action='append')

    parser.add_argument('-t', '--tsnr',
        help='Filter IQM: Temporal Signal-to-Noise ratio',
        type=str, metavar="[ == | <= | >=] TSNR",
        dest='tsnr', action='append')

    parser.add_argument('-d', '--dvars',
        help='Filter IQM: Temporal Derivatives Variance (DVAR)',
        type=str, metavar="[ == | <= | >=] DVAR",
        dest='dvars', action='append')

    parser.add_argument('-fw', '--fwhm',
        help='Filter IQM: Full-width half maximum smoothness',
        type=str, metavar="[ == | <= | >=] FWHM",
        dest='fwhm', action='append')

    parser.add_argument('-m', '--fd',
        help='Filter IQM: Framewise displacement',
        type=str, metavar="[ == | <= | >=] FD",
        dest='fd', action='append')

    parser.add_argument('-gx', '--gsr_x',
        help='Filter IQM: Ghost-to-Signal ratio (X axis)',
        type=str, metavar="[ == | <= | >=] gsr_x",
        dest='gsrx', action='append')

    parser.add_argument('-gy', '--gsr_y',
        help='Filter IQM: Ghost-to-Signal ratio (Y axis)',
        type=str, metavar="[ == | <= | >=] gsr_y",
        dest='gsry', action='append')

    parser.add_argument('-e', '--te',
        help='Filter Acquisition Parameter: Echo time',
        type=str, metavar="[ == | <= | >=] TE",
        dest='te', action='append')

    parser.add_argument('-r', '--tr',
        help='Filter Acquisition Parameter: Repetition time',
        type=str, metavar="[ == | <= | >=] TR",
        dest='tr', action='append')

    parser.add_argument('-T', '--Tesla',
        help='Filter Acquisition Parameter: Magnetic Field Strength',
        type=str, metavar="[ == | <= | >=] Tesla",
        dest='tesla', action='append')

    args = parser.parse_args()

    if sys.argv[1:] == 0:
        return df
    else:
        query = []
        if args.snr is not None:
            args.snr = ['snr' + s for s in args.snr]
            query += args.snr
        if args.tsnr is not None:
            args.tsnr = ['tsnr' + s for s in args.tsnr]
            query += args.tsnr
        if args.dvars is not None:
            args.dvars = ['dvars_nstd' + s for s in args.dvars]
            query += args.dvars
        if args.fwhm is not None:
            args.fwhm = ['fwhm_avg' + s for s in args.fwhm]
            query += args.fwhm
        if args.fd is not None:
            args.fd = ['fd_mean' + s for s in args.fd]
            query += args.fd
        if args.gsrx is not None:
            args.gsrx = ['gsr_x' + s for s in args.gsrx]
            query += args.gsrx
        if args.gsry is not None:
            args.gsry = ['gsr_y' + s for s in args.gsry]
            query += args.gsry
        if args.te is not None:
            args.te = ['bids_meta_EchoTime' + s for s in args.te]
            query += args.te
        if args.tr is not None:
            args.tr = ['bids_meta_RepetitionTime' + s for s in args.tr]
            query += args.tr
        if args.tesla is not None:
            args.tesla = ['bids_meta_MagneticFieldStrength' + s for s in args.tesla]
            query += args.tesla

        return df.query(" & ".join(query))


# Functions are in alphabetical order, because lazy! ##
def load_groupfile(infile_path):
    """ Load your MRIQC group tsv file and return a pandas df to then 
        use for visualizations or any other functions down the line.
    
    Args:
        infile_path (string): Path to your MRIQC tsv that you got
        from running MRIQC on your LOCAL group. However, this can
        be used to load any other downloaded/shared tsv for future 
        integration

    Returns: A pandas dataframe of your tsv file that was output by
        MRIQC. (This can also be tsv files shared or downloaded, such 
        as the ABIDE example tsv available online).
    """
    name, ext = os.path.splitext(os.path.basename(infile_path))
    if ext == '.tsv':
        df = pd.read_table(infile_path, header=0)
    elif ext == '.csv':
        df = pd.read_csv(infile_path, header=0)
    else:
        raise ValueError("File type not supported: " + ext)

    return df


def query_api(stype, filters):
    """ Query the MRIQC API using 3 element conditional statement.
    
    Args:
        stype (string): Scan type. Supported: 'bold','T1w',or 'T2w'.
        filters (list): List of conditional phrases consisting of:
            keyword to query + conditional argument + value. All
            conditions checked against API as and phrases.

    Returns: A pandas dataframe of all MRIQC entries that satisfy the 
        contitional statement (keyword condition value).
    """
    url_root = 'https://mriqc.nimh.nih.gov/api/v1/' + stype
    print('Search currently slow. Running through approximately '
          '12k possible pages...')
    print('Checking %d search phrases' % len(filters))

    # complex search line working?
    # https://mriqc.nimh.nih.gov/api/v1/bold?max_results=1000&where=bids_meta.MultibandAccelerationFactor%3C8&RepetitionTime=0.72&page=3
    # https://mriqc.nimh.nih.gov/api/v1/bold?max_results=1000&where=bids_meta.MultibandAccelerationFactor%3C8&bids_meta.RepetitionTime=0.72&page=3
    # https://mriqc.nimh.nih.gov/api/v1/bold?max_results=1000&where{"bids_meta.MultibandAccelerationFactor": {"$gte":"3"}}
    # looks like API limits at a max results of 1k
    if isinstance(filters, str):
        filters_str = filters
    elif isinstance(filters, list):
        filters_str = '&'.join(filters)
    else:
        raise ValueError("The filters can either be a list of strings or a "
                         "string")
    dfs = []
    # for phrase in args:
    #     try:
    #         del last_page
    #     except:
    #         pass

    print('\nPhrase: ' + filters_str)
    page = 0
    while True:
        # Give quick page update
        if page == 0:
            pass
        else:
            if page % 10 == 0:
                print('On page %d' % page + '...')
            else:
                pass

        ### CHANGE THIS TO OPENING A LOCAL API DUMP IN THE FUTURE ##
        page_url = url_root + '?max_results=1000&page=%d' % page
        print(page_url)

        # page_url = url_root + '?max_results=1000&where=bids_meta.' + \
        #            filters_str + '&page=%d' % page
        # print(page_url)
        with urlopen(page_url) as url:
            data = json.loads(url.read().decode())
            try:
                last_page
            except NameError:
                last_page = data['_links']['last']['href'].split('=')[-1]
                print('Searching through %s pages...' % last_page)

            dfs.append(json_normalize(data['_items']))
            if page > int(last_page):
                break
            ## TEMPORARY BREAK FOR HACKADEMY TESTING ##
            # elif page == 15:
            #     break
            else:
                page += 1

    print('Done searching!')
    print(len(dfs))
    # Concatenate all into pandas df
    df = pd.concat(dfs, ignore_index=True, sort=True)

    ## if it's OR, remove duplicates, if it's AND, *only* take duplicates??
    ## Figure out a good way to do the sorting here ##

    # remove duplicates from df
    df_unique = df.groupby('provenance.md5sum').mean()
    print(df_unique.head())

    return df_unique
