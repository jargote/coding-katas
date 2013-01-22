__author__ = 'jargote'

import random
import os

def cls():
    os.system('clear')

class NotEnoughCredit(Exception):
    pass

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

    def __cmp__(self, other):
        return cmp(self.NUMBERS[self.number], self.NUMBERS[other.number])

    @property
    def number(self):
        return self._number

    @property
    def suit(self):
        return self._suite


class CardList(list):
    def __str__(self):
        if self.__len__() > 0:
            return '  '.join([str(item) for item in self])
        return 'No cards.'


class PlayerList(list):
    def __str__(self):
        if self.__len__() > 0:
            return '\n'.join([str(item) for item in self])
        return 'No players.'


class Deck(CardList):
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


class Rules(object):
    # Blinds
    SMALL_BLIND = 5.0
    BIG_BLIND = 10.0
    # Blinds increment scale. small_blind = (small_blind * raise_scale)
    RAISE_SCALE = 2
    # Poker hands before raising the blinds.
    RAISE_AFTER = 10


class Visuals(object):
    def _header(self):
        print '-'*60
        print '\t\t\tPoker 1.0'
        print '-'*60

    def _winner(self, winner):
        print '-'*60
        print '\t\t\tWINNER: %s $%0.3f' % (winner.name, winner.wallet)
        print '-'*60

class Game(Visuals):
    # Game states
    PLAY = 1
    EXIT = 0

    # Poker hand states
    DEAL = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
    CRFA = 5 # Check, Raise, Fold or All-in
    WINNER = 4

    def __init__(self, n_players, wallet):
        # Game settings.
        self._players = PlayerList()
        self._players_out = PlayerList()
        self._deck = Deck()
        self._wallet = wallet

        # Attributes updated on each round.
        self._board = CardList()
        self._burnt = CardList()
        self._winning_pot = 0.0
        self._hands_played = 0

        # Represents the indexes (players list) of the blinds.
        self._small_blind = Rules.SMALL_BLIND
        self._big_blind = Rules.BIG_BLIND
        self._blinds_index = (0, 1)

        # Add players and sort them by order of play.
        self._init_players(n_players)

    def _init_players(self, n_players=0):
        if not self._players:
            for n in range(n_players):
                player = Player('Player%s' % n, self._wallet)
                self._players.append(player)
        else:
            for player in self._players:
                player.reset_cards()

    def _remove_player(self, player):
        self._players_out.append(player)
        self._players.remove(player)
        # Recalculate blinds again
        self._set_blinds()

    def _new_hand(self):
        self._hands_played += 1
        # Check if blinds have to be raised.
        if self._hands_played % Rules.RAISE_AFTER == 0:
            self._small_blind *= Rules.RAISE_SCALE
            self._big_blind *= Rules.RAISE_SCALE
        self._board = CardList()
        self._burnt = CardList()
        self._deck = Deck()
        self._init_players()
        self._set_blinds()

    def _set_blinds(self):
        self._blinds_index = ((self._blinds_index[0] + 1) % len(self._players),
                              (self._blinds_index[1] + 1) % len(self._players))

    def _get_blind(self, index=0):
        player_index = 0
        if index in (0, 1):
            player_index = self._blinds_index[index]
        return self._players[player_index]

    def _show_blinds(self):
        print 'Blinds: '
        print '\tSmall: $%0.2f (%s)' % (self._small_blind,
                                        self._get_blind(0).name)
        print '\tBig: $%0.2f (%s)' % (self._big_blind,
                                      self._get_blind(1).name)

    def _deal_to_players(self):
        print '\n', '-'*50
        print 'Dealing card to players ...'
        print '-'*50
        raw_input('\nPress any key to continue.')
        cls()

        for player in self._players:
            try:
                if player == self._get_blind(0):
                    self._charge_player(player, self._small_blind)
                elif player == self._get_blind(1):
                    self._charge_player(player, self._big_blind)
            except NotEnoughCredit:
                print '%s: RAN OUT OF CREDIT' % player.name
                self._remove_player(player)

            player.take_card(self._deck.draw())
            player.take_card(self._deck.draw())



    def _deal(self, n_to_deal, n_to_burn):
        for n in range(n_to_burn):
            self._burnt.append(self._deck.draw())

        for n in range(n_to_deal):
            self._board.append(self._deck.draw())

    def _check_raise_fold_allin(self):
        print '\n'
        for n, player in enumerate(self._players):
            opt = raw_input('Player%s: Check(c), Raise(r), Fold(f), '
                            'All-in(a)? ' % n)

    def _charge_player(self, player, amount):
        if player.wallet < amount:
            raise NotEnoughCredit
        player.wallet -= amount
        self._winning_pot += amount

    def _pay_player(self, player, amount):
        player.wallet += amount
        self._winning_pot -= amount

    def _game_status(self):
        # Game header
        self._header()

        # Printing cards dealt
        print 'Hand # %d' % (self._hands_played+1)
        print 'Cards Dealt: %s' % self._board
        print 'Cards Burnt: %s' % self._burnt

        # Current winning pot
        print 'Winning pot: $%0.2f' % self._winning_pot

        # Blinds
        self._show_blinds()

        # Printing players games
        print self._players

    def _control(self, state=0):
        if state == Game.DEAL:
            # deal cards to players
            self._deal_to_players()

        elif state == Game.CRFA:
            return self._check_raise_fold_allin()

        elif state == Game.FLOP:
            print '\n', '-'*50
            print 'Dealing the FLOP ...'
            print '-'*50
            raw_input('\nPress any key to continue.')
            cls()

            self._deal(3, 1)

        elif  state == Game.TURN:
            # deal river
            print '\n', '-'*50
            print 'Dealing the TURN ...'
            print '-'*50
            raw_input('\nPress any key to continue.')
            cls()

            self._deal(1, 1)

        elif state == Game.RIVER:
            # deal river
            print '\n', '-'*50
            print 'Dealing the RIVER ...'
            print '-'*50
            raw_input('\nPress any key to continue.')
            cls()

            self._deal(1, 1)

        elif state == Game.WINNER:
            # Check for winner

            if len(self._players) == 1:
                self._winner(self._players.pop())
                return Game.EXIT

            self._new_hand()
            return Game.PLAY

        # Showing status of the game.
        self._game_status()
        # Check, Raise or Fold?
        self._control(state=Game.CRFA)

        # Next move to next state
        return self._control(state=state+1)

    def play(self, state=1):
        while(state is not Game.EXIT):
            state = self._control()

    @classmethod
    def set_up(cls):
        while True:
            print '-'*60
            print '\t\t\tPoker 1.0'
            print '-'*60
            try:
                n_players = int(raw_input('Please type number of players: '))
                wallet = int(raw_input('Starting money for each player: $'))
                break
            except Exception as e:
                print 'Please type a valid number.'

        return Game(n_players, wallet)

    @classmethod
    def run(cls):
        game = Game.set_up()
        game.play()


class Player(object):
    def __init__(self, name, wallet):
        self.wallet = wallet
        self.cards = CardList()
        self.name = name
        self.order_of_play = 0

    def __str__(self):
        # Player's name.
        out = '\n%s:' % self.name
        # Cards dealt to player.
        out += '\n\t%s' % self.cards
        # Player's wallet.
        out += '\n\t$%0.2f' % self.wallet
        return out

    def take_card(self, card):
        if len(self.cards) == 2:
            print '%s: Thanks, I already have 2 cards.' % self.name
        else:
            self.cards.append(card)

    def reset_cards(self):
        self.cards = CardList()


class WinningHand(object):
    NAME = None
    PRIORITY = None

    def __init__(self):
        assert self.NAME is not None
        assert self.PRIORITY is not None

    def eval(self):
        raise NotImplementedError


#class HighestCard(WinningHand):
#    NAME = 'Highest Card'
#    PRIORITY = 1
#
#    def eval(self, cards):
#        return max(cars)