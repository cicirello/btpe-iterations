# Analysis of iterations of BTPE algorithm for binomial random variate generation.
# Copyright (C) 2023 Vincent A. Cicirello
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

def naive(n, M, r) :
    return math.comb(n, M) * r ** M * (1 - r) ** (n - M)

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
    for (n, p), d in zip(cases, data):
        if n != prev_n:
            if prev_n != None:
                print("\\hline")
                print("\\end{tabular}")
                print("\\end{table}")
                print()
            prev_n = n
            print("\\begin{table}[t]")
            print("\\caption{{Average number of calls to $U(0,1)$ by $\\rho\\mu$'s BTPE implementation for $n={0}$}}".format(n))
            print("\\label{{tab:calls{0}}}".format(n))
            print("\\begin{tabular}{cccc} \\hline")
            print("    & $\\rho\\mu$ & & T-test \\\\")
            print("$p$ & mean & predicted & $p$-value \\\\ \\hline")

        expected = expected_number_uniform_doubles(n, p)
        result = scipy.stats.ttest_1samp(d, expected)
        confidence_interval = result.confidence_interval(0.95)
        pm = (confidence_interval.high - confidence_interval.low) / 2
        print(
            template.format(
                "{0:.10f}".format(p).rstrip("0"),
                statistics.mean(d),
                pm,
                expected,
                result.pvalue
            )
        )
    print("\\hline")
    print("\\end{tabular}")
    print("\\end{table}")
    print()
