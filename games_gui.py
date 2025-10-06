import tkinter as tk
from tkinter import messagebox
import random
# NOTE: We'll put your existing game logic into this file later, but we need to
# refactor them to use GUI elements instead of 'print' and 'input'.
import json
import os

def load_hangman_words(filename="hangman_words.json"):
    """Loads a list of words from a JSON file using the script's absolute path."""
    
    # Use the same logic to find the absolute path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, filename)
    
    if not os.path.exists(full_path):
        print(f"Error: Hangman data file not found at {full_path}")
        return ["error"] # Return a default list so the game doesn't crash
    
    try:
        with open(full_path, 'r') as f:
            data = json.load(f)
            # Ensure the loaded data is a list of strings
            if isinstance(data, list) and all(isinstance(item, str) for item in data):
                return [word.lower() for word in data]
            else:
                print(f"Error: Hangman data file is not a list of strings: {full_path}")
                return ["error"]
    except Exception as e:
        print(f"An error occurred while reading the Hangman file: {e}")
        return ["error"]

def load_quiz_questions(filename="quiz_data.json"):
    """Loads quiz questions from a JSON file using the script's absolute path."""

    # 1. Get the directory of the currently executing script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Combine the script directory and the filename to create the full path
    full_path = os.path.join(script_dir, filename)

    if not os.path.exists(full_path):
        print(f"Error: Quiz data file not found at {full_path}")
        return []
    
    try:
        with open(full_path, 'r') as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {filename}. Check the file format.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return []

# --- Global Class to Manage the Application ---
class GameApp(tk.Tk):
    """The main application window."""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Python Text-based Games Collection")
        self.geometry("600x450")

        # Container Frame: All other frames (pages) will be stacked on top of this.
        container = tk.Frame(self, bg="#90EE90") 
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # Add all pages/frames to the dictionary
        for F in (MainMenu, NumberGuessingGUI, WordGuessingGUI, RockPaperScissorsGUI, HigherOrLowerGUI, DiceRollingGUI, QuizGameGUI, TicTacToeGUI):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # Put all frames in the same location (stacking them)
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        """Raises the desired frame to the front."""
        frame = self.frames[page_name]
        frame.tkraise()

# --- Main Menu Screen ---
class MainMenu(tk.Frame):
    """The starting screen with buttons for all games."""
    def __init__(self, parent, controller):
        bg="#90EE90"
        tk.Frame.__init__(self, parent, bg=bg) 
        self.controller = controller

        tk.Label(self, text="=== Python Text-based Games Collection ===", font=('Arial', 16, 'bold'), bg=bg).pack(pady=20)
        
        # List of all games to create buttons dynamically
        games = [
            ("1. Number Guessing Game", "NumberGuessingGUI"),
            ("2. Word Guessing (Hangman)", "WordGuessingGUI"),
            ("3. Rock-Paper-Scissors", "RockPaperScissorsGUI"),
            ("4. Higher or Lower (1-100)", "HigherOrLowerGUI"),
            ("5. Dice Rolling (Betting)", "DiceRollingGUI"),
            ("6. Quiz Game", "QuizGameGUI"),
            ("7. Tic-Tac-Toe (2-Player)", "TicTacToeGUI"),
        ]

        for text, frame_name in games:
            if frame_name:
                tk.Button(self, text=text, width=50, command=lambda name=frame_name: controller.show_frame(name)).pack(pady=5)
            else:
                tk.Button(self, text=text, width=50, state=tk.DISABLED, command=lambda: messagebox.showinfo("WIP", "Game not yet implemented!")).pack(pady=5)

        tk.Button(self, text="Exit", width=30, command=controller.quit).pack(pady=20)

# --- Number Guessing Game GUI Frame ---
class NumberGuessingGUI(tk.Frame):
    def __init__(self, parent, controller):
        bg="#90EE90"
        tk.Frame.__init__(self, parent, bg=bg)
        self.controller = controller
        
        self.max_attempts = 10
        self.target_number = 0
        self.attempts_left = 0

        # --- Widgets Setup ---
        tk.Label(self, text="=== Number Guessing Game ===", font=('Arial', 14, 'bold'), bg=bg).pack(pady=10)
        
        # A Text widget to act as the Game Log
        self.log_text = tk.Text(self, height=8, width=60, state=tk.DISABLED)
        self.log_text.pack(pady=10)

        # Frame for Input and Button
        input_frame = tk.Frame(self, bg=bg)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Your Guess (1-10):", bg=bg).pack(side=tk.LEFT, padx=5)
        
        # Entry widget for the player's guess
        self.guess_entry = tk.Entry(input_frame, width=10)
        self.guess_entry.pack(side=tk.LEFT, padx=5)
        
        # Button to submit the guess
        self.guess_button = tk.Button(input_frame, text="Guess!", command=self.check_guess)
        self.guess_button.pack(side=tk.LEFT, padx=5)

        # Label to show status (Attempts left)
        self.status_label = tk.Label(self, text="", bg=bg)
        self.status_label.pack(pady=10)

        # Button to start a new game
        tk.Button(self, text="New Game", command=self.start_game).pack(pady=5)
        
        # Button to return to the main menu
        tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame("MainMenu")).pack(pady=5)

        # Start the first game automatically
        self.start_game()
        
    def log(self, message):
        """Helper function to update the Text widget (Game Log)"""
        self.log_text.config(state=tk.NORMAL) # Enable editing
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END) # Auto-scroll to the bottom
        self.log_text.config(state=tk.DISABLED) # Disable editing

    def start_game(self):
        """Initializes the game state."""
        self.target_number = random.randint(1, 10)
        self.attempts_left = self.max_attempts
        
        # Clear the log and reset status
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        self.status_label.config(text=f"Attempts left: {self.attempts_left}")
        self.log("New game started! Guess the number between 1 and 10!")
        
        self.guess_button.config(state=tk.NORMAL)
        self.guess_entry.config(state=tk.NORMAL)
        self.guess_entry.delete(0, tk.END)

    def check_guess(self):
        """Handles the logic when the 'Guess!' button is pressed."""
        guess_str = self.guess_entry.get()
        self.guess_entry.delete(0, tk.END) # Clear the input box

        try:
            guess = int(guess_str)
            if not (1 <= guess <= 10):
                self.log("⚠️ Please enter a number between 1 and 10!")
                return
            
            self.attempts_left -= 1
            
            if guess == self.target_number:
                self.log(f"🎉 Congrats! You guessed the correct number: {self.target_number}!")
                self.end_game(True)
            else:
                hint = "Lower!" if guess > self.target_number else "Higher!"
                self.log(f"❌ Wrong guess! It's {hint}")
                
                if self.attempts_left <= 0:
                    self.log(f"Game Over! The number was {self.target_number}.")
                    self.end_game(False)
                else:
                    self.status_label.config(text=f"Attempts left: {self.attempts_left}")

        except ValueError:
            self.log("⚠️ Please enter a valid number!")

    def end_game(self, won):
        """Disables input and updates status at the end of a round."""
        self.guess_button.config(state=tk.DISABLED)
        self.guess_entry.config(state=tk.DISABLED)
        self.status_label.config(text="Game Ended. Start a New Game.")


# --- Word Guessing Game GUI Frame (Hangman) ---
class WordGuessingGUI(tk.Frame):
    def __init__(self, parent, controller):
        # Set the frame background color
        tk.Frame.__init__(self, parent, bg="#90EE90")
        self.controller = controller
        
        # Game State Variables
        self.secret_word = ""
        self.guessed_letters = []
        self.attempts = 0
        self.letter_buttons = {} # Dictionary to hold the A-Z buttons

        # --- Widgets Setup ---
        tk.Label(self, text="=== Word Guessing (Hangman) ===", font=('Arial', 14, 'bold'), bg="#90EE90").pack(pady=10)
        
        # Label to display the masked word (e.g., P _ T H O N)
        self.word_display = tk.Label(self, text="", font=('Courier', 24, 'bold'), bg="#90EE90")
        self.word_display.pack(pady=10)
        
        # Label to display attempts left
        self.status_label = tk.Label(self, text="Attempts left: 6", bg="#90EE90")
        self.status_label.pack(pady=5)
        
        # Frame for the Letter Buttons
        self.letter_frame = tk.Frame(self, bg="#90EE90")
        self.letter_frame.pack(pady=20)
        
        self.create_letter_buttons()

        # Control Buttons
        tk.Button(self, text="New Game", command=self.start_game).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self, text="Back to Menu", command=self.back_to_menu).pack(side=tk.RIGHT, padx=10, pady=10)

        # Start the first game
        self.start_game()

    def create_letter_buttons(self):
        """Creates 26 buttons for A-Z in the letter_frame."""
        for i in range(26):
            letter = chr(ord('a') + i) # 'a', 'b', 'c', ...
            # Create the button, passing the letter to the check_letter method
            button = tk.Button(
                self.letter_frame, 
                text=letter.upper(), 
                width=2, 
                command=lambda l=letter: self.check_letter(l)
            )
            # Layout the buttons in rows of 9
            row = i // 9
            col = i % 9
            button.grid(row=row, column=col, padx=2, pady=2)
            self.letter_buttons[letter] = button

    def start_game(self):
        """Resets the game state and UI for a new round."""
        
        # === MODIFICATION IS HERE ===
        words = load_hangman_words() # Use the new function to load words
        if words == ["error"]:
            self.secret_word = "error"
            self.status_label.config(text="FATAL ERROR: Could not load word list.", fg="red")
            self.disable_all_letters()
            return

        self.secret_word = random.choice(words).lower()
        # ============================
        
        self.guessed_letters = []
        self.attempts = 6
        
        # Reset all letter buttons to be enabled
        for letter, button in self.letter_buttons.items():
            button.config(state=tk.NORMAL)
        
        self.update_display()
        self.status_label.config(text=f"Attempts left: {self.attempts}", fg="black")

    def get_masked_word(self):
        """Generates the string with underscores for unguessed letters."""
        display_word = ""
        for letter in self.secret_word:
            if letter in self.guessed_letters:
                display_word += letter + " "
            else:
                display_word += "_ "
        return display_word.strip()

    def update_display(self):
        """Updates the word display and checks for win/loss conditions."""
        masked_word = self.get_masked_word()
        self.word_display.config(text=masked_word)

        if "_" not in masked_word:
            self.status_label.config(text="🎉 CONGRATULATIONS! You guessed the word!")
            self.disable_all_letters()
        elif self.attempts <= 0:
            self.status_label.config(text=f"❌ GAME OVER! The word was: {self.secret_word}")
            self.disable_all_letters()
        else:
            self.status_label.config(text=f"Attempts left: {self.attempts}")

    def check_letter(self, guess):
        """Handles the logic when a letter button is pressed."""
        
        # Disable the button immediately
        self.letter_buttons[guess].config(state=tk.DISABLED)
        
        if guess not in self.guessed_letters:
            self.guessed_letters.append(guess)

            if guess not in self.secret_word:
                self.attempts -= 1
                
        self.update_display()
        
    def disable_all_letters(self):
        """Disables all letter buttons at the end of the game."""
        for letter, button in self.letter_buttons.items():
            button.config(state=tk.DISABLED)
            
    def back_to_menu(self):
        """Resets the game and returns to the main menu."""
        self.disable_all_letters()
        self.controller.show_frame("MainMenu")

# --- Rock-Paper-Scissors GUI Frame ---
class RockPaperScissorsGUI(tk.Frame):
    def __init__(self, parent, controller):
        # Set the frame background color
        tk.Frame.__init__(self, parent, bg="#90EE90")
        self.controller = controller
        
        # Game State Variables
        self.choices = ["rock", "paper", "scissors"]
        self.player_score = 0
        self.computer_score = 0

        # --- Widgets Setup ---
        tk.Label(self, text="=== Rock-Paper-Scissors ===", font=('Arial', 16, 'bold'), bg="#90EE90").pack(pady=10)
        
        # Label for displaying the current score
        self.score_label = tk.Label(self, text="First to 3 wins!\nScore: You 0 - 0 Computer", bg="#90EE90", font=('Arial', 12))
        self.score_label.pack(pady=10)

        # Label for displaying round results and status messages
        self.result_label = tk.Label(self, text="Choose your weapon!", bg="#90EE90", font=('Arial', 12, 'italic'))
        self.result_label.pack(pady=10)

        # Frame for the Choice Buttons
        button_frame = tk.Frame(self, bg="#90EE90")
        button_frame.pack(pady=20)
        
        # Create a button for each choice, mapping the choice to the play_round method
        self.rock_button = tk.Button(button_frame, text="✊ ROCK", width=10, command=lambda: self.play_round("rock"))
        self.rock_button.pack(side=tk.LEFT, padx=10)

        self.paper_button = tk.Button(button_frame, text="✋ PAPER", width=10, command=lambda: self.play_round("paper"))
        self.paper_button.pack(side=tk.LEFT, padx=10)

        self.scissors_button = tk.Button(button_frame, text="✌️ SCISSORS", width=10, command=lambda: self.play_round("scissors"))
        self.scissors_button.pack(side=tk.LEFT, padx=10)
        
        # Control Buttons
        self.new_game_button = tk.Button(self, text="New Game", command=self.reset_game)
        self.new_game_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame("MainMenu")).pack(side=tk.RIGHT, padx=10, pady=10)

    def update_score_display(self):
        """Updates the Label with the current scores."""
        self.score_label.config(text=f"First to 3 wins!\nScore: You {self.player_score} - {self.computer_score} Computer")

    def toggle_buttons(self, state):
        """Enables or disables the choice buttons."""
        self.rock_button.config(state=state)
        self.paper_button.config(state=state)
        self.scissors_button.config(state=state)

    def play_round(self, player_choice):
        """Contains the core Rock-Paper-Scissors logic."""
        computer_choice = random.choice(self.choices)
        round_result = ""
        
        self.result_label.config(text=f"You chose: {player_choice.upper()} | Computer chose: {computer_choice.upper()}")

        if player_choice == computer_choice:
            round_result = "🤝 It's a tie!"
        elif (
            (player_choice == "rock" and computer_choice == "scissors") or
            (player_choice == "paper" and computer_choice == "rock") or
            (player_choice == "scissors" and computer_choice == "paper")
        ):
            round_result += "🎉 You win this round!"
            self.player_score += 1
        else:
            round_result += "❌ Computer wins this round!"
            self.computer_score += 1

        # Update the result label to show the outcome
        self.result_label.config(text=self.result_label.cget("text") + "\n" + round_result)
        
        self.update_score_display()

        # Check for game end condition (first to 3)
        if self.player_score >= 3:
            self.result_label.config(text="🏆 You won the game! Click 'New Game' to restart.")
            self.toggle_buttons(tk.DISABLED)
        elif self.computer_score >= 3:
            self.result_label.config(text="💻 Computer won the game! Click 'New Game' to restart.")
            self.toggle_buttons(tk.DISABLED)

    def reset_game(self):
        """Resets the scores and allows a new game to begin."""
        self.player_score = 0
        self.computer_score = 0
        self.update_score_display()
        self.result_label.config(text="Choose your weapon!")
        self.toggle_buttons(tk.NORMAL)

# --- Higher or Lower GUI Frame ---
class HigherOrLowerGUI(tk.Frame):
    def __init__(self, parent, controller):
        # Set the frame background color
        tk.Frame.__init__(self, parent, bg="#90EE90")
        self.controller = controller
        
        # Game State Variables
        self.target_number = 0
        self.attempts = 0

        # --- Widgets Setup ---
        tk.Label(self, text="=== Higher or Lower (1-100) ===", font=('Arial', 16, 'bold'), bg="#90EE90").pack(pady=10)
        
        # A Text widget to act as the Game Log
        self.log_text = tk.Text(self, height=8, width=60, state=tk.DISABLED)
        self.log_text.pack(pady=10)

        # Label to show the status (Attempt count)
        self.status_label = tk.Label(self, text="Attempts: 0", bg="#90EE90", font=('Arial', 12))
        self.status_label.pack(pady=5)

        # Frame for Input and Button
        input_frame = tk.Frame(self, bg="#90EE90")
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Your Guess (1-100):", bg="#90EE90").pack(side=tk.LEFT, padx=5)
        
        # Entry widget for the player's guess
        self.guess_entry = tk.Entry(input_frame, width=10)
        self.guess_entry.pack(side=tk.LEFT, padx=5)
        
        # Button to submit the guess
        self.guess_button = tk.Button(input_frame, text="Guess!", command=self.check_guess)
        self.guess_button.pack(side=tk.LEFT, padx=5)

        # Control Buttons
        tk.Button(self, text="New Game", command=self.start_game).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame("MainMenu")).pack(side=tk.RIGHT, padx=10, pady=10)

        # Start the first game automatically
        self.start_game()
        
    def log(self, message):
        """Helper function to update the Text widget (Game Log)"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def start_game(self):
        """Initializes the game state."""
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        
        # Clear the log and reset status
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        self.status_label.config(text="Attempts: 0")
        self.log("New game started! Guess the number between 1 and 100!")
        
        self.guess_button.config(state=tk.NORMAL)
        self.guess_entry.config(state=tk.NORMAL)
        self.guess_entry.delete(0, tk.END)

    def check_guess(self):
        """Handles the logic when the 'Guess!' button is pressed."""
        guess_str = self.guess_entry.get()
        self.guess_entry.delete(0, tk.END) # Clear the input box

        try:
            guess = int(guess_str)
            if not (1 <= guess <= 100):
                self.log("⚠️ Please enter a number between 1 and 100!")
                return
            
            self.attempts += 1
            self.status_label.config(text=f"Attempts: {self.attempts}")
            
            if guess == self.target_number:
                self.log(f"🎉 Correct! You guessed it ({self.target_number}) in {self.attempts} attempts!")
                self.end_game()
            elif guess < self.target_number:
                self.log(f"Your guess: {guess}. ⬆️ Higher!")
            else:
                self.log(f"Your guess: {guess}. ⬇️ Lower!")

        except ValueError:
            self.log("⚠️ Please enter a valid number!")

    def end_game(self):
        """Disables input and updates status at the end of a round."""
        self.guess_button.config(state=tk.DISABLED)
        self.guess_entry.config(state=tk.DISABLED)

# --- Dice Rolling Game GUI Frame (Betting) ---
class DiceRollingGUI(tk.Frame):
    def __init__(self, parent, controller):
        # Set the frame background color
        tk.Frame.__init__(self, parent, bg="#90EE90")
        self.controller = controller
        
        # Game State Variables
        self.money = 100
        self.bet_choice = tk.StringVar(value="h") # Tkinter variable for Radiobuttons (default to High)

        # --- Widgets Setup ---
        tk.Label(self, text="=== Dice Rolling Game ===", font=('Arial', 16, 'bold'), bg="#90EE90").pack(pady=10)
        
        # Label for displaying current money
        self.money_label = tk.Label(self, text=f"💰 Current Money: ${self.money}", bg="#90EE90", font=('Arial', 14, 'bold'))
        self.money_label.pack(pady=10)

        # A Text widget to act as the Game Log (dice rolls and results)
        self.log_text = tk.Text(self, height=8, width=60, state=tk.DISABLED)
        self.log_text.pack(pady=10)

        # Frame for Betting Input
        input_frame = tk.Frame(self, bg="#90EE90")
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Bet Amount:", bg="#90EE90").pack(side=tk.LEFT, padx=5)
        
        # Entry widget for the bet amount
        self.bet_entry = tk.Entry(input_frame, width=10)
        self.bet_entry.pack(side=tk.LEFT, padx=10)

        # Radiobuttons for Choice (High or Low)
        tk.Radiobutton(input_frame, text="High (4-6)", variable=self.bet_choice, value="h", bg="#90EE90").pack(side=tk.LEFT)
        tk.Radiobutton(input_frame, text="Low (1-3)", variable=self.bet_choice, value="l", bg="#90EE90").pack(side=tk.LEFT)
        
        # Button to place the bet
        self.place_bet_button = tk.Button(self, text="Place Bet!", command=self.place_bet)
        self.place_bet_button.pack(pady=10)

        # Control Buttons
        tk.Button(self, text="New Game (Reset Money)", command=self.reset_game).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame("MainMenu")).pack(side=tk.RIGHT, padx=10, pady=10)

        self.log("Welcome! Bet on High (4-6) or Low (1-3)!")

    def log(self, message):
        """Helper function to update the Text widget (Game Log)"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def update_money_display(self):
        """Updates the money label."""
        self.money_label.config(text=f"💰 Current Money: ${self.money}")

    def place_bet(self):
        """Handles the dice roll and betting logic."""
        bet_str = self.bet_entry.get()
        self.bet_entry.delete(0, tk.END) # Clear the input box

        try:
            bet = int(bet_str)
            
            # Validation checks
            if bet <= 0:
                self.log("⚠️ Bet must be a positive number!")
                return
            if bet > self.money:
                self.log(f"⚠️ You only have ${self.money}! Bet less than that.")
                return
            
            choice = self.bet_choice.get() # 'h' or 'l'
            dice = random.randint(1, 6)
            
            self.log(f"\n--- Round ---")
            self.log(f"Bet: ${bet} on {'HIGH' if choice == 'h' else 'LOW'}")
            self.log(f"🎲 Dice rolled: {dice}")

            # Check win condition
            is_win = (choice == "h" and dice >= 4) or (choice == "l" and dice <= 3)

            if is_win:
                self.money += bet
                self.log(f"✅ YOU WIN! You gained ${bet}.")
            else:
                self.money -= bet
                self.log(f"❌ You lose ${bet}.")
            
            self.update_money_display()

            # Check for Game Over
            if self.money <= 0:
                self.log("\n💸 GAME OVER! You're out of money. Start a New Game.")
                self.place_bet_button.config(state=tk.DISABLED)
                self.bet_entry.config(state=tk.DISABLED)

        except ValueError:
            self.log("⚠️ Please enter a valid numerical bet!")

    def reset_game(self):
        """Resets money to 100 for a new game."""
        self.money = 100
        self.update_money_display()
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        self.log("New game started. Bet wisely!")
        self.place_bet_button.config(state=tk.NORMAL)
        self.bet_entry.config(state=tk.NORMAL)

# --- Quiz Game GUI Frame ---
class QuizGameGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#90EE90")
        self.controller = controller
        
        # Game State Variables
        self.questions = []
        self.current_question_index = 0
        self.score = 0

        # --- Widgets Setup ---
        tk.Label(self, text="=== Quiz Game ===", font=('Arial', 16, 'bold'), bg="#90EE90").pack(pady=10)
        
        # Label to display the current score
        self.score_label = tk.Label(self, text="Score: 0/0", bg="#90EE90", font=('Arial', 12))
        self.score_label.pack(pady=5)

        # Label for the question text
        self.question_label = tk.Label(self, text="", wraplength=500, justify=tk.LEFT, bg="#90EE90", font=('Arial', 14))
        self.question_label.pack(pady=20, padx=10)

        # Frame for Answer Input
        input_frame = tk.Frame(self, bg="#90EE90")
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Your Answer:", bg="#90EE90").pack(side=tk.LEFT, padx=5)
        
        self.answer_entry = tk.Entry(input_frame, width=30)
        self.answer_entry.pack(side=tk.LEFT, padx=5)
        
        self.submit_button = tk.Button(input_frame, text="Submit", command=self.submit_answer)
        self.submit_button.pack(side=tk.LEFT, padx=5)
        
        # Label for feedback (Correct/Wrong)
        self.feedback_label = tk.Label(self, text="", bg="#90EE90", font=('Arial', 12, 'italic'))
        self.feedback_label.pack(pady=10)

        # Control Buttons
        tk.Button(self, text="New Game", command=self.start_game).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame("MainMenu")).pack(side=tk.RIGHT, padx=10, pady=10)

        self.start_game()
        
    def start_game(self):
        """Loads questions and resets the game state."""
        self.questions = load_quiz_questions() # Load questions from the JSON file
        self.current_question_index = 0
        self.score = 0
        
        self.submit_button.config(state=tk.NORMAL)
        self.answer_entry.config(state=tk.NORMAL)
        self.feedback_label.config(text="")
        
        if self.questions:
            self.show_next_question()
        else:
            self.question_label.config(text="No questions loaded. Check quiz_data.json.")
            self.submit_button.config(state=tk.DISABLED)

    def show_next_question(self):
        """Displays the next question in the list."""
        if self.current_question_index < len(self.questions):
            q_data = self.questions[self.current_question_index]
            self.question_label.config(text=f"Q{self.current_question_index + 1}: {q_data['question']}")
            self.score_label.config(text=f"Score: {self.score}/{len(self.questions)}")
            self.answer_entry.delete(0, tk.END) # Clear previous answer
            self.feedback_label.config(text="")
        else:
            self.end_game()

    def submit_answer(self):
        """Checks the player's answer against the correct answer."""
        if self.current_question_index >= len(self.questions):
            return # Should not happen, but a safety check
            
        q_data = self.questions[self.current_question_index]
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = q_data['answer'].strip().lower()
        
        if user_answer == correct_answer:
            self.score += 1
            self.feedback_label.config(text="✅ Correct!", fg="green")
        else:
            self.feedback_label.config(text=f"❌ Wrong! Answer: {correct_answer}", fg="red")
        
        # Move to the next question after a brief delay so the user can see the feedback
        self.current_question_index += 1
        self.after(1000, self.show_next_question)

    def end_game(self):
        """Displays final score."""
        final_score_text = f"📊 Quiz Finished! Your final score is: {self.score}/{len(self.questions)}"
        self.question_label.config(text=final_score_text)
        self.score_label.config(text=f"Final Score: {self.score}/{len(self.questions)}")
        self.submit_button.config(state=tk.DISABLED)
        self.answer_entry.config(state=tk.DISABLED)

# --- Tic-Tac-Toe GUI Frame ---
class TicTacToeGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#90EE90")
        self.controller = controller
        
        # Game State Variables
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.buttons = {}  # Dictionary to hold the 9 button objects
        self.game_active = True

        # --- Widgets Setup ---
        tk.Label(self, text="=== Tic-Tac-Toe (2-Player) ===", font=('Arial', 16, 'bold'), bg="#90EE90").pack(pady=10)
        
        # Label to display current status
        self.status_label = tk.Label(self, text="Player X's turn", bg="#90EE90", font=('Arial', 14))
        self.status_label.pack(pady=10)

        # Frame for the 3x3 Game Board Grid
        grid_frame = tk.Frame(self, bg="#90EE90")
        grid_frame.pack(pady=20)
        
        # Create 9 buttons in a 3x3 grid
        for row in range(3):
            for col in range(3):
                # We use a lambda to pass the row and col arguments to the button_click function
                button = tk.Button(
                    grid_frame, 
                    text=" ", 
                    font=('Arial', 24, 'bold'), 
                    width=4, 
                    height=2,
                    command=lambda r=row, c=col: self.button_click(r, c)
                )
                button.grid(row=row, column=col, padx=2, pady=2)
                self.buttons[(row, col)] = button # Store button reference by (row, col)

        # Control Buttons
        tk.Button(self, text="New Game", command=self.reset_game).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame("MainMenu")).pack(side=tk.RIGHT, padx=10, pady=10)

    def check_winner(self):
        """Checks the 3x3 board for a winner."""
        # Check rows, columns, and diagonals using the board array
        
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
        
        # Check columns
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != ' ':
                return self.board[0][j]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        
        return None

    def button_click(self, row, col):
        """Handles the logic when a grid button is pressed."""
        if not self.game_active or self.board[row][col] != ' ':
            return

        # 1. Update the board state
        self.board[row][col] = self.current_player
        
        # 2. Update the button text and disable it
        button = self.buttons[(row, col)]
        button.config(text=self.current_player, state=tk.DISABLED)
        
        winner = self.check_winner()

        if winner:
            self.status_label.config(text=f"🎉 Player {winner} wins!")
            self.game_active = False
            self.disable_all_buttons()
        
        # Check for a tie
        elif all(self.board[i][j] != ' ' for i in range(3) for j in range(3)):
            self.status_label.config(text="🤝 It's a tie!")
            self.game_active = False

        else:
            # 3. Switch player and update status label
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.config(text=f"Player {self.current_player}'s turn")

    def disable_all_buttons(self):
        """Disables all buttons at the end of the game."""
        for button in self.buttons.values():
            if button['text'] == ' ': # Don't re-disable buttons already played
                button.config(state=tk.DISABLED)
                
    def reset_game(self):
        """Resets the board and game state."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_active = True
        self.status_label.config(text="Player X's turn")
        
        # Reset all button appearances and state
        for button in self.buttons.values():
            button.config(text=" ", state=tk.NORMAL)

# --- Execution ---
if __name__ == "__main__":
    app = GameApp()
    app.mainloop()