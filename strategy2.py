#!/usr/bin/env python
'''
Same as strategy1 but using 5 mines (resulting a smaller multiplier)

Seriously, just send me some of those bitcoins, result is the same
Wallet: 1GagBVNaAEPQPJw5rZYnNaES4yv9btMNuT

kkthnx
'''

import strategy1
import sys

strategy1.MINES = 5
strategy1.MULTIPLIER = 1 / 0.24

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: %s PLAYER_HASH\n' % __file__)
        sys.exit(1)

    strategy1.main(*sys.argv[1:])
