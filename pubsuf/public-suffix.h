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

#ifndef PUBSUF_PUBLIC_SUFFIX_H
#define PUBSUF_PUBLIC_SUFFIX_H

/**
 * Retrieves the domain name from a host name.
 *
 * The domain name starts at the host name section before the public suffix;
 * thus "dc01.xyz.domain.public.suffix" will yield "domain.public.suffix".
 *
 * This function will return a non-NULL string only when hostname ends with a
 * public suffix.
 *
 * The returned value is a pointer into hostname.
 *
 * The input string MUST be lowercase UTF-8. If it is NULL, it is not accessed.
 *
 * @param hostname
 *     The hostname for which to retrieve the domain name.
 * @return the domain name for the host name, or NULL
 * @see public_suffix_test
 */
const char*
public_suffix_get_domain_name(const char *hostname);

/**
 * Tests whether a string is a public suffix.
 *
 * A string is a public suffix if it matches any of the rules in the effective
 * TLD list.
 *
 * The input string MUST be lowercase UTF-8. If it is NULL, it is not accessed.
 *
 * @param string
 *     The string to test. This must be on the form .public.suffix or
 *     public.suffix.
 * @param depth
 *     The depth of the string. This should be the return value of
 *     public_suffix_get_depth(string), or a negative value to have it
 *     calculated.
 * @return whether string is a public suffix and non-NULL
 * @see public_suffix_get_depth
 */
int
public_suffix_test(const char *string, int depth);

/**
 * Retrieves the depth of a string.
 *
 * The depth is calculated as the number of dots in string, excluding the first
 * character, plus one; thus "public.suffix" and ".public.suffix" will yield 2.
 *
 * The input string MUST be lowercase UTF-8. If it is NULL, it is not accessed.
 *
 * @param string
 *     The string to check.
 * @return the depth of the string, or 0 if string is NULL
 */
int
public_suffix_get_depth(const char *string);

#endif

