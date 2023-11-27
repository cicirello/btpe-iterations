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

import sys

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

if __name__ == "__main__" :
    filename = sys.argv[1]
    cases, data = parse(filename)
    m = 0
    max_case = None
    for (n, p), d in zip(cases, data):
        update = max(m, max(d))
        if update != m:
            max_case = (n, p)
            m = update
    print("Max across all cases:", m)
    print("Occurred for (n,p) =", max_case)
    print()
        
    print("{0:7} {1:14} {2:3}".format("n", "p", "max"))
    for (n, p), d in zip(cases, data):
        print("{0:<7d} {1:14} {2:<3d}".format(
            n,
            "{0:.10f}".format(p).rstrip("0"),
            max(d))) 
