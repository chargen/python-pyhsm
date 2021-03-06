#!/usr/bin/env python
#
# Copyright (c) 2011, Yubico AB
# All rights reserved.
#
# Get random data from TRNG on YubiHSM and insert it into host
# entropy pool. Probably only works on Linux since the ioctl()
# request value RNDADDENTROPY seems Linux specific.
#

import os
import sys
import fcntl
import struct
sys.path.append('Lib');
import pyhsm

device = "/dev/ttyACM0"
iterations = 100
entropy_ratio = 2	     # number of bits of entropy per byte of random data
RNDADDENTROPY = 1074287107   # from /usr/include/linux/random.h

def get_entropy(hsm, iterations, entropy_ratio):
    fd = os.open("/dev/random", os.O_WRONLY)
    # struct rand_pool_info {
    #    int     entropy_count;
    #    int     buf_size;
    #    __u32   buf[0];
    # };
    fmt = 'ii%is' % (pyhsm.defines.YSM_MAX_PKT_SIZE - 1)
    for _ in xrange(iterations):
        rnd = hsm.random(pyhsm.defines.YSM_MAX_PKT_SIZE - 1)
        this = struct.pack(fmt, entropy_ratio * len(rnd), len(rnd), rnd)
        fcntl.ioctl(fd, RNDADDENTROPY, this)

# simplified arguments parsing
d_argv = dict.fromkeys(sys.argv)
debug = d_argv.has_key('-v')

if d_argv.has_key('-h'):
    sys.stderr.write("Syntax: %s [-v]\n" % (sys.argv[0]))
    sys.exit(0)

res = 0
try:
    s = pyhsm.base.YHSM(device=device, debug=debug)
    get_entropy(s, iterations, entropy_ratio)
except pyhsm.exception.YHSM_Error, e:
    print "ERROR: %s" % e
    res = 1

sys.exit(res)
