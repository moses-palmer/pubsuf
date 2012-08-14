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

#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>

/**
 * The file that contains the externalised effective TLD database.
 *
 * The content of this file is similar to the data in etlds.c::pubsuf_etlds,
 * with the following differences:
 *
 *   1. It is one contiguous block of memory.
 *   2. The pointers are all relative, and thus the address of pubsuf_etlds must
 *      be added for every pointer to make it valid.
 */
#define ETLD_DATABASE DATA_PATH "/etlds.db"

/** @see etlds.h */
int pubsuf_max_depth = 0;

/** The size of the pubsuf_etlds buffer */
static size_t pubsuf_etlds_size = 0;

/** @see etlds.h */
const char ***pubsuf_etlds = NULL;

/**
 * Initialises a table by adding the address of pubsuf_etlds to every offset
 * in table until (ptrdiff_t)0 is encountered.
 *
 * If recurse is greater than 0, this function is called recursively for every
 * adjusted address with recurse set to recurse - 1.
 *
 * @param table
 *     The table to initialise.
 * @param recurse
 *     A recurse counter.
 */
static void
initialize_table(ptrdiff_t *table, int recurse)
{
    while (*table) {
        *table += (ptrdiff_t)(char*)pubsuf_etlds;
        if (recurse > 0) {
            initialize_table((ptrdiff_t*)*table, recurse - 1);
        }
        table++;
    }
}

__attribute__((constructor))
void public_suffix_initialize(void)
{
    /* Open the external database */
    FILE *f = fopen(ETLD_DATABASE, "rb");
    if (!f) {
        return;
    }

    /* Determine the size of the database */
    if (fseek(f, 0, SEEK_END) != 0) {
        fclose(f);
        return;
    }
    pubsuf_etlds_size = ftell(f);
    rewind(f);
    if (pubsuf_etlds_size == 0) {
        fclose(f);
        return;
    }

    /* Load the database */
    pubsuf_etlds = malloc(pubsuf_etlds_size);
    if (!pubsuf_etlds) {
        fclose(f);
        return;
    }
    if (fread(pubsuf_etlds, 1, pubsuf_etlds_size, f) != pubsuf_etlds_size) {
        free(pubsuf_etlds);
        pubsuf_etlds = NULL;
        fclose(f);
        return;
    }
    fclose(f);

    /* Add the required offset to the tables; recurse only once */
    initialize_table((ptrdiff_t*)pubsuf_etlds, 1);

    /* Get the number of depths */
    const char ***tables;
    for (tables = pubsuf_etlds, pubsuf_max_depth = 0; *tables; tables++) {
        pubsuf_max_depth++;
    }
}

__attribute__((destructor))
void public_suffix_finalize(void)
{
    /* Free and zero the buffer */
    free(pubsuf_etlds);
    pubsuf_etlds = NULL;
}

