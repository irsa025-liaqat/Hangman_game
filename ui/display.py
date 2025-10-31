class Display:
    def print_header(self, text):
        print("=" * 40)
        print(text)
        print("=" * 40)

    def print_new_word(self, category, length, hints):
        cat = category if category else "Random"
        print(f"\nNew word selected from '{cat}' (length {length})")
        if hints:
            print(f"Hint: possible {cat.lower()} word(s) with {length} letters -> {', '.join(hints)}")
        else:
            print("No hints available for this length.")
        print()

    def show_state(self, progress, guessed, remaining, ascii_art):
        print("\n" + progress + "\n")
        print("Guessed letters:", ", ".join(sorted(guessed)) if guessed else "(none)")
        print("Remaining attempts:", remaining)
        print(ascii_art)

    def prompt_input(self):
        raw = input("\nEnter a letter (or 'guess' for full word, 'quit' to exit): ").strip()
        if not raw: return ""
        if raw.lower() in ("quit", "exit"): return None
        if raw.lower() == "guess": return "guess"
        if len(raw) == 1 and raw.isalpha(): return raw.lower()
        print("Invalid input.")
        return ""

    def prompt_full_word(self): return input("Enter full-word guess: ").strip()
    def print_message(self, msg): print(msg)
    def show_win(self, word, score): print(f"\n🎉 You win! The word was '{word}'. Score: {score}")
    def show_loss(self, word): print(f"\n💀 You lost! The word was '{word}'.")
    def show_stats(self, stats):
        g, w, l, t = stats.values()
        winrate = (w / g * 100) if g else 0
        avg = (t / g) if g else 0
        print(f"\nGames: {g} | Wins: {w} | Losses: {l} | WinRate: {winrate:.2f}% | Avg: {avg:.2f}")
