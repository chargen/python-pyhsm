#!/usr/bin/env python
#
# Copyright (c) 2011, Yubico AB
# All rights reserved.
#
# Utility to show system information of a YubiHSM.
#

import sys
sys.path.append('Lib');
import pyhsm

device = "/dev/ttyACM0"

# simplified arguments parsing
d_argv = dict.fromkeys(sys.argv)
debug = d_argv.has_key('-v')

if d_argv.has_key('-h'):
    sys.stderr.write("Syntax: %s [-v]\n" % (sys.argv[0]))
    sys.exit(0)

res = 0
try:
    hsm = pyhsm.base.YHSM(device=device, debug=debug)

    print "Version : %s\n" % (hsm.info())

    password = raw_input('Enter HSM password (will be echoed) : ')
    if len(password) == 32:
        password = password.decode('hex')
    print "\n"
    hsm.key_storage_unlock(password)
    print "OK"
except pyhsm.exception.YHSM_Error, e:
    print "ERROR: %s" % e
    res = 1

sys.exit(res)
