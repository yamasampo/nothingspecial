import os
import pandas as pd
from collections import Counter

__version__='1.2'
__update__='180223'
__author__='Haruka Yamashita'

def slide_window(data_df, win, col_list):
    '''
    Parameter:
        window size: int
            a width of window to average over.
        col_list: list
            a list of column names for calculation.
    '''
    print('{}lines in the given data'.format(len(data_df.index)))
    print('Parameters\n\twindow size: {0}\n\tcolumns: {1}'.format(win, col_list))

    for i in range(len(data_df.index)):
        tmp_df = data_df.loc[i:win+i-1]

        for col in col_list:
            new_col = '{0}_win{1}'.format(col, win)

            data_df.loc[i+((win+1)/2), new_col] = tmp_df.mean()[col]

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

def search(df, **kwargs):
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
                print('column "{0}" filtered to be "{1}".'.format(k, i))
                res_df = f(res_df, k, i)
        elif isinstance(v, str):
            print('column "{0}" filtered to be "{1}".'.format(k, v))
            res_df = f(res_df, k, v)
        elif isinstance(v, int):
            print('column "{0}" filtered to be "{1}".'.format(k, v))
            res_df = res_df[res_df[k] == v]
    return res_df
