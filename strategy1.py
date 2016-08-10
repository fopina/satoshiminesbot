#!/usr/bin/env python
'''
Took this strategy from http://www.bitcointools.xyz/js/satoshimines/bot1.js
Similar to the roulette strategy "double when losing"
This is guaranteed to make you money (but lose even more)

So, what are the odds of blowing up?
Assuming you are rich and willing to game 1 BTC in satoshimines (really, just send it to me),
and that you start with a 30 bits bet (multiplier is something like 25.001 but these are the minimum values manually confirmed)

1 loss -> next bet = 751 (to win 30)
2 losses in a row -> next bet = 18776 (to win 751)
3 losses in a row -> next bet = 469401 (to win 18776)
4 losses in a row -> NO next bet possible because maximum bet is 1000000 (1 BTC) which only gives 39999 bits

Odds of that? 1/25^4 = 0.00025%, yup, really low, but you only make 1 bit per successful bet,
how many games will you be playing?!

Seriously, just send me some of those bitcoins, result is the same
Wallet: 1GagBVNaAEPQPJw5rZYnNaES4yv9btMNuT

kkthnx
'''

import satoshiminesbot
import time
import sys

MINES = 1
GUESSES = 1
MULTIPLIER = 25
INITIAL_BET = 30


def main(player_hash, initial_balance=0):
    bot = satoshiminesbot.SMB(player_hash)
    wins, losses = 0, 0
    if not initial_balance:
        initial_balance = bot.balance
    balance = int(initial_balance)

    bet = INITIAL_BET

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
            bits = 0
            for guess in xrange(GUESSES):
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
                    # also cover previously lost bet (if this is not initial bet)
                    bet = bet * MULTIPLIER + (1 if bet == INITIAL_BET else bet)
                    done = False
                    break
                elif f['outcome'] == 'bitcoins':
                    bet = INITIAL_BET
                    bits += int(f['change'] * 1000000)
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
                balance += bits
                wins += 1
                print('+ %s bits - BAL: %d - %s' % (bits, balance, g.url()))
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
