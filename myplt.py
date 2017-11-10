import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_means_CIs(data_df, rep_num, category_column, data_column, rep_column='rep',
                  xlabel=None, ylabel=None, label=None, categories=None, style=None,
                  ci=95, width=0.3, space=0.5, alpha=1, color='#e41a1c', error_kw={'ecolor': '0.3'},
                  show_fig=False, save_fig=False, fig_fname=None):
    '''
    values that will be plotted should be contained
    as being specified by category and rep values in data_df
    '''
    ## Remove duplications from sets of category and rep columns
    if not categories:
        categories = set(data_df[category_column].tolist())
    data = data_df.drop_duplicates([category_column, rep_column, data_column])
    if len(data.index) != len(categories)*rep_num:
        raise Exception('Given data is not unique by given category and replication columns.')

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

    if show_fig or save_fig:

        if style:
            plt.style.use(style)
        fig, ax = plt.subplots()
        d = space + width
        index = np.arange(1, len(means_array)*d+1, d)

        ax.bar(index, means_array, width=width, alpha=alpha, color=color, yerr=yerrs,
               error_kw=error_kw, label=label)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xticks(index)
        ax.set_xticklabels(categories)
        ax.legend()

        fig.tight_layout()
        if save_fig:
            plt.savefig(fig_fname, format = 'png', dpi=300)

        plt.show()

    return [means_array, yerrs]

def compare_means_bar(data_df, rep_num, category_column, data_column, compare,
                      xlabel, ylabel, colors=[], rep_column='rep', categories=[],
                      ci=95, width=0.3, space=0.5, alpha=1, style=None, title=None, label=[],
                      error_kw={'ecolor': '0.3'}, save_fig=False, fig_fname=None):
    '''
    data that will be compared should be specified by rep and category(xlabel),
    but except compare category (label) and bins(collection of comparings).

    '''

    if not categories:
        categories = list(set(data_df[category_column].tolist()))
        categories.sort()
    color_list = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf']

    for k, v in compare.items():

        if not colors:
                colors=color_list[:len(v)]
        if len(colors) != len(v):
            raise Exception('length of colors should be {}.'.format(len(v)))

        if style:
            plt.style.use(style)
        fig, ax = plt.subplots()

        for i, a in enumerate(v):

            print(k, a)
            data = data_df.loc[data_df[data_df[k] == a].index]

            means_array = []
            yerrs = []
            means_array, yerrs = get_means_CIs(data_df=data, rep_num=rep_num,
                                               category_column=category_column,
                                               data_column=data_column, categories=categories)

            print('mean array:', means_array)
            print('yerr arrays:',yerrs)

            d = space + len(v)*width
            index = np.arange(1, len(means_array)*d+1, d)
            x = index + width*i
            if label:
                l = label[i]
            else:
                l = a

            ax.bar(x, means_array, width=width, alpha=alpha, color=colors[i],
                   yerr=yerrs, error_kw=error_kw, label=l)

        if title:
            ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        print(index)
        ax.set_xticks(index+(width/2)*(len(v)-1))
        ax.set_xticklabels(categories)
        ax.legend()

        fig.tight_layout()
        if save_fig:
            plt.savefig(fig_fname, format = 'png', dpi=300)

        plt.show()

def compare_means_bar_loop(data_df, rep_num, category_column, data_column, compare, series,
                      xlabel, ylabel, colors=[], rep_column='rep', categories=[],
                      ci=95, width=0.3, space=0.5, alpha=1, title=None, label=[], style=None,
                      error_kw={'ecolor': '0.3'}, save_fig=False, fig_fname_pre=None):
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
            concat_list.append(dat_df[dat_df[kc] == ac])

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
                              label=label,error_kw=error_kw, save_fig=save_fig, fig_fname=fig_fname)

if '__name__' == '__main__':
	get_means_CIs()
