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

def main(infile, outfile):
    # TODO: Implement
    pass

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print 'Usage: %s <test.txt> <test.def>' % sys.argv[0]
        sys.exit(1)

    sys.exit(main(*(sys.argv[1:])))
