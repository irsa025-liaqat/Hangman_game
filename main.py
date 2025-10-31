
from pathlib import Path
from game.wordlist import WordList
from game.engine import HangmanEngine
from ui.display import Display

ROOT = Path(__file__).parent
GAME_LOG_DIR = ROOT / "game_log"
STATS_FILE = GAME_LOG_DIR / "stats.txt"

def load_stats():
    """Load game stats from a simple text file instead of JSON."""
    GAME_LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Default stats
    stats = {"games_played": 0, "wins": 0, "losses": 0, "total_score": 0}

    if not STATS_FILE.exists():
        save_stats(stats)
        return stats

    try:
        with STATS_FILE.open("r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    if key in stats:
                        stats[key] = int(value)
    except Exception:
        # If file corrupt or unreadable, recreate it
        save_stats(stats)
    return stats


def save_stats(stats):
    """Save stats to a plain text file."""
    with STATS_FILE.open("w", encoding="utf-8") as f:
        for key, value in stats.items():
            f.write(f"{key}={value}\n")


def choose_category(wordlist: WordList):
    """Display categories and let the player choose one."""
    display = Display()
    display.print_header("Welcome to Hangman!")
    cats = wordlist.available_categories()
    print("Choose a category (or press Enter for random):")
    for i, c in enumerate(cats, 1):
        print(f"  {i}. {c}")
    choice = input("Enter number or name: ").strip()
    if not choice:
        return None
    if choice.isdigit():
        i = int(choice) - 1
        if 0 <= i < len(cats):
            return cats[i]
    for c in cats:
        if c.lower() == choice.lower():
            return c
    print("Invalid input, selecting random.")
    return None


def main():
    wordlist = WordList(ROOT / "words")
    stats = load_stats()
    display = Display()

    while True:
        category = choose_category(wordlist)
        engine = HangmanEngine(wordlist, GAME_LOG_DIR, stats)
        engine.start_new_game(category)
        engine.play(display)
        stats = engine.update_stats_and_get()
        save_stats(stats)
        display.show_stats(stats)
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thankyou for playing!")
            break


if __name__ == "__main__":
    main()
