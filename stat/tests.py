import numpy as np, matplotlib.pyplot as plt, math
import warnings
from collections import namedtuple
from scipy.stats import distributions, rankdata, mannwhitneyu
from myBasic import num

__version__ = '1.2'
__author__ = 'Haruka Yamashita'

__all__ = ['ks_2samp_test']

def fd2data(x, fd, scaler=1):
    data = []
    fd = [num.myround(a, 0) for a in scaler * np.array(fd)]
    for i, d in enumerate(x):
        for _ in range(int(fd[i])):
            data.append(d)
    if len(data) != sum(fd):
        print(len(data), sum(fd))
        raise Exception('')
    return data

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

    elif len(fd1) > 0 and len(fd2) > 0:
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
        prob = distributions.kstwobign.sf((en + 0.12 + 0.11 / en) * d)
    except Exception:
        warnings.warn('This should not happen! Please open an issue at '
                    'https://github.com/scipy/scipy/issues and provide the code '
                    'you used to trigger this warning.\n')
        prob = 1.0

    return Ks_2sampResult(d, prob)

# codes below are from scipy v1.2.0
# Reference link:
#   https://github.com/scipy/scipy/blob/a6009217b66f58b7b4e445ff365686f48845e33a/scipy/stats/stats.py#L5252-L5382

BrunnerMunzelResult = namedtuple('BrunnerMunzelResult',
                                 ('statistic', 'pvalue'))

def brunnermunzel(x, y, alternative="two-sided", distribution="t",
                  nan_policy='propagate'):
    """
    Computes the Brunner-Munzel test on samples x and y
    The Brunner-Munzel test is a nonparametric test of the null hypothesis that
    when values are taken one by one from each group, the probabilities of
    getting large values in both groups are equal.
    Unlike the Wilcoxon-Mann-Whitney's U test, this does not require the
    assumption of equivariance of two groups. Note that this does not assume
    the distributions are same. This test works on two independent samples,
    which may have different sizes.
    Parameters
    ----------
    x, y : array_like
        Array of samples, should be one-dimensional.
    alternative :  'less', 'two-sided', or 'greater', optional
        Whether to get the p-value for the one-sided hypothesis ('less'
        or 'greater') or for the two-sided hypothesis ('two-sided').
        Defaults value is 'two-sided' .
    distribution: 't' or 'normal', optional
        Whether to get the p-value by t-distribution or by standard normal
        distribution.
        Defaults value is 't' .
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan. 'propagate' returns nan,
        'raise' throws an error, 'omit' performs the calculations ignoring nan
        values. Default is 'propagate'.
    Returns
    -------
    statistic : float
        The Brunner-Munzer W statistic.
    pvalue : float
        p-value assuming an t distribution. One-sided or
        two-sided, depending on the choice of `alternative` and `distribution`.
    See Also
    --------
    mannwhitneyu : Mann-Whitney rank test on two samples.
    Notes
    -------
    Brunner and Munzel recommended to estimate the p-value by t-distribution
    when the size of data is 50 or less. If the size is lower than 10, it would
    be better to use permuted Brunner Munzel test (see [2]_).
    References
    ----------
    .. [1] Brunner, E. and Munzel, U. "The nonparametric Benhrens-Fisher
           problem: Asymptotic theory and a small-sample approximation".
           Biometrical Journal. Vol. 42(2000): 17-25.
    .. [2] Neubert, K. and Brunner, E. "A studentized permutation test for the
           non-parametric Behrens-Fisher problem". Computational Statistics and
           Data Analysis. Vol. 51(2007): 5192-5204.
    Examples
    --------
    >>> from scipy import stats
    >>> x1 = [1,2,1,1,1,1,1,1,1,1,2,4,1,1]
    >>> x2 = [3,3,4,3,1,2,3,1,1,5,4]
    >>> w, p_value = stats.brunnermunzel(x1, x2)
    >>> w
    3.1374674823029505
    >>> p_value
    0.0057862086661515377
    """
    x = np.asarray(x)
    y = np.asarray(y)

#     # check both x and y
#     cnx, npx = _contains_nan(x, nan_policy)
#     cny, npy = _contains_nan(y, nan_policy)
#     contains_nan = cnx or cny
#     if npx == "omit" or npy == "omit":
#         nan_policy = "omit"

#     if contains_nan and nan_policy == "propagate":
#         return BrunnerMunzelResult(np.nan, np.nan)
#     elif contains_nan and nan_policy == "omit":
#         x = ma.masked_invalid(x)
#         y = ma.masked_invalid(y)
#         return mstats_basic.brunnermunzel(x, y, alternative, distribution)

    nx = len(x)
    ny = len(y)
    if nx == 0 or ny == 0:
        return BrunnerMunzelResult(np.nan, np.nan)
    rankc = rankdata(np.concatenate((x, y))) # rank all values
    # get the x- and y-ranks
    rankcx = rankc[0:nx]
    rankcy = rankc[nx:nx+ny]
    rankcx_mean = np.mean(rankcx)
    rankcy_mean = np.mean(rankcy)
    rankx = rankdata(x)
    ranky = rankdata(y)
    rankx_mean = np.mean(rankx)
    ranky_mean = np.mean(ranky)

    Sx = np.sum(np.power(rankcx - rankx - rankcx_mean + rankx_mean, 2.0))
    Sx /= nx - 1
    Sy = np.sum(np.power(rankcy - ranky - rankcy_mean + ranky_mean, 2.0))
    Sy /= ny - 1

    wbfn = nx * ny * (rankcy_mean - rankcx_mean)
    wbfn /= (nx + ny) * np.sqrt(nx * Sx + ny * Sy)

    if distribution == "t":
        df_numer = np.power(nx * Sx + ny * Sy, 2.0)
        df_denom = np.power(nx * Sx, 2.0) / (nx - 1)
        df_denom += np.power(ny * Sy, 2.0) / (ny - 1)
        df = df_numer / df_denom
        p = distributions.t.cdf(wbfn, df)
    elif distribution == "normal":
        p = distributions.norm.cdf(wbfn)
    else:
        raise ValueError(
            "distribution should be 't' or 'normal'")

    if alternative == "greater":
        p = p
    elif alternative == "less":
        p = 1 - p
    elif alternative == "two-sided":
        p = 2 * np.min([p, 1-p])
    else:
        raise ValueError(
            "alternative should be 'less', 'greater' or 'two-sided'")

    return BrunnerMunzelResult(wbfn, p)

def brunnermunzel_scale(x1, x2, scaler, alternative="two-sided", distribution="t",
                        nan_policy='propagate'):
    n1 = len(x1)
    n2 = len(x2)
    if n1 == 0 or n2 == 0:
        return BrunnerMunzelResult(np.nan, np.nan)
    rankc = rankdata(np.concatenate((x1, x2))) # rank all values
    # get the x- and y-ranks
    rankcx = rankc[0:n1]
    rankcy = rankc[n1:n1+n2]
    rankcx_mean = np.mean(rankcx)
    rankcy_mean = np.mean(rankcy)
    rankx = rankdata(x1)
    ranky = rankdata(x2)
    rankx_mean = np.mean(rankx)
    ranky_mean = np.mean(ranky)

    Sx = np.sum(np.power(rankcx - rankx - rankcx_mean + rankx_mean, 2.0))
    Sx /= n1 - 1
    Sy = np.sum(np.power(rankcy - ranky - rankcy_mean + ranky_mean, 2.0))
    Sy /= n2 - 1

    scaled_wbfn = n1 * n2 * (rankcy_mean - rankcx_mean)
    scaled_wbfn /= (n1 + n2) * np.sqrt(n1 * Sx + n2 * Sy)

    wbfn = scaled_wbfn / np.sqrt(scaler)

    if distribution == "t":
        df_numer = np.power(n1 * Sx + n2 * Sy, 2.0)
        df_denom = np.power(n1 * Sx, 2.0) / (n1 - 1)
        df_denom += np.power(n2 * Sy, 2.0) / (n2 - 1)
        df = df_numer / df_denom
        p = distributions.t.cdf(wbfn, df)
    elif distribution == "normal":
        p = distributions.norm.cdf(wbfn)
    else:
        raise ValueError(
            "distribution should be 't' or 'normal'")

    if alternative == "greater":
        p = p
    elif alternative == "less":
        p = 1 - p
    elif alternative == "two-sided":
        p = 2 * np.min([p, 1-p])
    else:
        raise ValueError(
            "alternative should be 'less', 'greater' or 'two-sided'")

    return BrunnerMunzelResult(wbfn, p)

def mwu_U2z(u, n1, n2): 
    mu = (n1*n2)/2
    su = np.sqrt((n1*n2*(n1+n2+1))/12)
    return (u - mu)/su

MannwhitneyuResult = namedtuple('MannwhitneyuResult', ('u_prime', 'z', 'pvalue'))

def mannwhitneyu_scale(x1, x2, scaler, alternative='two-sided', use_continuity=True):
    mwu_sc_res = mannwhitneyu(x1, x2, use_continuity, alternative)
    n1, n2 = len(x1), len(x2)
    sc_z = mwu_U2z(mwu_sc_res.statistic, n1, n2)
    z = sc_z / np.sqrt(scaler)
    if alternative is None:
        # This behavior, equal to half the size of the two-sided
        # p-value, is deprecated.
        p = distributions.norm.sf(abs(z))
    elif alternative == 'two-sided':
        p = 2 * distributions.norm.sf(abs(z))
    else:
        p = distributions.norm.sf(z)

    return MannwhitneyuResult(mwu_sc_res.statistic, z, p)
