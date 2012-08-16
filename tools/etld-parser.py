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


def binary(depths, binary_out, **kwargs):
    """
    Converts an effective TLD database to a header and source file.

    @param depths
        The effective TLD database.
    @param binary_out
        The name of the file to write.
    @return a list of generated file names
    """
    import struct

    # Calculate the size of the depth table; include the terminating 0
    depth_table = [0] * len(depths)
    depth_table_size = struct.calcsize(str(len(depth_table) + 1) + 'P')

    # Calculate the sizes of the string tables
    string_tables = [[0] * len(depth)
        for depth in depths]
    string_table_sizes = [struct.calcsize(str(len(string_table) + 1) + 'P')
        for string_table in string_tables]

    # We start at the end of the depth table
    offset = depth_table_size

    # Initialise the depth table
    for depth_index in xrange(len(depth_table)):
        depth_table[depth_index] = offset
        offset += string_table_sizes[depth_index]

    # Initialise the string tables and the data buffer
    data_buffer = ''
    for depth_index, depth in enumerate(depths):
        for string_index, string in enumerate(depth):
            data = string.encode('utf-8') + '\0'
            string_tables[depth_index][string_index] = offset
            data_buffer += data
            offset += len(data)

    # Write the file
    with open(binary_out, 'wb') as f:
        f.write(struct.pack(
            str(len(depth_table) + 1) + 'P',
            *(depth_table + [0])))
        for string_table in string_tables:
            f.write(struct.pack(
                str(len(string_table) + 1) + 'P',
                *(string_table + [0])))
        f.write(data_buffer)

    return (binary_out,)


def c_source(depths, c_source_c, **kwargs):
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
    SOURCE_FORMAT = '''
#include <stdlib.h>

#include "etlds.h"

int pubsuf_max_depth = %d;

%s

static const char **depths[] = {
%s
    NULL};

const char ***pubsuf_etlds = depths;
'''[1:]

    DEPTH_FORMAT = '''
static const char *depth%d[] = {
%s
    NULL};
'''[1:]

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
        f.write(SOURCE_FORMAT % (len(depths), depth_definitions, depth_listing))

    return (c_source_c,)


# Intialise the output type map
output_types = {
    'binary': binary,
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
    parser.add_argument('--c-source-c',
        help = 'The C source file to output')
    parser.add_argument('--binary-out',
        help = 'The binary database to output')

    parser.add_argument('output_type',
        help = 'The type of output to generate.', choices = output_types.keys())
    parser.add_argument('database',
        help = 'The database file to read.')

    args = parser.parse_args()

    sys.exit(main(**vars(args)))
