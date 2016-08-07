# satoshiminesbot
Just because... everyone should be able to quickly burn a few satoshi.

Usage
=====

Go to [satoshimines.com](https://satoshimines.com/a/Js6e) and click _Start playing_

The URL should now look something like `https://satoshimines.com/play/767ca91bec38197612349e3867dbbb914f6bf70b/#DONT_SHARE_URL`

`767ca91bec38197612349e3867dbbb914f6bf70b` (not this specific one but whatever shows there in your url) is your _PLAYER_HASH_

```
$ ./satoshiminesbot.py 
Usage: ./satoshiminesbot.py PLAYER_HASH BET_IN_BITS NUMBER_OF_MINES NUMBER_OF_GUESSES

$ ./satoshiminesbot.py 767ca91bec38197612349e3867dbbb914f6bf70b 30 3 4
- 30 bits - BAL: -30 - https://satoshimines.com/s/96950248/C8SIlzHVeLXu/
+ 18 bits - BAL: -12 - https://satoshimines.com/s/96950252/NmfM2N169TmH/
- 30 bits - BAL: -42 - https://satoshimines.com/s/96950264/fBcJtt59awh6/
+ 18 bits - BAL: -24 - https://satoshimines.com/s/96950269/1OM0zmXIRx0T/
+ 18 bits - BAL: -6 - https://satoshimines.com/s/96950283/K1ijF774AemN/
...
^CStopped
Session balance: -6 - 3 wins - 2 losses
```

The default _strategy_ is _no strategy_ as it always bets the same. That means you have 1/25 chance of losing 30 bits and you only make 1 bit per win. If you make the math, that means you make 24 and then lose 30, so _sure win_ right?!

But it's easy to implement your own _SureWin_ strategy such as [strategy1](strategy1.py). That is an obvious win (RIGHT?!)!

Feel free to start a new game (even if you have one) with my [affiliate link](https://satoshimines.com/a/Js6e) so I can make something with your losses.

Or if you really like to burn money, just send some of it over to `1GagBVNaAEPQPJw5rZYnNaES4yv9btMNuT`
