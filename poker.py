__author__ = 'jargote'

import random


class Card(object):
    SUITS = {'d': u'\u2664',
             's': u'\u2666',
             'h': u'\u2665',
             'c': u'\u2663'}
    NUMBERS = {'2': 1,
               '3': 2,
               '4': 3,
               '5': 4,
               '6': 5,
               '7': 6,
               '8': 7,
               '9': 8,
               '10': 9,
               'J': 10,
               'Q': 11,
               'K': 12,
               'A': 13,}

    def __init__(self, number, suit):
        self._suit = suit
        self._number = number

    def __unicode__(self):
        return unicode('%s%s' % (self._number, self.SUITS[self._suit]))

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    @property
    def number(self):
        return self._number

    @property
    def suit(self):
        return self._suite


    def __cmp__(self, other):
        if self.NUMBERS[self.number] > self.NUMBERS[other.number]:
            return 1
        elif self.NUMBERS[self.number] < self.NUMBERS[other.number]:
            return -1
        elif self.NUMBERS[self.number] == self.NUMBERS[other.number]:
            return 0


class Deck(list):
    def __init__(self):
        self._unpack()

    def _unpack(self):
        for suit, chr in Card.SUITS.items():
            for number, order in Card.NUMBERS.items():
                new_card = Card(number, suit)
                self.append(new_card)

    def draw(self):
        left = self.__len__()
        if left > 0:
            index = random.randint(0, left-1)
            return self.pop(index)
        return None


class WinningHand(object):
    NAME = None
    PRIORITY = None

    def __init__(self):
        assert self.NAME is not None
        assert self.PRIORITY is not None

    def eval(self):
        raise NotImplementedError


class PokerEngine(object):
    pass


class HighestCard(WinningHand):
    NAME = 'Highest Card'
    PRIORITY = 1

    def eval(self, cards):
        return max(cars)
