import sys


def prompt_int(prompt, low, high):
    while True:
        try:
            val = input(prompt).strip()
            if val.lower() in ("q", "quit", "exit"):
                print("Goodbye!")
                sys.exit(0)
            n = int(val)
            if low <= n <= high:
                return n
            print(f"Enter a number between {low} and {high}.")
        except ValueError:
            print("Please enter a valid number.")
