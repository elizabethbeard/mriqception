import json, os, sys

import pandas as pd

from urllib.request import urlopen
from xml.dom import minidom
from json import load
from pandas.io.json import json_normalize

def filterIQM(apidf, modality, filter_list):
    """ Loads the API info and filters based on user-provided
        parameters. Filter parameters should be a list of strings
        and string formats should be "(VAR) (Operator) (Value)".
        Example: ['TR == 3.0'] or ['TR > 1.0','FD < .3']
        Note: Each element in each string is SPACE separated!

    Args:
        apidf (pandas dataframe): Pandas df of the API info.
        modality ('string'): Type of MRI scan queried.
                             Options: ['Bold' 'T1w' 'T2w'].
        filter_list = (list): List of argument strings that will
        be joined by ampersands to use pandas query function.

    Returns: A pandas dataframe containing data pulled from
        the MRICQ API, but filtered to contain only your match
        specifications.
    """
    cols = apidf.columns
    cols = cols.map(lambda x: x.replace(".", "_").lowercase())
    apidf.columns = cols

    query = []
    mod = modality.lowercase()

    if mod == 'bold':
        expected_filters = {'snr':'snr','tsnr':'tsnr',
                'dvar':'dvars_nstd','fd':'fd_mean',
                'fwhm':'fwhm_avg','tesla':'bids_meta_magneticfieldstrength',
                'gsr_x':'gsr_x','gsr_y':'gsr_y',
                'te':'bids_meta_echotime','tr':'bids_meta_repetitiontime'}
    elif mod == 't1w':
        expected_filters = {'snr':'snr_total', 'snrg':'snr_gm', 'srnw':'snr_wm',
                'snrc':'snr_csf', 'cnr':'cnr', 'efc':'efc',
                'fwhm':'fwhm_avg','tesla':'bids_meta_magneticfieldstrength',
                'te':'bids_meta_echotime','tr':'bids_meta_repetitiontime'}
    elif mod == 't2w':
        expected_filters = {'snr':'snr_total', 'snrg':'snr_gm', 'srnw':'snr_wm',
                'snrc':'snr_csf', 'cnr':'cnr', 'efc':'efc',
                'fwhm':'fwhm_avg','tesla':'bids_meta_magneticfieldstrength',
                'te':'bids_meta_echotime','tr':'bids_meta_repetitiontime'}

    if all(isinstance(x,str) for x in filter_list):
        filter_list = [x.lower() for x in filter_list]
    else:
        raise ValueError('filter_list contains items other than strings')

    filter_check = list(expected_filters.keys())

    for filt in filter_list:
        var = filt.split(' ')[0]
        op = filt.split(' ')[1]
        val = filt.split(' ')[2]
        if var in filter_check:
            filt_str = expected_filters[var] + op + val
            query.append(filt_str)
        else:
            raise Exception(var + 'is not found in the available IQMs')

    filtered_df = apidf.query(' & '.join(query))

    return filtered_df

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

def merge_dfs(userdf, filtered_apidf):
    """ Merges the user/group dataframe and the filtered API dataframe
        while adding a groupby variable. Name is "SOURCE". User entries
        are "USER" and API entries are "API".

    Args:
        udf (pandas df): User MRIQC tsv converted to pandas dataframe
        apidf (pandas df): API info, filtered and stored in padas
            dataframe.

    Returns: A merged pandas dataframe containing the user group info and
        the filtered API info. A "groupby" header called "SOURCE" is added
        with a "USER" or "API" entry for easy sorting/splitting.
    """
    userdf['SOURCE']='USER'
    filtered_apidf['SOURCE']='API'

    merged_df = pd.concat([userdf,filtered_apidf], sort=True).fillna(0)
    return merged_df

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
