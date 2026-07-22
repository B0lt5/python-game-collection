# Python GUI Games Collection 🎮

A fun collection of classic games built with Python and Tkinter. This project provides a simple desktop interface where you can switch between different games from a central menu.

## Download and Run

If you are using the Windows release build:

1. Download the executable from the GitHub Releases page.
2. Run the `.exe` file to launch the game collection.

If you are running the source version, open the project folder and run:

```bash
python games_gui.py
```

### Requirements (for the source version)

- Python 3
- Tkinter (included with most Python installations)
- The game data files such as `hangman_words.json` and `quiz_data.json` should be present when running the source version

## Included Games

This collection includes:

1. **Number Guessing Game** – Guess a random number between 1 and 10.
2. **Word Guessing (Hangman)** – Guess the hidden word before you run out of attempts. *(Requires `hangman_words.json`)*
3. **Rock-Paper-Scissors** – Play against the computer.
4. **Higher or Lower (1-100)** – Guess the secret number using higher/lower hints.
5. **Dice Rolling Game** – Bet virtual money on whether the roll will be high or low.
6. **Quiz Game** – Answer a series of questions. *(Requires `quiz_data.json`)*
7. **Tic-Tac-Toe** – Play against another player or the computer.
8. **Bulls and Cows** – Crack the secret 4-digit number using clue-based guesses.
9. **Word Scramble** – Unscramble the given word before time runs out.
10. **Battleship** – Play a naval strategy game against the computer or another player.
11. **Slot Machine** – Spin the reels, place a bet, and aim for a win.
12. **Escape Room** – Explore a room, solve puzzles, and try to escape.

## Notes

- The app uses a multi-frame menu system, so switching between games is quick and simple.
- The project is designed to be easy to expand with more games in the future.
