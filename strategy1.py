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

MINES = 1
GUESSES = 1
BETS = [30, 751, 18776, 469401]


def main(player_hash, initial_balance=0):
    bot = satoshiminesbot.SMB(player_hash)
    wins, losses = 0, 0
    balance = int(initial_balance)

    bet_ind = 0

    try:
        while True:
            done = True
            bet = BETS[bet_ind]

            if initial_balance and bet > balance:
                print('Not enough balance for this bet...')
                exit(1)

            try:
                g = bot.new_game(bet, MINES)
            except Exception as e:
                # unexpected error, let's ignore and try again
                print(e)
                time.sleep(5)
                continue
            bits = 0
            for guess in xrange(GUESSES):
                f = g.play()
                if f['outcome'] == 'bomb':
                    balance -= bet
                    losses += 1
                    print('- %s bits - BAL: %d - %s' % (bet, balance, g.url()))
                    bet_ind += 1
                    if bet_ind >= len(BETS):
                        print('You should have cut your losses sooner....')
                        exit(1)
                    done = False
                    break
                elif f['outcome'] == 'bitcoins':
                    bet_ind = 0
                    bits += int(f['change'] * 1000000)
                else:
                    print('wtf?!')
                    print(f)
                    raise Exception('STOP!')
            if done:
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
    import sys

    if len(sys.argv) < 2:
        sys.stderr.write('Usage: %s PLAYER_HASH\n' % __file__)
        sys.exit(1)

    main(*sys.argv[1:])
