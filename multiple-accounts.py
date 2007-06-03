#!/bin/sh -
"exec" "python" "$0" "$@"

import random


class account:
    SERVER = {}
    PORT = {}
    USERNAME = {}
    PASSWORD = {}
    RESOURCE = {}
    COUNT = 0

GENERAL_CONFIG_FILE = 'accounts.txt'

fp = open(GENERAL_CONFIG_FILE, 'r')
GENERAL_CONFIG = eval(fp.read())
fp.close()

account.COUNT = int(GENERAL_CONFIG['account.COUNT'])

i=1
while i <= account.COUNT:
    account.SERVER[i] = GENERAL_CONFIG['account.SERVER' + '[' + str(i) + ']']
    account.PORT[i] = GENERAL_CONFIG['account.PORT' + '[' + str(i) + ']']
    account.USERNAME[i] = GENERAL_CONFIG['account.USERNAME' + '[' + str(i) + ']']
    account.PASSWORD[i] = GENERAL_CONFIG['account.PASSWORD' + '[' + str(i) + ']']
    account.RESOURCE[i] = GENERAL_CONFIG['account.RESOURCE' + '[' + str(i) + ']']
    print account.SERVER[i]
    print account.PORT[i]
    print account.USERNAME[i]
    print account.PASSWORD[i]
    print account.RESOURCE[i]
    i += 1
