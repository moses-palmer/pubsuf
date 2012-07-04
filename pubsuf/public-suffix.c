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
    /* TODO: Implement */
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
    if (depth > ETLDS_MAX_DEPTH) {
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

        /* If the rule matches, quit */
        if (suffix_cmp(string, current) == 0) {
            return !is_exception;
        }
    }

    if (depth < ETLDS_MAX_DEPTH) {
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
                if (suffix_cmp(string, current + 2) == 0) {
                    return 1;
                }
                continue;
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

