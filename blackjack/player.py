from hand import Hand


class Player:
    def __init__(self, bankroll=1000):
        self.bankroll = bankroll
        self.hand = None

    def place_bet(self, amount: int):
        if amount > self.bankroll:
            raise ValueError("Not enough bankroll")
        self.bankroll -= amount
        self.hand = Hand(bet=amount)
        return self.hand


class Dealer:
    def __init__(self):
        self.hand = None
