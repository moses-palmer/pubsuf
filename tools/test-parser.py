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

import os
import re

from collections import OrderedDict

def main(infile, outfile):
    # Read the input file
    with open(infile, 'r') as f:
        lines = [l.strip() for l in f.readlines()]

    # Every test is on this format
    test_re = re.compile(r'''
        checkPublicSuffix\s* \(\s*
            (?:NULL|'([^']*)')\s*,\s*
            (?:NULL|'([^']*)')\s*
        \)\s*;''', re.VERBOSE)

    # Find all tests
    current = None
    tests = OrderedDict()
    for i, l in enumerate(lines):
        if not l:
            continue
        elif l[0] == '#':
            # Only use the last comment line as description
            current = l[1:].strip()
            if current.endswith('.'):
                current = current[:-1]
        elif current:
            m = test_re.search(l)
            if not m:
                print 'Failed to parse line %d: %s' % (
                    i + 1, l)
                continue
            if not current in tests:
                tests[current] = []
            tests[current].append(m.groups())
        else:
            print 'Invalid format on line %d: found %s, expected comment' % (
                i + 1, l)

    # Create the test definition
    test_strings = []
    for i, (description, assertions) in enumerate(tests.items()):
        assertion_string = '\n'.join('''
    assert_%seq(
        public_suffix_get_domain_name(%s),
        %s);
'''[1:-1] % (
            '' if not all(assertion) else 'str',
            ('"%s"' % assertion[0].lower()) if assertion[0] else 'NULL',
            ('"%s"' % assertion[1].lower()) if assertion[1] else 'NULL')
            for assertion in assertions)
        test_strings.append('''
TEST(public_suffix_get_domain%d,
    "%s",
    ,

%s
    ,
)'''[1:] % (i, description, assertion_string))

    # Write the output file
    with open(outfile, 'w') as f:
        f.write('\n\n'.join(test_strings))

    # Update the timestamp
    st = os.stat(infile)
    os.utime(outfile, (st.st_atime, st.st_mtime))


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print 'Usage: %s <test.txt> <test.def>' % sys.argv[0]
        sys.exit(1)

    sys.exit(main(*(sys.argv[1:])))
