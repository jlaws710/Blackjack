import tkinter as tk
from tkinter import messagebox
from blackjack.game import BlackjackGame


class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")

        self.game = BlackjackGame(bankroll=500)

        # Frames
        self.info_frame = tk.Frame(root)
        self.info_frame.pack(pady=10)

        self.dealer_frame = tk.LabelFrame(root, text="Dealer", padx=10, pady=10)
        self.dealer_frame.pack(padx=10, pady=5)

        self.player_frame = tk.LabelFrame(root, text="Player", padx=10, pady=10)
        self.player_frame.pack(padx=10, pady=5)

        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack(pady=10)

        # Info labels
        self.bankroll_label = tk.Label(self.info_frame, text=f"Bankroll: {self.game.player.bankroll}")
        self.bankroll_label.pack()

        # Dealer + player hand labels
        self.dealer_label = tk.Label(self.dealer_frame, text="")
        self.dealer_label.pack()

        self.player_label = tk.Label(self.player_frame, text="")
        self.player_label.pack()

        # Controls
        self.bet_entry = tk.Entry(self.controls_frame, width=10)
        self.bet_entry.insert(0, "50")
        self.bet_entry.grid(row=0, column=0, padx=5)

        self.bet_button = tk.Button(self.controls_frame, text="Place Bet", command=self.start_round)
        self.bet_button.grid(row=0, column=1, padx=5)

        self.hit_button = tk.Button(self.controls_frame, text="Hit", state="disabled", command=self.hit)
        self.hit_button.grid(row=1, column=0, padx=5)

        self.stand_button = tk.Button(self.controls_frame, text="Stand", state="disabled", command=self.stand)
        self.stand_button.grid(row=1, column=1, padx=5)

    def start_round(self):
        try:
            bet = int(self.bet_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid bet amount")
            return

        if bet < self.game.min_bet or bet > min(self.game.max_bet, self.game.player.bankroll):
            messagebox.showerror("Error", "Invalid bet size")
            return

        self.hand = self.game.player.place_bet(bet)
        self.dealer_hand = self.game.dealer.hand = self.hand.__class__()

        for _ in range(2):
            self.hand.add(self.game.deck.deal())
            self.dealer_hand.add(self.game.deck.deal())

        self.update_ui(hide_dealer=True)

        # Disable bet button, enable game actions
        self.bet_button.config(state="disabled")
        self.hit_button.config(state="normal")
        self.stand_button.config(state="normal")

    def hit(self):
        self.hand.add(self.game.deck.deal())
        self.update_ui(hide_dealer=True)

        if self.hand.is_bust():
            self.end_round()

    def stand(self):
        # Dealer plays
        while self.dealer_hand.value() < 17:
            self.dealer_hand.add(self.game.deck.deal())
        self.end_round()

    def end_round(self):
        self.update_ui(hide_dealer=False)
        net = self.game.settle(self.hand, self.dealer_hand)
        if net >= 0:
            self.game.player.bankroll += self.hand.bet + net
        self.update_bankroll()

        # Disable actions, re-enable betting
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")
        self.bet_button.config(state="normal")

        if self.game.player.bankroll < self.game.min_bet:
            messagebox.showinfo("Game Over", "You don't have enough bankroll left!")
            self.root.quit()

    def update_ui(self, hide_dealer=False):
        dealer_text = self.dealer_hand.show(hide_first=hide_dealer)
        player_text = f"{self.hand.show()}  (total {self.hand.value()})"
        self.dealer_label.config(text=dealer_text)
        self.player_label.config(text=player_text)

    def update_bankroll(self):
        self.bankroll_label.config(text=f"Bankroll: {self.game.player.bankroll}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()
