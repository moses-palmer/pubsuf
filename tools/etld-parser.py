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


def load_etld_database(database):
    """
    Reads all effective TLDs found in database and sorts them.

    The sorting is an alphanumerical sorting followed by sorting based on the
    key <0 if s[0] == '!' else 1 if s[0] == '*' else 2>.

    @param database
        The file name of the database file.
    @return a two-dimensional array where the first dimension is the TLD depth
        and the second the sorted list of effective TLDs
    """
    # Read all effective TLDs from the database and sort them on string value,
    # and make sure exceptions and then wildcards are preferred within every
    # depth segment
    with open(database, 'r') as f:
        etlds = read_etlds(f)
    etlds.sort()
    etlds.sort(key = lambda s: 0 if s[0] == '!' else 1 if s[0] == '*' else 2)

    # Create the lists for each depth
    return [[etld for etld in etlds if etld.count('.') + 1 == i]
        for i in range(1, max(e.count('.') for e in etlds) + 1)]


def c_source(depths, c_source_h, c_source_c, **kwargs):
    """
    Converts an effective TLD database to a header and source file.

    @param depths
        The effective TLD database.
    @param c_source_h
        The name of the header file to write.
    @param c_source_c
        Th name of the source file to write.
    @return a list of generated file names
    """
    HEADER_FORMAT = '''
/* Copyright 2012 Moses Palmér
 *
 * This library is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as published by the
 * Free Software Foundation; either version 2 of the License, or (at your
 * option) any later version.
 *
 * This library is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License
 * for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library; if not, write to the Free Software Foundation,
 * Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */

#ifndef PUBSUF_ETLDS_H
#define PUBSUF_ETLDS_H

/**
 * The maximum depth of any of the rules.
 */
#define ETLDS_MAX_DEPTH %d

/**
 * The list of eTLD name rules.
 *
 * This is a NULL terminated list with ETLDS_MAX_DEPTH NULL terminated lists
 * of strings.
 *
 * The top-level lists are sorted with depth descending.
 *
 * The lower-level lists are sorted alphabetically and partitioned so that the
 * first part is exceptions if any, the second part is wilcards if any and the
 * third part is plain rules.
 */
extern const char **pubsuf_etlds[ETLDS_MAX_DEPTH + 1];

#endif
'''[1:]

    SOURCE_FORMAT = '''
#include <stdlib.h>

#include "etlds.h"

%s

const char **pubsuf_etlds[ETLDS_MAX_DEPTH + 1] = {
%s
    NULL};
'''[1:]

    DEPTH_FORMAT = '''
static const char *depth%d[] = {
%s
    NULL};
'''[1:]

    # Write the header file
    with open(c_source_h, 'w') as f:
        f.write(HEADER_FORMAT % len(depths))

    # To make sure hex escaping is correct, we need to write hex encoding
    # separately
    hex_splitter = re.compile(r'(\\x[0-9a-fA-F]{2})([0-9a-fA-F])')

    # Write the source file
    depth_definitions = '\n\n'.join(DEPTH_FORMAT % (
        d + 1,
        '\n'.join('    "%s",' % hex_splitter.sub('\\1" "\\2',
            rule.encode('utf-8').encode('string_escape'))
                for rule in depths[d]))
            for d in range(len(depths)))
    depth_listing = '\n'.join('    depth%d,' % (d + 1)
        for d in range(len(depths)))
    with open(c_source_c, 'w') as f:
        f.write(SOURCE_FORMAT % (depth_definitions, depth_listing))

    return (c_source_h, c_source_c)


# Intialise the output type map
output_types = {
    'c-source': c_source}


def main(output_type, database, **kwargs):
    # Load the TLD database
    depths = load_etld_database(database)

    # Get the timestamp of the database
    st = os.stat(database)
    for output_file in output_types[output_type](depths, **kwargs):
        os.utime(output_file, (st.st_atime, st.st_mtime))

if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description = 'Parses an eTLD database and outputs formatted data.');
    parser.add_argument('--c-source-h',
        help = 'The header to output')
    parser.add_argument('--c-source-c',
        help = 'The C source file to output')

    parser.add_argument('output_type',
        help = 'The type of output to generate.', choices = output_types.keys())
    parser.add_argument('database',
        help = 'The database file to read.')

    args = parser.parse_args()

    sys.exit(main(**vars(args)))
