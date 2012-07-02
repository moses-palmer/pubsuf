#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012 Moses Palmér
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.


def read_etlds(input_file):
    """
    Reads all effective TLDs found in input file.

    The list returned will keep the order from the the input file.

    @param input_file, file
        An opened file containing the effective TLD definitions.
    @return a sequence of str
    """
    def strip(l):
        if not l:
            return l
        return l[0 if l[0] != '.' else 1:l.find('//')].strip()

    return filter(lambda l: len(l) > 0,
        (strip(l).decode('utf-8') for l in input_file.readlines()))


def main(database, header_name, source_name):
    # Read all effective TLDs from the database
    with open(database, 'r') as f:
        etlds = read_etlds(f)

    # TODO: Sort the eTLDs and write the header and source file

    return 0;

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 4:
        print 'Usage: %s <database> <output header> <output c source>'
        sys.exit(1)

    sys.exit(main(*(sys.argv[1:])))
