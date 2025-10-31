# Hangman Game

## How to run
Run the game by executing `main.py` inside the `hangman_game/` folder:


python main.py
## Wordlist Format and Categories

* **File:** Words are stored in `words/words.txt`.
* **Format:** Each word is on a new line. Words are associated with a category using the format `word:Category`.
    * Example: `python:Programming`
    * Words without a category tag are assigned to the `General` category.
* **Required Categories:** The game supports the following categories, and words must be provided for them:
    * `Animals`
    * `Countries`
    * `Programming`
    * `Science`

## Scoring Method

A player only scores points upon winning a round. The score is calculated using the following formula:

$$\text{Score} = \max(0, (\text{Word Length} \times 10) - (\text{Wrong Guesses} \times 5))$$

* The maximum number of wrong guesses allowed is 6.
* A wrong full-word guess counts as one wrong guess.

## How Logs are Saved

* **Log Directory:** All logs are saved under the `game_log/` directory.
* **Automatic Folders:** For every new game, a new, unique folder is automatically created (e.g., `game_log/game1/`, `game_log/game2/`, etc.) to prevent overwriting.
* **Log File:** Inside each folder, a `log.txt` file is written, which includes:
    * Timestamp
    * Selected category and the word (revealed)
    * Player's guess history (correct/wrong)
    * Final result (Win/Loss) and points earned for the round
    * Updated overall statistics.