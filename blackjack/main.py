from blackjack.game import BlackjackGame

if __name__ == "__main__":
    game = BlackjackGame(bankroll=1000, min_bet=10, max_bet=1000)
    print("="*50)
    print("Blackjack — Created by jlaws710")
    print("Type 'q' at any prompt to quit.")
    print("="*50)

    while game.player.bankroll >= game.min_bet:
        game.play_round()
        if game.player.bankroll < game.min_bet:
            print("You're below the table minimum. Game over!.")
            break
        again = input("Play another round? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            break
    print("Thanks for playing!")