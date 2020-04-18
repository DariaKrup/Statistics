import numpy as np
import scipy.stats as stats

gamma_confidence = 0.95


def _m_confidence_interval(distr):
    m = np.mean(distr)
    s = np.std(distr)
    n = len(distr)
    interval = s * stats.t.ppf((1 + gamma_confidence) / 2, n - 1) / (n - 1) ** 0.5
    return np.around(m - interval, decimals=2), np.around(m + interval, decimals=2)


def _var_confidence_interval(distr):
    s = np.std(distr)
    n = len(distr)
    low_b = s * (n / stats.chi2.ppf((1 + gamma_confidence) / 2, n - 1)) ** 0.5
    high_b = s * (n / stats.chi2.ppf((1 - gamma_confidence) / 2, n - 1)) ** 0.5
    return np.around(low_b, decimals=2), np.around(high_b, decimals=2)


def _m_confidence_asimpt(distr):
    m = np.mean(distr)
    s = np.std(distr)
    n = len(distr)
    u = stats.norm.ppf((1 + gamma_confidence) / 2)
    interval = s * u / (n ** 0.5)
    return np.around(m - interval, decimals=2), np.around(m + interval, decimals=2)


def _var_confidence_asimpt(distr):
    m = np.mean(distr)
    s = np.std(distr)
    n = len(distr)
    m_4 = stats.moment(distr, 4)
    e_ = m_4 / s**4 - 3
    u = stats.norm.ppf((1 + gamma_confidence) / 2)
    U = u * (((e_ + 2) / n) ** 0.5)
    low_b = s * (1 + 0.5 * U) ** (-0.5)
    high_b = s * (1 - 0.5 * U) ** (-0.5)
    return np.around(low_b, decimals=2), np.around(high_b, decimals=2)


if __name__ == '__main__':
    size = [20, 100]
    for s in size:
        distr = np.random.normal(0, 1, size=s)
        print('size = ' + str(s))
        print('mean', _m_confidence_interval(distr))
        print('variance', _var_confidence_interval(distr))
        print('asimpt_mean', _m_confidence_asimpt(distr))
        print('asimpt_variance', _var_confidence_asimpt(distr))