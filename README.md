# Python GUI Games Collection 🎮

This is a collection of classic text-based games implemented with a Graphical User Interface (GUI) using Python's built-in **Tkinter** library.

The application uses a multi-frame structure, allowing users to easily switch between games from a central **Main Menu**.

## Features

* **Main Menu:** A central hub to select any of the implemented games.
* **Modular Design:** Each game is contained within its own `tk.Frame` class for clean separation of logic and GUI.
* **External Data Loading:** Games like Word Guessing (Hangman) and the Quiz Game load their data from external JSON files, making them easy to update.

---

## Implemented Games

1.  **Number Guessing Game:** Guess a random number between 1 and 10 within 10 attempts.
2.  **Word Guessing (Hangman):** Guess the secret word by clicking on letter buttons. Limited attempts are given. *(Requires `hangman_words.json`)*
3.  **Rock-Paper-Scissors:** Play against the computer in a best-of-5-rounds format.
4.  **Higher or Lower (1-100):** Guess a secret number between 1 and 100, receiving "Higher" or "Lower" hints.
5.  **Dice Rolling Game (Betting):** Bet your virtual money on whether a 6-sided die roll will be "High" (4-6) or "Low" (1-3).
6.  **Quiz Game:** Answer a series of questions. *(Requires `quiz_data.json`)*
7.  **Tic-Tac-Toe (2-Player):** A simple, two-player version of the classic game.
