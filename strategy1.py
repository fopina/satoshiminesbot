#!/usr/bin/env python
'''
Took this strategy from http://www.bitcointools.xyz/js/satoshimines/bot1.js
Similar to the roulette strategy "double when losing"
This is guaranteed to make you money (but lose even more)

So, what are the odds of blowing up?
Assuming you are rich and willing to game 1 BTC in satoshimines (really, just send it to me),
and that you start with a 30 bits bet

1 loss -> next bet = 769
2 losses in a row -> next bet = 19683
3 losses in a row -> next bet = 504475
4 losses in a row -> NO next bet possible because maximum bet is 1000000 (1 BTC)

Odds of that? 1/25^4 = 0.00025%, yup, really low, but you only make 1 bit per successful bet,
how many games will you be playing?!

Seriously, just send me some of those bitcoins, result is the same
Wallet: 1GagBVNaAEPQPJw5rZYnNaES4yv9btMNuT

kkthnx
'''

import satoshiminesbot
import time

MINES = 1
ORIGINAL_BET = 30
GUESSES = 1
MULTIPLIER = 25.63


def main(player_hash):
    bot = satoshiminesbot.SMB(player_hash)
    wins, losses, balance = 0, 0, 0

    bet = ORIGINAL_BET

    try:
        while True:
            done = True
            g = bot.new_game(bet, MINES)
            bits = 0
            for guess in xrange(GUESSES):
                f = g.play()
                if f['outcome'] == 'bomb':
                    balance -= bet
                    losses += 1
                    print('- %s bits - BAL: %d - %s' % (bet, balance, g.url()))
                    bet = int(bet * MULTIPLIER)
                    done = False
                    break
                elif f['outcome'] == 'bitcoins':
                    bet = ORIGINAL_BET
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
            time.sleep(2)
    except KeyboardInterrupt:
        print('Stopped')
        print('Session balance: %d - %d wins - %d losses' % (balance, wins, losses))


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        sys.stderr.write('Usage: %s PLAYER_HASH\n' % __file__)
        sys.exit(1)

    main(sys.argv[1])
