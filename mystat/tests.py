import numpy as np, matplotlib.pyplot as plt, math
import warnings
from collections import namedtuple
from scipy import stats
from myBasic import num

__version__ = '1.0'
__author__ = 'Haruka Yamashita'

__all__ = ['ks_2samp_test']

Ks_2sampResult = namedtuple('Ks_2sampResult', ('statistic', 'pvalue'))

def ks_2samp_test(data1=[], data2=[], fd1=[], fd2=[]):
    if data1 and data2:
        data1 = np.sort(data1)
        data2 = np.sort(data2)
        n1 = data1.shape[0]
        n2 = data2.shape[0]
        data_all = np.sort(np.concatenate([data1, data2]))
        cdf1 = np.searchsorted(data1, data_all, side='right') / n1
        cdf2 = np.searchsorted(data2, data_all, side='right') / n2

    elif fd1 and fd2:
        if len(fd1) != len(fd2):
            raise ValueError('Frequency distributions should be the same lengths of arrays.')

        n1 = sum(fd1)
        n2 = sum(fd2)
        cdf1 = np.cumsum(fd1) / n1
        cdf2 = np.cumsum(fd2) / n2

    else:
        raise ValueError('Input data1 and data2, or fd1 and fd2.')

    d = np.max(np.absolute(cdf1 - cdf2))
    # Note: d absolute not signed distance
    en = np.sqrt(n1 * n2 / (n1 + n2))
    try:
        prob = stats.kstwobign.sf((en + 0.12 + 0.11 / en) * d)
    except Exception:
        warnings.warn('This should not happen! Please open an issue at '
                    'https://github.com/scipy/scipy/issues and provide the code '
                    'you used to trigger this warning.\n')
        prob = 1.0

    return Ks_2sampResult(d, prob)
