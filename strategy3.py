#!/usr/bin/env python
'''
This strategy relies on going crazy ONCE and then playing only with the profit from that play (until you lose it all).
This is guaranteed to make you money (but lose even more)

Seriously, just send me some of those bitcoins, result is the same
Wallet: 1GagBVNaAEPQPJw5rZYnNaES4yv9btMNuT

kkthnx
'''

import satoshiminesbot
import time
import sys

MINES = 1
GUESSES = 1
INITIAL_BET = 5000


def main(player_hash, initial_balance=0):
    bot = satoshiminesbot.SMB(player_hash)
    wins, losses = 0, 0
    if not initial_balance:
        initial_balance = bot.balance
    balance = int(initial_balance)

    bet = INITIAL_BET
    bits2bet = 0

    try:
        while True:
            done = True

            if initial_balance and bet > balance:
                sys.stderr.write('Not enough balance for this bet...\n')
                exit(1)

            try:
                g = bot.new_game(bet, MINES)
            except satoshiminesbot.SMBError as e:
                if e[0] != 90:
                    raise
                # network error, just retry
                time.sleep(3)
                continue
            try:
                f = g.play()
            except satoshiminesbot.SMBError as e:
                if e[0] != 90:
                    raise
                # network error, just retry
                time.sleep(3)
                continue
            if f['outcome'] == 'bomb':
                balance -= bet
                losses += 1
                print('- %s bits - BAL: %d - %s' % (bet, balance, g.url()))
                # go back to the CRAZY bet
                bet = INITIAL_BET
                done = False
            elif f['outcome'] == 'bitcoins':
                bits2bet += int(f['change'] * 1000000) - 1
                bet = bits2bet
            else:
                raise Exception('STOP! WTF?', f)
            if done:
                try:
                    g.cashout()
                except satoshiminesbot.SMBError as e:
                    sys.stderr.write('missed a cashout for %s\n' % g._info['game_hash'])
                    if e[0] != 90:
                        raise
                    # network error, try again otherwise we miss the cashout!!!
                    time.sleep(3)
                    g.cashout()
                balance += int(f['change'] * 1000000)
                wins += 1
                print('+ %s bits - BAL: %d - %s' % (int(f['change'] * 1000000), balance, g.url()))
            # let's give the server a break...
            time.sleep(1)
    except KeyboardInterrupt:
        print('Stopped')
        print('Session balance: %d - %d wins - %d losses' % (balance, wins, losses))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: %s PLAYER_HASH\n' % __file__)
        sys.exit(1)

    main(*sys.argv[1:])
