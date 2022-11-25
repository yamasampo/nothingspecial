import math

import numpy as np
import matplotlib.pyplot as plt

from scipy import stats

from nothingspecial import num

sample1 = np.array([104, 109, 112, 114, 116, 118, 118, 119, 121, 123, 125, 126, 126, 128, 128, 128])
sample2 = np.array([100, 105, 107, 107, 108, 111, 116, 120, 121, 123])
n1, n2 = len(sample1), len(sample2)

def simulate_D_dist_under_null(data1, data2, rep_num, with_replace):
    # 1. Construct null dataset
    null = np.append(data1, data2)
    d_dist = []
    for i in range(rep_num):
        # 2. Regenerate 2 samples
        re1, re2 = resample_2subsets(null, with_replace, len(data1), len(data2))
        # 3. Compute statistic D
        d = data2maxdist(re1, re2, show_fig=False)
        d_dist.append(d)
    return d_dist

def resample_2subsets(null, with_replace, n1, n2):
    if with_replace:
        re_null = bootstrap(null)
    else:
        re_null = permutation(null)
    return re_null[:n1], re_null[n1:n1+n2+1]

def bootstrap(data):
    '''Return a list of resampled data'''
    index = np.random.choice(len(data), len(data), replace=True)
    return data[index]

def permutation(data):
    '''Return numpy array of resampled data'''
    index = np.random.choice(len(data), len(data), replace=False)
    return data[index]

def data2maxdist(data1, data2, show_fig=False):
    # compute frequency distribution
    data_range, fd1, fd2 = freq_dist_2samples(list(data1), list(data2))
    # compute relative cumulative frequency distribution
    rcfd1, rcfd2 = relative_cfd(cfd(fd1), len(data1)), relative_cfd(cfd(fd2), len(data2))
    # compute statistic D
    d = maxdist(rcfd1, rcfd2)
    if show_fig:
        # show cumulative frequency distribution
        plt.style.use('default')
        plt.plot(data_range, rcfd1)
        plt.plot(data_range, rcfd2)
        plt.title('Relative cumulative frequency distribution')
        plt.xlabel('Data')
        plt.show()
        plt.close()
    return d

def freq_dist_2samples(sample1, sample2):
    mi = min(min(sample1) , min(sample2))
    ma = max(max(sample1) , max(sample2))
    data_range = [i for i in range(mi, ma+1)]
    fd1 = []
    fd2 = []
    for a in data_range:
        fd1.append(sample1.count(a))
        fd2.append(sample2.count(a))
    return data_range, fd1, fd2

def cfd(fd):
    cf = 0
    cfd = []
    for v in fd:
        cf += v
        cfd.append(cf)
    return cfd

def relative_cfd(cfd, data_size):
    return np.array(cfd) / data_size

def maxdist(cfd1, cfd2):
    '''Returns maximum value of distance between CFDs of two given data'''
    cfd_diff = cfd1 - cfd2
#     ix = np.where(cfd_diff == max(abs(cfd_diff))) # cannot specify index from absolute value
    return max(abs(cfd_diff))

### Functions to summarize simulation data ###
def bin_num(data_size):
    return int(num.myround(1 + math.log2(data_size), 0))

def show_d_prob_dist(d_dist):
    # calculate relative frequencies
    res = stats.relfreq(d_dist, numbins=bin_num(len(d_dist)))
    # calculate space of values for x
    x = res.lowerlimit + np.linspace(0, res.binsize*res.frequency.size, res.frequency.size)
    # plot relative frequency histogram
    plt.style.use('default')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.bar(x, res.frequency, width=res.binsize)
    ax.set_title('Frequency distribution of statistic D')
    ax.set_xlabel('statistic D')
    ax.set_xlim([0, 1.2])
    plt.show()
    plt.close()
    return x, res

def ks_pvalue(d, n1, n2):
    return stats.kstwobign.sf(ks_z(d, ne(n1, n2)))

def pks(z):
    if z < 0:
        raise Exception('bad z')
    elif z == 0:
        return 0
    elif z < 1.18:
        y = math.exp(-1.23370055013616983/(z**2)) # 1.23370055013616983 = pi**2 / 8
        return 2.25675833419102515 * math.sqrt(-math.log(y)) * (y + pow(y, 9) + pow(y, 25) + pow(y, 49)) # 2.25675833419102515 = 4/math.sqrt(math.pi)

def qks(z):
    '''Returns p-value for a given statistic z. This function is almost equivalent with scipy.stats.kstwobign.sf() function.
    Reference
    ---------
        Press, W.H. et al. 2007, Numerical Recipes, section 14.3
    '''
    if z < 0:
        raise Exception('bad z')
    elif z == 0:
        return 1
    elif z < 1.18:
        return 1 - pks(z)
    else:
        x = math.exp(-2*z**2)
        return 2 * (x-pow(x, 4)+pow(x, 9))

def ks_z(d, ne):
    return (math.sqrt(ne) + 0.12 + 0.11/math.sqrt(ne))*d

def ne(n1, n2):
    return n1*n2 / (n1 + n2)

if __name__ == '__main__':
    import sys
    rep_num = int(sys.argv[1])
    with_replace = bool(sys.argv[2])
    in_file = sys.argv[3]
    # parse input data
    data1, data2 = [], []
    with open(in_file, 'r') as f:
        for i, l in enumerate(f):
            if i == 0:
                data1 = np.array([int(a) for a in l[:-1].split(',')])
            elif i == 1:
                data2 = np.array([int(a) for a in l[:-1].split(',')])
    print('Input file:\t', in_file)
    print('\tdata 1:\t', data1)
    print('\tdata 2:\t', data2)
    out_file = sys.argv[4]
    d_dist = simulate_D_dist_under_null(data1=data1, data2=data2, rep_num=rep_num, with_replace=with_replace)
    with open(out_file, 'a') as f:
        d_dist = [str(a) for a in d_dist]
        print(','.join(d_dist), file=f, flush=True)
