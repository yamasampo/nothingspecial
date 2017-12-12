import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_means_CIs(data_df, rep_num, category_column, data_column, rep_column='rep',
                  xlabel=None, ylabel=None, label=None, categories=None, style=None, xticklabels=None,
                  ci=95, width=0.3, space=0.5, alpha=1, color='#e41a1c', error_kw={'ecolor': '0.3', 'elinewidth':'1'},
                  show_fig=False, save_fig=False, fig_fname=None, return_fmt='array', **kwargs):
    '''
    values that will be plotted should be contained
    as being specified by category and rep values in data_df
    '''
    ## Remove duplications from sets of category and rep columns
    if not categories:
        categories = set(data_df[category_column].tolist())
    data = data_df.drop_duplicates([category_column, rep_column, data_column])
    print(len(data.index))
    print(categories)
    if len(data.index) != len(categories)*rep_num:
        raise Exception('Given data is not unique by given category and replication columns. Input data length is {0} inspite expected length is {1}.'.format(len(data.index), len(categories)*rep_num))

    ## Get mean and CI
    means_list = []
    lower_ci_list = []
    upper_ci_list = []

    exp_rep_list = [i for i in range(rep_num)]
    percentile = (1-(ci/100))/2

    for c in categories:
        rep_list = list(set(data[data[category_column] == c]['rep'].tolist()))
        rep_list.sort()
        if exp_rep_list != rep_list:
            print(rep_list)
            raise Exception('replication error')

        v = data[data[category_column] == c][data_column]
        means_list.append(v.mean())
        lower_ci_list.append(v.quantile(percentile))
        upper_ci_list.append(v.quantile(1-percentile))

    means_array = np.array(means_list)
    lower_ci_array = np.array(lower_ci_list)
    upper_ci_array = np.array(upper_ci_list)
    lower_yerr = means_array - lower_ci_array
    upper_yerr = upper_ci_array - means_array
    yerrs = [lower_yerr, upper_yerr]

    df = pd.DataFrame({'mean': means_array, 'lower_ci': lower_ci_array, 'upper_ci': upper_ci_array})

    if show_fig or save_fig:

        if style:
            plt.style.use(style)
        fig, ax = plt.subplots()
        d = space + width
        index = np.linspace(1, 1+d*len(means_array), len(means_array),endpoint=True)

        ax.bar(index, means_array, width=width, alpha=alpha, color=color, yerr=yerrs,
               error_kw=error_kw, label=label)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xticks(index)
        if xticklabels:
            ax.set_xticklabels(xticklabels)
        else:
            ax.set_xticklabels(categories)
        ax.legend()

        fig.tight_layout()
        if save_fig:
            plt.savefig(fig_fname, format = 'png', dpi=300)
            df.to_csv(os.path.join(os.path.dirname(fig_fname), os.path.basename(fig_fname).split('.')[0]+'.csv'), index=False)

        plt.show()

    if return_fmt == 'array':
        return  [means_array, yerrs]
    elif return_fmt == 'df':
        return df

def compare_means_bar(data_df, rep_num, category_column, data_column, compare,
                      xlabel, ylabel, colors=[], rep_column='rep', categories=[], xticklabels=None,
                      ci=95, width=0.3, space=0.5, alpha=1, style=None, title=None, label=[],
                      tfontsize=18, xlfontsize=15, ylfontsize=15, lfontsize=10, yfontsize=9,
                      error_kw={'ecolor': '0.3', 'elinewidth':'1'}, save_fig=False, fig_fname=None):
    '''
    data that will be compared should be specified by rep and category(xlabel),
    but except compare category (label) and bins(collection of comparings).

    '''

    data_df.reset_index(inplace=True, drop=True)
    color_list = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf']
    summary_df = pd.DataFrame(index=[], columns=[])
    column_list = []

    if not categories:
        categories = list(set(data_df[category_column].tolist()))
        categories.sort()
    
    for k, v in compare.items():

        if not colors:
                colors=color_list[:len(v)]
        if len(colors) != len(v):
            raise Exception('length of colors should be {}.'.format(len(v)))

        if style:
            plt.style.use(style)
        fig, ax = plt.subplots()

        if v == 'all':
            v = list(set(data_df[k].tolist()))
            v.sort()

        # for each items to be compared
        for i, a in enumerate(v):

            print(k, a)
            # specify a series of one of compared data
            data = data_df.loc[data_df[data_df[k] == a].index]
            means_array = []
            yerrs = []

            means_array, yerrs = get_means_CIs(data_df=data, rep_num=rep_num,
                                               category_column=category_column, return_fmt='array',
                                               data_column=data_column, categories=categories)
            print('mean array:', means_array)
            print('yerr arrays:',yerrs)

            d = space + len(v)*width
            index = np.linspace(1, 1+d*len(means_array), len(means_array),endpoint=True)
            print(len(index))
            x = index + width*i
            if label:
                l = label[i]
            else:
                l = a

            # make bar plot
            ax.bar(x, means_array, width=width, alpha=alpha, color=colors[i],
                   yerr=yerrs, error_kw=error_kw, label=l)
            # make summary DataFrame
            lower_yerr = yerrs[0]
            upper_yerr = yerrs[1]
            lower_ci = means_array - lower_yerr
            upper_ci = means_array + upper_yerr

            # if len(summary_df.index) == 0:
            #     summary_df = pd.DataFrame({'{}_mean'.format(l): means_array, '{}_lower_ci'.format(l): lower_ci, '{}_upper_ci'.format(l): upper_ci})
            summary_df['{}_mean'.format(l)] = means_array
            summary_df['{}_lower_ci'.format(l)] = lower_ci
            summary_df['{}_upper_ci'.format(l)] = upper_ci
            column_list.append('{}_mean'.format(l))
            column_list.append('{}_lower_ci'.format(l))
            column_list.append('{}_upper_ci'.format(l))

        if title:
            ax.set_title(title, fontsize=tfontsize)
        ax.set_xlabel(xlabel, fontsize=xlfontsize)
        ax.set_ylabel(ylabel, fontsize=ylfontsize)
        # set xticklabels
        ax.set_xticks(index+(width/2)*(len(v)-1))
        if xticklabels:
            ax.set_xticklabels(xticklabels)
        else:
            ax.set_xticklabels(categories)
        ax.tick_params(labelsize=yfontsize)
        ax.legend(fontsize=lfontsize)

        fig.tight_layout()

        summary_df = summary_df.ix[:, column_list]
        if save_fig:
            plt.savefig(fig_fname, format = 'png', dpi=300)
            summary_df.to_csv(os.path.join(os.path.dirname(fig_fname), os.path.basename(fig_fname).split('.')[0]+'.csv'), index=False)

        plt.show()

    return summary_df

def compare_means_bar_loop(data_df, rep_num, category_column, data_column, compare, series,
                      xlabel, ylabel, colors=[], rep_column='rep', categories=[],
                      ci=95, width=0.3, space=0.5, alpha=1, title=None, label=[], style=None,
                      tfontsize=18, xlfontsize=15, ylfontsize=15, lfontsize=10, yfontsize=9,
                      error_kw={'ecolor': '0.3', 'elinewidth':'1'}, save_fig=False, fig_fname_pre=None):
    '''
    Compare means of data that is specified by category and replication columns and
    loop this calculation by data in given series.

    If you get an error that "Given data is not unique by given category and replication columns.",
    it means that the way to collect series was incompatible with this method.
    In that case, please change series parameter.
    '''

    concat_list = []

    for kc, vc in compare.items():

        for ac in vc:
            concat_list.append(data_df[data_df[kc] == ac])

    tmp_df = pd.concat(concat_list)

    for ks, vs, in series.items():

        if vs == 'all':
            vs = list(set(tmp_df[ks].tolist()))
            vs.sort()

        for a in vs:
            title = ks+str(a)
            if fig_fname_pre:
                fig_fname = fig_fname_pre+'_'+title+'.png'
            else:
                fig_fname = None

            compare_means_bar(data_df=tmp_df[tmp_df[ks] == a], rep_num=rep_num,
                              category_column=category_column, data_column=data_column,
                              compare=compare, xlabel=xlabel, ylabel=ylabel, style=style,
                              colors=colors, rep_column=rep_column, categories=categories,
                              ci=ci, width=width, space=space, alpha=alpha, title=title,
                              label=label, error_kw=error_kw, tfontsize=tfontsize, xlfontsize=xlfontsize,
                              ylfontsize=ylfontsize, lfontsize=lfontsize, yfontsize=yfontsize,
                              save_fig=save_fig, fig_fname=fig_fname)

if '__name__' == '__main__':
	get_means_CIs()
