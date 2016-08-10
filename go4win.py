#!/usr/bin/env python
'''
For the kicks, try to win a game!

I wouldn't recommend less than 24 mines:

Win probability:
24 mines - 1/25 = 0.04
5 mines - 24/25*23/24*...*1/6 = 0.000018

Seriously, just send me some of those bitcoins, result is the same
Wallet: 1GagBVNaAEPQPJw5rZYnNaES4yv9btMNuT

kkthnx
'''

import satoshiminesbot
import time
import sys

MINES = 24
BET = 100000


def main(player_hash):
    bot = satoshiminesbot.SMB(player_hash)
    wins, losses, balance = 0, 0, 0

    try:
        while True:
            done = False
            try:
                g = bot.new_game(BET, MINES)
            except satoshiminesbot.SMBError as e:
                if e[0] != 90:
                    raise
                # network error, just retry
                time.sleep(3)
                continue
            guesses = 0
            while not done and guesses < (25 - MINES):
                try:
                    f = g.play()
                except satoshiminesbot.SMBError as e:
                    if e[0] != 90:
                        raise
                    # network error, just retry
                    time.sleep(3)
                    continue
                guesses += 1
                if f['outcome'] == 'bomb':
                    losses += 1
                    balance -= BET
                    print('BAL: %d - PLAYS: %d - %s' % (balance, guesses, g.url()))
                    done = True
                elif f['outcome'] == 'bitcoins':
                    continue
                else:
                    raise Exception('STOP! WTF?', f)
            if not done:
                wins = 1
                # no way we miss this cashout!
                while not done:
                    try:
                        m = g.cashout()
                        done = True
                    except satoshiminesbot.SMBError as e:
                        if e[0] != 90:
                            raise
                        # network error, try again!!!
                        time.sleep(3)
                print('%s ONLY lost %d bits' % (m['message'], abs(balance)))
                print('Share only this game, not the ones you lost: %s' % g.url())
                break
            # let's give the server a break...
            time.sleep(1)
    except KeyboardInterrupt:
        print('Stopped')
    print('Session balance: %d wins - %d losses' % (wins, losses))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: %s PLAYER_HASH\n' % __file__)
        sys.exit(1)

    main(*sys.argv[1:])
