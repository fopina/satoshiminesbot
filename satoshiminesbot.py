#!/usr/bin/env python

import requests
from decimal import Decimal
from random import choice


class SMB(object):
    def __init__(self, player_hash):
        self._hash = player_hash
        self._game = None

    def new_game(self, bits_bet, num_mines):
        if not (30 <= bits_bet <= 1000000):
            raise SMBError('invalid bet')
        if num_mines not in [1, 3, 5, 24]:
            raise SMBError('invalid number of mines')

        r = requests.post('https://www.satoshimines.com/action/newgame.php', data={
            'bd': 1190,
            'player_hash': self._hash,
            'bet': Decimal(bits_bet) / 1000000,
            'num_mines': num_mines
        }).json()
        if r['status'] != 'success':
            raise SMBError('failed to start game')
        return SMBGame(r)


class SMBGame(object):
    def __init__(self, info):
        self._info = info
        self._board = range(1, 26)
        self._url = (None, None)

    def play(self, guess=None):
        if guess is None:
            guess = choice(self._board)
            self._board.remove(guess)
        else:
            if guess not in self._board:
                raise SMBError('invalid guess')

        r = requests.post('https://www.satoshimines.com/action/checkboard.php', data={
            'game_hash': self._info['game_hash'],
            'guess': guess,
            'v04': 1
        }).json()

        if r['status'] != 'success':
            raise SMBError('failed to play')

        self._url = (r.get('game_id'), r.get('random_string'))
        return r

    def cashout(self):
        r = requests.post('https://www.satoshimines.com/action/cashout.php', data={
            'game_hash': self._info['game_hash'],
        }).json()

        if r['status'] != 'success':
            raise SMBError('failed to cashout')

        self._url = (r.get('game_id'), r.get('random_string'))
        return r

    def url(self):
        return 'https://satoshimines.com/s/%s/%s/' % self._url


class SMBError(Exception):
    pass


def main(player_hash, bet, mines, guesses):
    bot = SMB(player_hash)
    wins, losses, balance = 0, 0, 0
    try:
        while True:
            done = True
            g = bot.new_game(int(bet), int(mines))
            bits = 0
            for guess in xrange(int(guesses)):
                f = g.play()
                if f['outcome'] == 'bomb':
                    balance -= int(bet)
                    losses += 1
                    print('- %s bits - BAL: %d - %s' % (bet, balance, g.url()))
                    done = False
                    break
                elif f['outcome'] == 'bitcoins':
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
    except KeyboardInterrupt:
        print('Stopped')
        print('Session balance: %d - %d wins - %d losses' % (balance, wins, losses))


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 5:
        sys.stderr.write('Usage: %s PLAYER_HASH BET_IN_BITS NUMBER_OF_MINES NUMBER_OF_GUESSES\n' % __file__)
        sys.exit(1)

    main(*sys.argv[1:5])
