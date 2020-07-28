import json
import requests
import re

import pandas as pd
import dateparser

from urllib.request import urlopen
from pandas.io.json import json_normalize


def backend_query_api(stype, filters):
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


def mriqc_url(modality, filters='', page_number=0, max_page_results=1000):
    url_root = 'https://mriqc.nimh.nih.gov/api/v1/' + modality
    page = '&page={}'.format(page_number)
    max_results = '?max_results=%s' % max_page_results

    filters_prefix = "&where="
    if isinstance(filters, str):
        if not filters.startswith(filters_prefix):
            filters_str = filters_prefix + filters
        else:
            filters_str = filters
    elif isinstance(filters, list):
        filters_str = filters_prefix + '&'.join(filters)
    else:
        raise TypeError("filters must be either a string of a list of strings")

    page_url = url_root + max_results + filters_str + page

    return page_url


def request_page(url):
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.get(url, headers=headers)
    return r


def database_info(url):
    data = request_page(url).json()
    page = data['_meta']['page']
    if len(data['_items']) == 0:
        raise ValueError("Page {} is empty".format(page))
    try:
        print(re.findall("page=(\d*)&", data['_links']['last']['href'])[0])
    except KeyError:
        print("no last page attribute")
    print(data['_links']['self']['href'])
    # last_page = re.findall("page=(\d*)&", data['_links']['last']['href'])[0]
    # self_page = re.findall("page=(\d*)&", data['_links']['self']['href'])[0]
    # total_results = data['_meta']['total']
    # page = data['_meta']['page']
    # return last_page, self_page, data['_meta']# page, data


def store_page(data, out_csv=None, append=True):
    df = json_normalize(data['_items'])
    if out_csv is not None:
        if append:
            with open(out_csv, 'a') as f:
                df.to_csv(f)
        else:
            df.to_csv(out_csv)

    return df


def pull_pages(modality, filters='', page_number=-1, max_page_results=1000,
                  out_csv=None, append=True):
    page_url = mriqc_url(modality, filters, page_number, max_page_results)
    request_res = request_page(page_url)
    data = request_res.json()
    page = data['_meta']['page']
    if len(data['_items']) == 0:
        raise ValueError("Page {} is empty".format(page))
    if page == 0:
        # continue
        print('todo')
    try:
        last_page = re.findall(
            r"page=(\d*)&", data['_links']['last']['href']
        )[0]
    except KeyError:
        print("Page {} is the last page".format(page))
    '''
    In[29]: data.keys()
    Out[29]: dict_keys(['_items', '_links', '_meta'])
    data['_items'] is a list of dictionaries
    
    In[30]: data['_links'].keys()
    Out[30]: dict_keys(['parent', 'self', 'next', 'last', 'prev'])
    
    In [31]: data['_meta'].keys()
    Out[31]: dict_keys(['page', 'max_results', 'total'])
    '''
    df = store_page(data, out_csv, append)
    # print(type(data))
    # print(str(data))
    return df


# curl -X GET "https://mriqc.nimh.nih.gov/api/v1/bold?max_results=10&where=bids_meta.MultibandAccelerationFactor%3C8&bids_meta.RepetitionTime=0.72&page=3" -H "accept: application/json"
#
# curl -X GET "https://mriqc.nimh.nih.gov/api/v1/bold?max_results=10&where=bids_meta.MultibandAccelerationFactor>3&bids_meta.RepetitionTime=0.72&bids_meta.EchoTime=0.03&page=3" -H "accept: application/json" > ../toto.json
#
# url1 = "https://mriqc.nimh.nih.gov/api/v1/bold?max_results=130&where=bids_meta.MultibandAccelerationFactor>3&bids_meta.RepetitionTime=0.72&bids_meta.EchoTime=0.03&page=0"
# url2 = "https://mriqc.nimh.nih.gov/api/v1/bold?max_results=130&where=bids_meta.MultibandAccelerationFactor>3&bids_meta.RepetitionTime=0.72&bids_meta.EchoTime=0.03&page=86060"
# payload = open("payload.json")
# headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
# r = requests.get(url1, headers=headers)
# r2 = requests.get(url2)

url_root = 'https://mriqc.nimh.nih.gov/api/v1/bold'
response = requests.get(
    url_root,
    params={'page': '3',
            'where': 'bids_meta.MultibandAccelerationFactor==3',
            'where': 'bids_meta.RepetitionTime==1'},
)
print(response.url)
print(len(response.json()['_items']))
print(response.json()['_meta'])
data = response.json()
def tata(data):
    for v in data['_items']:
        try:
            r1 = v['bids_meta']['RepetitionTime']
        except KeyError:
            r1 = None
        try:
            r2 = v['bids_meta']['MultibandAccelerationFactor']
        except KeyError:
            r2 = None
        try:
            r3 = v['bids_meta']['EchoTime']
        except KeyError:
            r3 = None
        if r1 is not None:
            print(str(r1))
        else:
            print('None')
        if r2 is not None:
            print(str(r2))
        else:
            print('None')
        if r3 is not None:
            print(str(r3))
        else:
            print('None')
        print()

# https://mriqc.nimh.nih.gov/api/v1/bold?max_results=25&where={%22bids_meta.RepetitionTime%22:2,%22bids_meta.task_id%22:%22balloonanalogrisktask%22}
# "Mon, 9 May 2016 12:00:00 GMT"
# https://mriqc.nimh.nih.gov/api/v1/bold?max_results=25&where={"_updated":"Sun, 04 Jun 2017 04:19:33 GMT"}
# https://mriqc.nimh.nih.gov/api/v1/bold?max_results=25&where={"_updated":{"$gt":"Sun, 04 Jun 2017 04:19:33 GMT"}}

# https://mriqc.nimh.nih.gov/api/v1/bold?max_results=25&where={"bids_meta.RepetitionTime":{"$gt":2}}
# https://mriqc.nimh.nih.gov/api/v1/bold?max_results=25&where={"_updated":{"&gt":"Mon, 9 May 2016 12:00:00 GMT"}}


# date_obj = datetime.strptime(date_input, '%m/%d/%Y')
# from datetime import datetime
# import dateutil

date_input = '07/15/2017 10:55:50'

date_obj = dateparser.parse(date_input)
good_format = date_obj.strftime('%a, %d %b %Y %H:%M:%S GMT')
print(good_format)

filter = '{"_updated":{"$gt":"%s"}}' % good_format
url = mriqc_url('bold', filter, 3, 30)

r = request_page(url)

keys = ['_updated', '_created']

gt_str = '{"_updated":{"$gt":"Sun, 04 Jun 2017 04:19:33 GMT"}, "_updated":{"$lt":"Sun, 11 Jun 2017 04:19:33 GMT"}, "bids_meta.RepetitionTime":2}'
gt_list = ["_updated>06/04/2017 04:19:33"]

url = mriqc_url('bold', gt_str, max_page_results=30)
r = request_page(url)
r.status_code

len(r.json()['_items'])
print(str([item['_updated'] for item in r.json()['_items']]))
print(str([item['bids_meta']['RepetitionTime'] for item in r.json()['_items']]))


def aq(string):
    """
    Add the quotes " characters around a string if they are not already there.
    Parameters
    ----------
    string : str
        just a string to be formatted
    Returns
    -------
        str
        a string with " character at the beginning and the end
    """
    tmp = string
    if not string.startswith('"'):
        tmp = '"' + tmp
    if not string.endswith('"'):
        tmp = tmp + '"'
    return tmp


def find_date(arg):
    if isinstance(arg, str):
        re.findall(r'\"_updated\":((\d|-)+)*', gt_str)
        re.search(r'\"_updated\":((\d|-)+)*', gt_str)
    elif isinstance(arg, list):
        print("todo")
    else:
        raise TypeError("arg can be either a string or a list")


def add_date(s):
    """

    Parameters
    ----------
    s : str
        a date string it can be in any format handled by the datetime package

    Returns
    -------
        str
        date string in mongodb format
    """
    date_obj = dateparser.parse(s)
    mongodb_format = date_obj.strftime('%a, %d %b %Y %H:%M:%S GMT')

    return aq(mongodb_format)


def format_operator(op):
    """
    Translate operators into mongodb syntax operators
    Parameters
    ----------
    op : str
        an operator in python/bash/mongodb format

    Returns
    -------
    op_out : str
        operator in mongodb syntax
    """
    # op_list = ['>', '>=', '<', '<=', '=', '==', ':', '<>', '!=']
    # op_list_letters_dollar = ['$' + s for s in op_list_letters]
    op_list_letters = ['gt', 'ge', 'le', 'lt', 'eq', 'ne']

    op_dict_invert = {
        '$gt': ['>', 'gt'],
        '$gte': ['>=', 'ge', '$ge'],
        '$lt': ['<', 'lt'],
        '$lte': ['<=', 'le', '$le'],
        '$eq': ['=', '==', ':', 'eq'],
        '$ne': ['<>', '!=', 'ne']
    }
    for key in op_dict_invert.keys():
        op_dict_invert[key].append(key)

    # associate all the operators to mongodb operators
    op_dict = dict((v, k) for k in op_dict_invert for v in op_dict_invert[k])
    for k in op_dict_invert.keys():
        op_dict[k] = k

    return aq(op_dict[op])


def add_operator(operator_str, string):
    """

    Parameters
    ----------
    operator_str : str
        an operator to be added to the string
    string : str
        a string shaped like "key:val"
    Returns
    -------
    element : str
        "key":{"operator":"val"}
    """
    tmp = string.split(':')
    key = tmp[0]
    val = tmp[1]
    element = '%s:{%s:%s}' % (aq(key), format_operator(operator_str), aq(val))
    return element


def add_filter(req_filter, request=''):
    """

    Parameters
    ----------
    req_filter : str
        string shaped like "key":"val" or "key":{"op":"val"}
    request : str (optional)
        request string shaped like: {"key1":{"op1":"val1"}[,"key2":{"op2":"val2"}]*}

    Returns
    -------
        str
        a string shaped like {["key_i":{"op_i":"val_i"},]*, "key", "val"}
    """
    if request == "":
        return "{%s}" % req_filter
    else:
        return request[:-1] + ',' + req_filter + '}'
