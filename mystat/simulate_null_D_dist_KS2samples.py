import numpy as np, matplotlib.pyplot as plt, math
from scipy import stats
from myBasic import num

__version__ = '1.0'
__updated__ = '180606'
__author__ = 'Haruka Yamashita'

sample1 = np.array([104, 109, 112, 114, 116, 118, 118, 119, 121, 123, 125, 126, 126, 128, 128, 128])
sample2 = np.array([100, 105, 107, 107, 108, 111, 116, 120, 121, 123])
n1, n2 = len(sample1), len(sample2)

def simulate_D_dist_under_null(data1, data2, rep_num, with_replace):
    # 1. Construct null dataset
    null = np.append(data1, data1)
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
    data_size, fd1, fd2 = freq_dist_2samples(list(data1), list(data2))
    # compute relative cumulative frequency distribution
    rcfd1, rcfd2 = relative_cfd(cfd(fd1), len(data1)), relative_cfd(cfd(fd2), len(data2))
    # compute statistic D
    d = maxdist(rcfd1, rcfd2)
    if show_fig:
        # show cumulative frequency distribution
        plt.style.use('default')
        plt.plot(data_range, relcfd1)
        plt.plot(data_range, relcfd2)
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

def critical_D_value(p, null_d, null_d_freq):
    # numulative frequency distribution of D statistic
    null_d_cfd = np.array(cfd(null_d_freq))
    ind1 = np.where(null_d_cfd <= 1-p)[0][-1]
    return null_d[ind1], 1- null_d_cfd[ind1]

if __name__ == '__main__':
    import sys
    rep_num = int(sys.argv[1])
    with_replace = bool(sys.argv[2])
    out_file = sys.argv[3]
    d_dist = simulate_D_dist_under_null(data1=sample1, data2=sample2, rep_num=rep_num, with_replace=with_replace)
    with open(out_file, 'a') as f:
        d_dist = [str(a) for a in d_dist]
        print(','.join(d_dist), file=f, flush=True)
