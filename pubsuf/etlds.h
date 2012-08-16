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
extern int pubsuf_max_depth;

/**
 * The list of eTLD name rules.
 *
 * This is a NULL terminated list with pubsuf_max_depth NULL terminated lists
 * of strings.
 *
 * The top-level lists are sorted with depth descending.
 *
 * The lower-level lists are sorted alphabetically and partitioned so that the
 * first part is exceptions if any, the second part is wilcards if any and the
 * third part is plain rules.
 */
extern const char ***pubsuf_etlds;

#endif
