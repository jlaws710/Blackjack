from dataclasses import dataclass, field
from typing import List
from deck import Card, VALUES


@dataclass
class Hand:
    cards: List[Card] = field(default_factory=list)
    bet: int = 0
    doubled: bool = False

    def add(self, card: Card):
        self.cards.append(card)

    def value(self) -> int:
        total = sum(VALUES[c.rank] for c in self.cards)
        aces = sum(1 for c in self.cards if c.rank == "A")
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.value() == 21

    def is_bust(self) -> bool:
        return self.value() > 21

    def show(self, hide_first=False) -> str:
        if hide_first:
            return "[??] " + " ".join(str(c) for c in self.cards[1:])
        return " ".join(str(c) for c in self.cards)
