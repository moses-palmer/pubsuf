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
#include "etlds.h"

const char*
public_suffix_get_domain_name(const char *hostname)
{
    const char *s;

    /* Check for NULL input */
    if (!hostname) {
        return NULL;
    }

    /* Go to the end of the string */
    s = hostname;
    while (*s) s++; s--;

    /* Find the first possible start of the public suffix */
    int depth = 0;
    while (1) {
        /* Find the previous segment */
        while (s > hostname && *s != '.') s--;
        depth++;

        /* Break if at the start of the hostname or if we have reached the
           maximum depth */
        if (s == hostname) {
            break;
        }
        else if (depth == pubsuf_max_depth) {
            s++;
            break;
        }

        /* We are at a dot; skip to the previous character */
        s--;
    }

    /* Test all depths lower than or equal to the depth found */
    while (depth) {
        if (public_suffix_test(s, depth)) {
            /* A public suffix is not a domain */
            if (s == hostname) {
                return NULL;
            }

            /* Find the previous segment */
            s -= 2;
            while (s > hostname && *s != '.') s--;
            return *s == '.' ? s + 1 : s;
        }

        depth--;
        while (*s != '.') s++;
        s++;
    }

    return NULL;
}

/**
 * Checks a string against a single rule.
 *
 * @param string
 *     The string to check. This must not begin with a dot ('.').
 * @param rule
 *     The rule to check. This must no be an exception; to check an exception,
 *     use rule + 1.
 * @return a value compatible with the return value of strcmp
 */
static inline int
suffix_cmp(const char *string, const char *rule)
{
    const char *s, *r;

    for (s = string, r = rule; *s && *r;) {
        if (*s == *r) {
            /* The simple case */
            s++;
            r++;
        }
        else if (*r == '*') {
            /* A wildcard; increment s until a dot */
            while (*s && *s != '.') s++;
            r++;
        }
        else {
            /* The rule does not match */
            break;
        }
    }

    return *s - *r;
}

int
public_suffix_test(const char *string, int depth)
{
    const char **rule;

    /* Check for NULL input */
    if (!string) {
        return 0;
    }

    /* Handle initial dot */
    if (*string == '.') {
        string++;
    }

    /* Check whether we need to calculate the depth */
    if (depth < 0) {
        depth = public_suffix_get_depth(string);
    }

    /* If the depth is greater that the maximum depth, we already know this is
       not a public suffix */
    if (depth > pubsuf_max_depth) {
        return 0;
    }

    /* Locate the rule list of interest and iterate over every rule */
    for (rule = pubsuf_etlds[depth - 1]; *rule; rule++) {
        const char *current = *rule;

        /* First see whether this is an exception */
        int is_exception = *current == '!';
        if (is_exception) {
            current++;
        }

        /* Check whether this is a wildcard */
        int is_wildcard = *current == '*';

        /* If the rule matches, quit; if the rule is greater than the string and
           not an exception or a wildcard, stop checking */
        int result = suffix_cmp(string, current);
        if (result == 0) {
            return !is_exception;
        }
        else if (result < 0 && !is_exception && !is_wildcard) {
            break;
        }
    }

    if (depth < pubsuf_max_depth) {
        /* Check the wildcards one level up, since *.public.suffix matches
           public.suffix */
        for (rule = pubsuf_etlds[depth]; *rule; rule++) {
            const char *current = *rule;

            /* Ignore all exceptions */
            int is_exception = *current == '!';
            if (is_exception) {
                continue;
            }

            /* Check all wildcards */
            int is_wildcard = *current == '*';
            if (is_wildcard) {
                int result = suffix_cmp(string, current + 2);
                if (result == 0) {
                    return 1;
                }
                else if (result < 0) {
                    break;
                }
                else {
                    continue;
                }
            }

            break;
        }
    }

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

