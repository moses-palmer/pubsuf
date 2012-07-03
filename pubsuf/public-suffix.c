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

#include <stdlib.h>

#include "public-suffix.h"

const char*
public_suffix_get_domain_name(const char *hostname)
{
    /* TODO: Implement */
    return NULL;
}

int
public_suffix_test(const char *string, int depth)
{
    /* TODO: Implement */
    return 0;
}

int
public_suffix_get_depth(const char *string)
{
    const char *s;
    int result = 1;

    /* Check for NULL input */
    if (!string) {
        return 0;
    }

    /* Skip the first character; if this is '.', it must not influence the
       result */
    for (s = string + 1; *s; s++) {
        if (*s == '.') {
            result++;
        }
    }

    return result;
}

