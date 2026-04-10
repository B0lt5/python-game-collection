import tkinter as tk

# Text Adventure Game Code - for reference
class TextAdventureGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#E6F3FF")
        self.controller = controller
        
        # Game State Variables
        self.current_scene = "start"
        self.visited_scenes = set()
        self.inventory = []
        self.puzzle_solved = False
        
        # Define all scenes and choices
        self.scenes = {
            "start": {
                "title": "You Wake Up...",
                "description": "You wake up in a locked room. The walls are gray concrete. There's a metal door ahead, "
                               "a wooden bookshelf to your left, and a rug on the floor to your right. You must find a way out!",
                "choices": [
                    ("1. Inspect the bookshelf", "bookshelf"),
                    ("2. Open the door", "door"),
                    ("3. Look under the rug", "rug"),
                ]
            },
            "bookshelf": {
                "title": "The Bookshelf",
                "description": "You examine the dusty bookshelf. Most books are fake, but one red book feels different. "
                               "You pull it and hear a CLICK! A hidden compartment opens, revealing a rusty KEY.",
                "action": "item_key",
                "choices": [
                    ("1. Go back", "start"),
                ]
            },
            "door": {
                "title": "The Metal Door",
                "description": "The door is locked with a keyhole. It won't budge without a key. "
                               "You notice a faint engraving: 'Only the worthy shall leave.'",
                "choices": [
                    ("1. Go back", "start"),
                ]
            },
            "rug": {
                "title": "Under the Rug",
                "description": "You lift the rug and find a dusty note. It reads: 'The answer is PUZZLE'. "
                               "Could this be a hint?",
                "action": "hint_puzzle",
                "choices": [
                    ("1. Go back", "start"),
                ]
            },
            "key": {
                "title": "Key Found!",
                "description": "You have obtained the KEY! Now you can try to open that metal door. "
                               "The key feels cold in your hand.",
                "choices": [
                    ("1. Go back to the start", "start_with_key"),
                ]
            },
            "start_with_key": {
                "title": "Back at the Start - With Key",
                "description": "Now that you have the key, the door calls to you. The bookshelf and rug are behind you. "
                               "Do you have what it takes to escape?",
                "choices": [
                    ("1. Inspect the bookshelf again", "bookshelf_again"),
                    ("2. Try the key on the door!", "escape_attempt"),
                    ("3. Look under the rug again", "rug_again"),
                ]
            },
            "bookshelf_again": {
                "title": "The Bookshelf (Again)",
                "description": "You already found the key here. Nothing else seems important now.",
                "choices": [
                    ("1. Go back", "start_with_key"),
                ]
            },
            "rug_again": {
                "title": "Under the Rug (Again)",
                "description": "The note is still there: 'The answer is PUZZLE'. Wait... could this be the puzzle?",
                "choices": [
                    ("1. Go back", "start_with_key"),
                ]
            },
            "escape_attempt": {
                "title": "🎉 FREEDOM!",
                "description": "You insert the key into the keyhole and turn it. The door swings open! "
                               "Sunlight floods in. You've escaped the room! Congratulations!",
                "choices": [
                    ("1. Play Again", "start_new_game"),
                ]
            },
            "start_new_game": {
                "title": "New Game",
                "description": "Starting a fresh escape room adventure...",
                "action": "reset_game",
                "choices": [
                    ("1. Begin", "start"),
                ]
            }
        }
        
        # --- Widgets Setup ---
        tk.Label(self, text="=== Mini Text Adventure: Escape Room ===", font=('Arial', 16, 'bold'), 
                bg="#E6F3FF", fg="#003366").pack(pady=10)
        
        # Scene title
        self.title_label = tk.Label(self, text="", font=('Arial', 14, 'bold'), 
                                   bg="#E6F3FF", fg="#003366", wraplength=500)
        self.title_label.pack(pady=10)
        
        # Scene description
        self.description_text = tk.Text(self, height=10, width=70, state=tk.DISABLED, 
                                        bg="white", fg="#333333", font=('Arial', 11), wraplength=600)
        self.description_text.pack(pady=15, padx=20, fill=tk.BOTH, expand=True)
        
        # Inventory display
        self.inventory_label = tk.Label(self, text="Inventory: Empty", font=('Arial', 10), 
                                       bg="#E6F3FF", fg="#003366")
        self.inventory_label.pack(pady=5)
        
        # Choices frame
        self.choices_frame = tk.Frame(self, bg="#E6F3FF")
        self.choices_frame.pack(pady=15, fill=tk.BOTH, expand=True)
        
        # Control Buttons
        button_frame = tk.Frame(self, bg="#E6F3FF")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Restart Game", command=self.restart_game, 
                 bg="#FF6B6B", fg="white", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Back to Menu", 
                 command=lambda: [self.restart_game(), controller.show_frame("MoreGamesMenu")],
                 bg="#4ECDC4", fg="white", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Start the game
        self.show_scene("start")
    
    def show_scene(self, scene_key):
        """Display a scene and its choices."""
        if scene_key not in self.scenes:
            scene_key = "start"
        
        self.current_scene = scene_key
        scene = self.scenes[scene_key]
        self.visited_scenes.add(scene_key)
        
        # Handle special actions
        if "action" in scene:
            action = scene["action"]
            if action == "item_key":
                if "key" not in self.inventory:
                    self.inventory.append("KEY")
            elif action == "hint_puzzle":
                if "puzzle_hint" not in self.inventory:
                    self.inventory.append("PUZZLE HINT")
            elif action == "reset_game":
                self.inventory = []
        
        # Update title
        self.title_label.config(text=scene["title"])
        
        # Update description
        self.description_text.config(state=tk.NORMAL)
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(tk.END, scene["description"])
        self.description_text.config(state=tk.DISABLED)
        
        # Update inventory display
        if self.inventory:
            inv_text = "Inventory: " + ", ".join(self.inventory)
        else:
            inv_text = "Inventory: Empty"
        self.inventory_label.config(text=inv_text)
        
        # Clear previous choices
        for widget in self.choices_frame.winfo_children():
            widget.destroy()
        
        # Display choice buttons
        for choice_text, next_scene in scene["choices"]:
            btn = tk.Button(self.choices_frame, text=choice_text, width=50, 
                           command=lambda scene=next_scene: self.show_scene(scene),
                           bg="#95E1D3", fg="#333333", font=('Arial', 11),
                           relief=tk.RAISED, bd=2)
            btn.pack(pady=5)
    
    def restart_game(self):
        """Reset the game to the start."""
        self.current_scene = "start"
        self.visited_scenes = set()
        self.inventory = []
        self.puzzle_solved = False
        self.show_scene("start")
