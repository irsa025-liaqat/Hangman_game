from pathlib import Path
from .ascii_art import get_state
from datetime import datetime

MAX_WRONG = 6

class HangmanEngine:
    def __init__(self, wordlist, logs_dir: Path, stats: dict):
        self.wordlist = wordlist
        self.logs_dir = Path(logs_dir)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.stats = stats or {"games_played": 0, "wins": 0, "losses": 0, "total_score": 0}

    def start_new_game(self, category=None):
        self.word, self.word_length, self.category = self.wordlist.random_word(category)
        self.guessed, self.correct, self.wrong_letters = set(), set(), []
        self.wrong_guesses = 0
        self.start_time = datetime.now()
        self.game_num = self._next_game_num()
        self.game_dir = self.logs_dir / f"game{self.game_num}"
        self.game_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.game_dir / "log.txt"
        self._write_log_header()

    def _next_game_num(self):
        nums = [int(f.name.replace("game", "")) for f in self.logs_dir.glob("game*") if f.is_dir() and f.name[4:].isdigit()]
        return max(nums, default=0) + 1

    def _write_log_header(self):
        text = [
            f"Game {self.game_num} Log",
            f"Category: {self.category}",
            f"Word: {self.word}",
            f"Word Length: {self.word_length}",
            "", "Guesses (in order):"
        ]
        self.log_file.write_text("\n".join(text), encoding="utf-8")

    def _append_log(self, line): 
        with self.log_file.open("a", encoding="utf-8") as f: 
            f.write(line + "\n")

    def current_progress(self):
        return " ".join([c if c in self.correct else "_" for c in self.word])

    def guess_letter(self, ch):
        ch = ch.lower()
        if not (ch.isalpha() and len(ch) == 1):
            return False, "Invalid input."
        if ch in self.guessed:
            return False, f"You already guessed '{ch}'."
        self.guessed.add(ch)
        if ch in self.word:
            self.correct.add(ch)
            self._append_log(f"{len(self.guessed)}. {ch} -> Correct")
            return True, "Correct!"
        else:
            self.wrong_guesses += 1
            self.wrong_letters.append(ch)
            self._append_log(f"{len(self.guessed)}. {ch} -> Wrong")
            return False, "Wrong!"

    def guess_full_word(self, attempt):
        attempt = attempt.strip().lower()
        if attempt == self.word:
            self.correct.update(self.word)
            self._append_log(f"Full-word guess '{attempt}' -> Correct")
            return True, "Correct! You guessed the word!"
        else:
            self.wrong_guesses += 1
            self._append_log(f"Full-word guess '{attempt}' -> Wrong")
            return False, "Wrong full-word guess."

    def is_won(self): return all(c in self.correct for c in self.word)
    def is_lost(self): return self.wrong_guesses >= MAX_WRONG
    def remaining(self): return MAX_WRONG - self.wrong_guesses
    def get_ascii(self): return get_state(self.wrong_guesses)
    def compute_score(self): return 0 if not self.is_won() else max(0, self.word_length * 10 - self.wrong_guesses * 5)

    def finalize(self, result, score):
        self._append_log("")
        self._append_log(f"Result: {result}")
        self._append_log(f"Score: {score}")
        self._append_log(f"Time: {datetime.now()}")

    def update_stats_and_get(self):
        self.stats["games_played"] += 1
        if self.is_won(): self.stats["wins"] += 1
        else: self.stats["losses"] += 1
        self.stats["total_score"] += self.compute_score()
        return self.stats

    def play(self, display):
        hints = self.wordlist.words_of_length(self.category, self.word_length)
        display.print_new_word(self.category, self.word_length, hints)
        while True:
            display.show_state(self.current_progress(), self.guessed, self.remaining(), self.get_ascii())
            cmd = display.prompt_input()
            if cmd is None:
                print("Exiting game...")
                break
            if cmd == "guess":
                attempt = display.prompt_full_word()
                ok, msg = self.guess_full_word(attempt)
                display.print_message(msg)
            else:
                ok, msg = self.guess_letter(cmd)
                display.print_message(msg)
            if self.is_won():
                score = self.compute_score()
                display.show_win(self.word, score)
                self.finalize("Win", score)
                break
            if self.is_lost():
                display.show_loss(self.word)
                self.finalize("Loss", 0)
                break
