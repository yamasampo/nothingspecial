"""All functions related to Mann-Whitney test are moved into evogen_share.stats 
without any modification by 2024.7.29. After this date, a change can be made at 
the destination.
"""

import warnings
import numpy as np

from collections import namedtuple
from scipy.stats import distributions, rankdata, mannwhitneyu, tiecorrect

from .. import num

# def fd2data(x, fd, scaler=1):
#     """ Regenerate data from given frequency distributions for given data. You 
#     can change scale of sample size from "scaler" option.

#     Parameters
#     ----------
#     x: list
#         A list of sample data. Data can be numeric and/or string but have to be
#         categorical data.
#     fd: list
#         A list of sample frequency distributions.
#     scaler: int (optional)
#         Scale of sample size. If it is set to 100, each frequency will be 
#         multiplied by 100.

#     Assumption
#     ----------
#         Frequency of x have to be found in the same place in fd.
    
#     Dependencies
#     ------------
#     numpy
#     round function

#     """
#     data = []
#     fd = [num.myround(a, 0) for a in scaler * np.array(fd)]
#     for i, d in enumerate(x):
#         for _ in range(int(fd[i])):
#             data.append(d)
#     if len(data) != sum(fd):
#         print(len(data), sum(fd))
#         raise Exception('')
#     return data

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

# def mwu_U2z(u, n1, n2): 
#     mu = (n1*n2)/2
#     su = np.sqrt((n1*n2*(n1+n2+1))/12)
#     return (u - mu)/su

# MannwhitneyuResult = namedtuple('MannwhitneyuResult', ('u_prime', 'z', 'pvalue'))

# def mannwhitneyu(x, y, use_continuity=True, alternative=None):
#     """
#     Compute the Mann-Whitney rank test on samples x and y.

#     Parameters
#     ----------
#     x, y : array_like
#         Array of samples, should be one-dimensional.
#     use_continuity : bool, optional
#             Whether a continuity correction (1/2.) should be taken into
#             account. Default is True.
#     alternative : None (deprecated), 'less', 'two-sided', or 'greater'
#             Whether to get the p-value for the one-sided hypothesis ('less'
#             or 'greater') or for the two-sided hypothesis ('two-sided').
#             Defaults to None, which results in a p-value half the size of
#             the 'two-sided' p-value and a different U statistic. The
#             default behavior is not the same as using 'less' or 'greater':
#             it only exists for backward compatibility and is deprecated.

#     Returns
#     -------
#     statistic : float
#         The Mann-Whitney U statistic, equal to min(U for x, U for y) if
#         `alternative` is equal to None (deprecated; exists for backward
#         compatibility), and U for y otherwise.
#     pvalue : float
#         p-value assuming an asymptotic normal distribution. One-sided or
#         two-sided, depending on the choice of `alternative`.

#     Notes
#     -----
#     Use only when the number of observation in each sample is > 20 and
#     you have 2 independent samples of ranks. Mann-Whitney U is
#     significant if the u-obtained is LESS THAN or equal to the critical
#     value of U.

#     This test corrects for ties and by default uses a continuity correction.

#     References
#     ----------
#     .. [1] https://en.wikipedia.org/wiki/Mann-Whitney_U_test

#     .. [2] H.B. Mann and D.R. Whitney, "On a Test of Whether one of Two Random
#            Variables is Stochastically Larger than the Other," The Annals of
#            Mathematical Statistics, vol. 18, no. 1, pp. 50-60, 1947.

#     """
#     if alternative is None:
#         warnings.warn("Calling `mannwhitneyu` without specifying "
#                       "`alternative` is deprecated.", DeprecationWarning)

#     x = np.asarray(x)
#     y = np.asarray(y)
#     n1 = len(x)
#     n2 = len(y)
#     ranked = rankdata(np.concatenate((x, y)))
#     rankx = ranked[0:n1]  # get the x-ranks
#     u1 = n1*n2 + (n1*(n1+1))/2.0 - np.sum(rankx, axis=0)  # calc U for x
#     u2 = n1*n2 - u1  # remainder is U for y
#     T = tiecorrect(ranked)
    
#     if T == 0:
#         warnings.warn(
#             'All numbers are identical in mannwhitneyu')
#     sd = np.sqrt(T * n1 * n2 * (n1+n2+1) / 12.0)

#     meanrank = n1*n2/2.0 + 0.5 * use_continuity
#     if alternative is None or alternative == 'two-sided':
#         bigu = max(u1, u2)
#     elif alternative == 'less':
#         bigu = u1
#     elif alternative == 'greater':
#         bigu = u2
#     else:
#         raise ValueError("alternative should be None, 'less', 'greater' "
#                          "or 'two-sided'")
    
#     z = (u2 - meanrank) / sd
#     if alternative is None:
#         # This behavior, equal to half the size of the two-sided
#         # p-value, is deprecated.
#         p = distributions.norm.sf(abs(z))
#     elif alternative == 'two-sided':
#         p = 2 * distributions.norm.sf(abs(z))
#     else:
#         p = distributions.norm.sf(z)

#     u = u2
#     # This behavior is deprecated.
#     if alternative is None:
#         u = min(u1, u2)
#     return MannwhitneyuResult(u, z ,p)

# def mannwhitneyu_scale(x1, x2, scaler, alternative='two-sided', use_continuity=True):
#     mwu_sc_res = mannwhitneyu(x1, x2, use_continuity, alternative)
#     n1, n2 = len(x1), len(x2)
#     z = mwu_sc_res.z / np.sqrt(scaler)
#     if alternative is None:
#         # This behavior, equal to half the size of the two-sided
#         # p-value, is deprecated.
#         p = distributions.norm.sf(abs(z))
#     elif alternative == 'two-sided':
#         p = 2 * distributions.norm.sf(abs(z))
#     else:
#         p = distributions.norm.sf(z)

#     return MannwhitneyuResult(mwu_sc_res.u_prime, z, p)
