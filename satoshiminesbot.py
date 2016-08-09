#!/usr/bin/env python

import requests
from decimal import Decimal
from random import choice
import re


class SMB(object):
    def __init__(self, player_hash):
        self._hash = player_hash
        self._game = None
        self.balance = 0
        self.refresh_balance()

    def refresh_balance(self):
        r = self.get('play/%s/' % self._hash, to_json=False)
        self.balance = int(re.findall('<span class="num" title=".*?">([0-9,]+)</span>', r)[0].replace(',', ''))

    def new_game(self, bits_bet, num_mines):
        bits_bet = int(bits_bet)
        if not (30 <= bits_bet <= 1000000):
            raise SMBError(1, 'invalid bet')
        if num_mines not in [1, 3, 5, 24]:
            raise SMBError(2, 'invalid number of mines')

        r = self.post('action/newgame.php', {
            'bd': 1190,
            'player_hash': self._hash,
            'bet': Decimal(bits_bet) / 1000000,
            'num_mines': num_mines
        })
        if r['status'] != 'success':
            raise SMBError(99, r)
        return SMBGame(self, r)

    def get(self, url, to_json=True):
        try:
            r = requests.get('https://www.satoshimines.com/%s' % url)
        except requests.exceptions.ConnectionError as e:
            raise SMBError(90, e)
        if to_json:
            return r.json()
        else:
            return r.content

    def post(self, url, data):
        try:
            r = requests.post('https://www.satoshimines.com/%s' % url, data)
        except requests.exceptions.ConnectionError as e:
            raise SMBError(90, e)
        return r.json()


class SMBGame(object):
    def __init__(self, bot, info):
        self._bot = bot
        self._info = info
        self._board = range(1, 26)
        self._url = (None, None)

    def play(self, guess=None):
        if guess is None:
            guess = choice(self._board)
            self._board.remove(guess)
        else:
            if guess not in self._board:
                raise SMBError(3, 'invalid guess')

        r = self._bot.post('action/checkboard.php', {
            'game_hash': self._info['game_hash'],
            'guess': guess,
            'v04': 1
        })

        if r['status'] != 'success':
            raise SMBError(99, r)

        self._url = (r.get('game_id'), r.get('random_string'))
        return r

    def cashout(self):
        r = self._bot.post('action/cashout.php', {
            'game_hash': self._info['game_hash'],
        })

        if r['status'] != 'success':
            raise SMBError(99, r)

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
