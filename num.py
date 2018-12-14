import os
import re
import pandas as pd
from collections import Counter
import numpy as np

__version__ = '2.3'
__updated__ = '180529'
__author__ = 'Haruka Yamashita'

def slide_window(data_df, win_size, dat_col_list):
    '''
    Parameters
    ----------
    window size: int
        a width of window to average over.
    col_list: list
        a list of column names to be calculated.
    '''
    print('{} lines in the given data'.format(len(data_df.index)))
    print('Parameters\n\twindow size: {0}\n\tcolumns: {1}'.format(win_size, dat_col_list))

    for col in dat_col_list:
        new_col = '{0}_win{1}'.format(col, win_size)

        for i in range(len(data_df.index)):
            tmp_df = data_df.loc[i:win_size+i-1]
            data_df.loc[i+((win_size+1)/2), new_col] = tmp_df[col].mean()

def step(df, step):
    index = [i for i in range(len(df.index)) if i % step == 0]

    return df.loc[index, :]

def count_occurrence(df, column, out_path=None, by=None, to_file=True, **kwargs):
    '''
    Returns Dataframe containing items and its occurence.
    Parameters
    ----------
        df: DataFrame(pandas)
            input data. You can give a path to comma delemited table to df.
        column: str
            a column name that you want count items in
        **kwargs:
            will give to pd.read_csv(). Please use the same paramters as pd.read_csv() for **kwargs.
    '''
    # check output path
    if to_file:
        if not out_path:
            out_path = './{0}_count.csv'.format(column)
        if os.path.isfile(out_path):
            raise Exception('{} already exists.'.format(out_path))

    # get initial DataFrame
    if isinstance(df, str):
        df = pd.read_csv(df, **kwargs)

    # If "by" is specified, select items which have the key.
    if isinstance(by, tuple):
        dat = df[df.loc[:, by[0]] == by[1]]
        c = '{0}_{1}'.format(by[1], column)
    else:
        dat = df
        c = column

    # count items
    res_df = pd.DataFrame(list(dict(Counter(dat.loc[:, column])).items()), columns=[c, 'count'])
    if not to_file:
        return res_df.sort_values(by=c)
    else:
        res_df.sort_values(by=c, inplace=True).to_csv(out_path, index=False)
        print('saved to {}'.format(out_path))
        return res_df

def search_items_df(df, **kwargs):
    '''
    Search rows which have specifies items from a given dataframe.
    Please pass key words for searching to **kwargs.
    For example, if you want to get items that is greater than equal (>=)
    100 in column "A", please specify **kwargs as "A=gte100". Please see below for details.
    If nothing passed to **kwargs, return input dataframe.
    Paramters
    ---------
        df: DataFrame (pandas)
            input dataframe
        **kwargs:
            key is for column, value is for filtering values (items)
            You can use indicators below for filtering way.
            "gt" for ">"
            "gte" for ">="
            "lt" for "<"
            "lte" for "<="
            "ne" for "!="
            "c/" for "contains"
            "" for "=="
            If you pass tuple to value, this function search and filter items recursively.
    '''
    res_df = df

    def f(res_df, k, v):
        if v == '*':
            pass
        elif re.search('^gt\d+', v):
            v = float(re.search('^gt(\d+\.*\d*)$', v).group(1))
            res_df = res_df[res_df[k] > v]
        elif re.search('^gte\d+', v):
            v = float(re.search('^gte(\d+\.*\d*)$', v).group(1))
            res_df = res_df[res_df[k] >= v]
        elif re.search('^lt\d+', v):
            v = float(re.search('^lt(\d+\.*\d*)$', v).group(1))
            res_df = res_df[res_df[k] < v]
        elif re.search('^lte\d+', v):
            v = float(re.search('lte(\d+\.*\d*)$', v).group(1))
            res_df = res_df[res_df[k] <= v]
        elif re.search('^ne\d+', v):
            v = float(re.search('ne(\d+\.*\d*)$', v).group(1))
            res_df = res_df[res_df[k] != v]
        elif re.search('^c\/', v):
            v = re.search('^c\/(.+)\/$', v).group(1)
            res_df = res_df[res_df[k].str.contains(v)]
        else:
            res_df = res_df[res_df[k] == v]
        return res_df

    for k,v in kwargs.items():
        if isinstance(v, tuple):
            for i in v:
                res_df = f(res_df, k, i)
        elif isinstance(v, str):
            res_df = f(res_df, k, v)
        elif isinstance(v, int):
            res_df = res_df[res_df[k] == v]

    return res_df

def adjust_average(data, average=1000, divisor=None, integer=False):

    if divisor:
        const = average / divisor
    else:
        const = average * len(data) / sum(data)

    if integer:
        out = [round(const * a) for a in data]
    else:
        out = [const * a for a in data]

    return out

def bootstrap(data, rep_num, output='matrix'):
    '''
    Returns a list of means of resampled data.

    Parameters
    ----------
    data: list
        array-like data
    rep_num: int
        number of replications. bootstrap will be repeated this number of times.
    output: str, 'mean' or 'matrix'
        output info. if mean was specified, only means of bootstrapped data will 
        be outputted.

    '''
    data = np.array(data)
    boot_dat = []

    for i in range(rep_num):
        index = np.random.choice(len(data), len(data), replace=True)
        index.sort()
        if output == 'index':
            boot_dat.append(index)
            continue

        new_data = data[index]
        if output == 'mean':
            boot_dat.append(np.mean(new_data))
        elif output == 'matrix':
            boot_dat.append(np.array(new_data))

    if len(boot_dat) != rep_num:
        raise Exception('bootstrapped data has excess or lack of data.')

    boot_array = np.array(boot_dat)
    # boot_array.sort()
    return boot_array

def median_CIs(data, ci=95):
    lower_ci = np.percentile(data, 100-ci)
    median = np.median(data)
    upper_ci = np.percentile(data, ci)

    return lower_ci, median, upper_ci

def bootstrap_df(df, rep_num, ci=95):
    '''
    Returns df containing median and confidence intervals.
    Parameters
    ----------
        df: DataFrame (pandas)
            rows of df should be composed of data of each sample and columns should be categories.
        rep_num: int
            number of replicates. bootstrap will be performed rep_num times.
        ci: int (0<= ci <= 100)
            percentile for confidence intervals.

    Returns
    -------
        stat_df: DataFrame (pandas)
            stat_df is composed of a table containing arrays of median, lower ci and upper ci.
    '''
    # drop NaN from df
    df2 = df.dropna(how='any')

    cnt = 0
    out_list=[]
    print('Bootstrap', end=' ', flush=True)
    for i, row in df2.iteritems():
        # extract data for each category
        data = np.array(row)

        # resample data
        boot_data = bootstrap(data, rep_num)

        # compute median and CI
        quantiles = median_CIs(boot_data, ci)
        out_list.append([a for a in [np.mean(data), np.mean(boot_data),
                                     quantiles[0], quantiles[1], quantiles[2]]])
        cnt += 1
        if cnt % 100 == 0:
            print('.', end='', flush=True)

    print(' Done.', flush=True)

    stat_df = pd.DataFrame(out_list, columns=['orig_mean', 'boot_mean',
                                          'ci_{}'.format(100-ci), 'median',
                                          'ci_{}'.format(ci)])
    return stat_df

def bootstrap_df2(df, bin_col, data_col, rep_num, ci=95):

    bin_list = list(set(df[bin_col].tolist()))
    bin_list.sort()

    cnt = 0
    out_list = []
    print('Bootstrap')
    print('bin column:\t', bin_col)
    print('data column:\t', data_col)
    for b in bin_list:
        # extract data for each category
        data = np.array(df[df[bin_col] == b][data_col])

        # resample transcripts
        boot_data = bootstrap(data, rep_num)

        quantiles = median_CIs(boot_data, ci)
        out_list.append(
            [a for a in [b, np.mean(data), np.mean(boot_data),
                         quantiles[0], quantiles[1], quantiles[2]]]
        )
        cnt += 1
        if cnt % 100 == 0:
            print('.', end='', flush=True)
    stat_df = pd.DataFrame(
        out_list,
        columns=['bin', 'orig_mean', 'boot_mean',
                 'ci_{}'.format(100-ci), 'median','ci_{}'.format(ci)]
    )
    return stat_df

def myround(a, ndigits=2):
    n = 10 ** ndigits
    return (a * n * 2 + 1) // 2 / n
