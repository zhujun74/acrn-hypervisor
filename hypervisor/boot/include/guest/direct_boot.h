/*
 * Copyright (C) 2019 Intel Corporation. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#ifndef DIRECT_BOOT_H

#define DIRECT_BOOT_H

#include <vboot.h>

struct vboot_operations* get_direct_boot_ops(void);

#endif /* end of include guard: DIRECT_BOOT_H */
