from deck import Deck
from player import Player, Dealer
from blackjack.util.utils import prompt_int


class BlackjackGame:
    def __init__(self, bankroll=1000, min_bet=10, max_bet=500):
        self.deck = Deck()
        self.player = Player(bankroll)
        self.dealer = Dealer()
        self.min_bet = min_bet
        self.max_bet = max_bet

    def settle(self, player, dealer):
        bet = player.bet * (2 if player.doubled else 1)
        if player.is_blackjack() and not dealer.is_blackjack():
            win = int(player.bet * 1.5)
            print(f"Blackjack! You win {win}.")
            return win
        if dealer.is_blackjack() and not player.is_blackjack():
            print("Dealer has blackjack. You lose.")
            return -player.bet
        if player.is_bust():
            print("You busted. You lose.")
            return -bet
        if dealer.is_bust():
            print(f"Dealer busts. You win {bet}.")
            return bet
        if player.value() > dealer.value():
            print(f"You win {bet}.")
            return bet
        elif player.value() < dealer.value():
            print("You lose.")
            return -bet
        else:
            print("Push. Your bet is returned.")
            return 0

    def play_round(self):
        print(f"\nBankroll: {self.player.bankroll}")
        max_allowed = min(self.max_bet, self.player.bankroll)
        bet = prompt_int(f"Place your bet ({self.min_bet}-{max_allowed}): ",
                         self.min_bet, max_allowed)
        hand = self.player.place_bet(bet)
        dealer_hand = self.dealer.hand = self.player.hand.__class__()  # same Hand class

        for _ in range(2):
            hand.add(self.deck.deal())
            dealer_hand.add(self.deck.deal())

        print(f"Dealer: {dealer_hand.show(hide_first=True)}")
        print(f"You:    {hand.show()}  (total {hand.value()})")

        # Handle player actions

        # Dealer plays
        print(f"Dealer reveals: {dealer_hand.show()}  (total {dealer_hand.value()})")
        while dealer_hand.value() < 17:
            c = self.deck.deal()
            dealer_hand.add(c)
            print(f"Dealer hits and draws {c}. Total {dealer_hand.value()}")

        # Settle
        net = self.settle(hand, dealer_hand)
        self.player.bankroll += hand.bet + net if net >= 0 else 0
        print(f"Bankroll now: {self.player.bankroll}")
