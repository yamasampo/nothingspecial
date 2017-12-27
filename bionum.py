import pandas as pd

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
        tmp_df = dat_df.loc[i:win+i-1]

        for col in col_list:
            new_col = '{0}_win{1}'.format(col, win)

            dat_df.loc[i+((win+1)/2), new_col] = tmp_df.mean()[col]
