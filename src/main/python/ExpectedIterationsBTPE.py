# An Analysis of an Open Source Binomial Random Variate Generation Algorithm.
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

from math import floor, sqrt, comb, log, exp

def naive(n, M, r) :
    return comb(n, M) * r ** M * (1 - r) ** (n - M)

def numerically_stable_terms(n, M, r) :
    """Computes choose(n, M) * r**M * (1-r)**(n-M)
    in a numerically stable way to ensure that cases with
    large n, M, etc don't run into floating-point issues.
    """
    result = 0
    if M >= n - M:
        for i in range(1, n - M + 1):
            result += log(1 - r) + log(M + i) - log(i)
        result += M * log(r)
    else:
        for i in range(1, M + 1):
            result += log(r) + log(n - M + i) - log(i)
        result += (n - M) * log(1 - r)
    return exp(result)

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
    M = floor(fM)
    p1 = floor(2.195 * sqrt(n * r * q) - 4.6 * q) + 0.5
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

def expected_iterations_inverse_transform(n, p) :
    """Computes the expected number of iterations of
    the inverse transform method for binomial random
    variates, which is also the expected number of
    random doubles in [0.0, 1.0) since it generates 1
    per iteration.

    Keyword arguments:
    n - the value of n
    p - the value of p
    """
    return n * min(p, 1-p)

def output_BTPE_table(n) :
    """Outputs a table of expected iterations and number of random doubles
    for BTPE and a value of n.
    """
    min_relevant_p = 10 / n
    if min_relevant_p > 0.5:
        print("BTPE not relevant for n =", n)
        print()
        return
    max_relevant_p = 1.0 - min_relevant_p

    p_values = []
    p = 1 / n
    while p < min_relevant_p:
        p_values.append(p)
        p *= 2
    p_values.append(min_relevant_p)
    while p <= 0.50001 :
        p_values.append(p)
        p *= 2
        
    for pr in reversed(p_values[:-1]) :
        p_values.append(1 - pr)

    table_row_only_inv = "{0:.10f} &  &  & {1:.0f} \\\\"
    table_row = "{0:.10f} & {1:.2f} & {2:.2f} & {3:.0f} \\\\"
    print("Table for n =", n)
    print("\\begin{tabular}{l|cc|r} \\hline")
    print("    & \multicolumn{2}{|c|}{BTPE} & BINV \\\\")
    print("$p$ & iterations & calls to $U(0.0, 1.0)$ & both \\\\ \\hline")
    for p in p_values :
        if p < min_relevant_p or p > max_relevant_p:
            print(
                table_row_only_inv.format(
                    p,
                    expected_iterations_inverse_transform(n, p)
                )
            )
        else :
            print(
                table_row.format(
                    p,
                    expected_iterations(n, p),
                    expected_number_uniform_doubles(n, p),
                    expected_iterations_inverse_transform(n, p)
                )
            )
    print("\\hline")
    print("\\end{tabular}")
    print()

if __name__ == "__main__" :
    output_BTPE_table(32)
    output_BTPE_table(64)
    output_BTPE_table(128)
    output_BTPE_table(256)
    output_BTPE_table(512)
    output_BTPE_table(1024)
    output_BTPE_table(2048)
    output_BTPE_table(4096)
    output_BTPE_table(8192)
    output_BTPE_table(16384)
    output_BTPE_table(32768)
    output_BTPE_table(65536)
    output_BTPE_table(131072)
    output_BTPE_table(262144)
    output_BTPE_table(524288)
    output_BTPE_table(1048576)
