/*
 * Copyright (C) 2018 Intel Corporation. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */
#include <logmsg.h>
#include <security.h>

void __stack_chk_fail(void)
{
	ASSERT(false, "stack check fails in HV\n");
}
