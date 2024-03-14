# On the Average Runtime of an Open Source Binomial Random Variate Generation Algorithm.
# Copyright (C) 2024 Vincent A. Cicirello
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import math
import statistics
import sys
import scipy.stats

def parse(filename) :
    """Parses the raw data file.

    Keyword arguments:
    filename - the name of the file to parse
    """
    with open(filename, "r") as f:
        cases = []
        data = []
        for line in f:
            row = line.strip().split()
            if len(row) < 1:
                continue
            if row[0] == "Case":
                cases.append((int(row[1]), float(row[2])))
            else:
                data.append( [int(x) for x in row] )
        return cases, data

def numerically_stable_terms(n, M, r) :
    """Computes choose(n, M) * r**M * (1-r)**(n-M)
    in a numerically stable way to ensure that cases with
    large n, M, etc don't run into floating-point issues.
    """
    result = 0
    if M >= n - M:
        for i in range(1, n - M + 1):
            result += math.log(1 - r) + math.log(M + i) - math.log(i)
        result += M * math.log(r)
    else:
        for i in range(1, M + 1):
            result += math.log(r) + math.log(n - M + i) - math.log(i)
        result += (n - M) * math.log(1 - r)
    return math.exp(result)

def expected_iterations(n, p) :
    """Computes the expected number of iterations of the
    BTPE algorithm for binomial random variates.

    Keyword arguments:
    n - the value of n
    p - the value of p
    """
    r = min(p, 1 - p)
    q = 1 - r
    fM = n * r + r
    M = math.floor(fM)
    p1 = math.floor(2.195 * math.sqrt(n * r * q) - 4.6 * q) + 0.5
    xM = M + 0.5
    xL = xM - p1
    xR = xM + p1
    c = 0.134 + 20.5 / (15.3 + M)
    a = (fM - xL) / (fM - xL * r)
    lambda_L = a * (1 + a / 2)
    a = (xR - fM) / (xR * q)
    lambda_R = a * (1 + a / 2)
    p2 = p1 * (1 + 2 * c)
    p3 = p2 + c / lambda_L
    p4 = p3 + c / lambda_R
    return p4 * numerically_stable_terms(n, M, r)

def expected_number_uniform_doubles(n, p) :
    """Computes the expected number of uniform doubles
    from interval [0.0, 1.0) for the
    BTPE algorithm for binomial random variates.

    Keyword arguments:
    n - the value of n
    p - the value of p
    """
    return 2 * expected_iterations(n, p)

if __name__ == "__main__" :
    filename = sys.argv[1]
    cases, data = parse(filename)
    template = "{0:12} & ${1:.2f} \pm {2:.3f}$ & {3:.2f} & {4:.2f} \\\\"
    prev_n = None
    case1 = []
    case2 = []
    for (n, p), d in zip(cases, data):
        compute_case = False
        if n != prev_n:
            prev_n = n
            compute_case = True
            results = case1
        elif abs(p - 0.5) < 0.001:
            compute_case = True
            results = case2
        if compute_case:
            expected = expected_number_uniform_doubles(n, p)
            ttest_result = scipy.stats.ttest_1samp(d, expected)
            confidence_interval = ttest_result.confidence_interval(0.95)
            pm = (confidence_interval.high - confidence_interval.low) / 2

            results.append(
                (n, p, expected, statistics.mean(d), pm, ttest_result.pvalue)
            )
    header = """\\begin{table}[t]
\\centering
\\caption{Average number of calls to $U(0,1)$ by $\\rho\\mu$'s BTPE implementation
compared to the prediction of Equation~\\ref{eq:uniform}. 95\% confidence intervals
are shown, as well as the $p$-values from t-tests.}\\label{fig:results}
\\begin{tabular}{c|ccc|ccc}\\hline
    & \\multicolumn{3}{|c}{$B(n,\\frac{10}{n})$} & \\multicolumn{3}{|c}{$B(n,0.5)$} \\\\
$n$ & predicted & mean & $p$-value & predicted & mean & $p$-value \\\\\\hline"""
    print(header)
    template = "$2^{{{0}}}$ & {1:.3f} & ${2:.3f} \pm {3:.3f}$ & {4:.2f} & {5:.3f} & ${6:.3f} \pm {7:.3f}$ & {8:.2f} \\\\"
    for i, (c1, c2) in enumerate(zip(case1, case2)):
        print(template.format(
            i+5,
            c1[2], # expected case 1 maximized uniforms
            c1[3], # observed case 1 maximized uniforms
            c1[4], # observed case 1 95% confidence interval
            c1[5], # t-test p-value case 1
            c2[2], # expected case 2 p=0.5
            c2[3], # observed case 2 p=0.5
            c2[4], # observed case 1 95% confidence interval
            c2[5]  # t-test p-value case 2
        ))
    print("\\hline")
    print("\\end{tabular}")
    print("\\end{table}")
