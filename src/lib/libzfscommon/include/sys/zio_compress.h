/*
 * CDDL HEADER START
 *
 * The contents of this file are subject to the terms of the
 * Common Development and Distribution License, Version 1.0 only
 * (the "License").  You may not use this file except in compliance
 * with the License.
 *
 * You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
 * or http://www.opensolaris.org/os/licensing.
 * See the License for the specific language governing permissions
 * and limitations under the License.
 *
 * When distributing Covered Code, include this CDDL HEADER in each
 * file and include the License file at usr/src/OPENSOLARIS.LICENSE.
 * If applicable, add the following below this CDDL HEADER, with the
 * fields enclosed by brackets "[]" replaced with your own identifying
 * information: Portions Copyright [yyyy] [name of copyright owner]
 *
 * CDDL HEADER END
 */
/*
 * Copyright 2005 Sun Microsystems, Inc.  All rights reserved.
 * Use is subject to license terms.
 */

#ifndef _SYS_ZIO_COMPRESS_H
#define	_SYS_ZIO_COMPRESS_H



#include <sys/zio.h>

#ifdef	__cplusplus
extern "C" {
#endif

/*
 * Common signature for all zio compress/decompress functions.
 */
typedef size_t zio_compress_func_t(void *src, void *dst,
    size_t s_len, size_t d_len);
typedef int zio_decompress_func_t(void *src, void *dst,
    size_t s_len, size_t d_len);

/*
 * Information about each compression function.
 */
typedef struct zio_compress_info {
	zio_compress_func_t	*ci_compress;
	zio_decompress_func_t	*ci_decompress;
	char			*ci_name;
} zio_compress_info_t;

extern zio_compress_info_t zio_compress_table[ZIO_COMPRESS_FUNCTIONS];

/*
 * Compression routines.
 */
extern size_t lzjb_compress(void *src, void *dst, size_t s_len, size_t d_len);
extern int lzjb_decompress(void *src, void *dst, size_t s_len, size_t d_len);

/*
 * Compress and decompress data if necessary.
 */
extern int zio_compress_data(int cpfunc, void *src, uint64_t srcsize,
    void **destp, uint64_t *destsizep, uint64_t *destbufsizep);
extern int zio_decompress_data(int cpfunc, void *src, uint64_t srcsize,
    void *dest, uint64_t destsize);

#ifdef	__cplusplus
}
#endif

#endif	/* _SYS_ZIO_COMPRESS_H */