import tkinter as tk
from tkinter import messagebox
import random

class Morpion:
    def __init__(self, root):
        self.root = root
        self.root.title("Morpion")
        self.root.geometry("350x600")  # Augmenter la hauteur pour accueillir les nouveaux boutons
        self.current_player = "X"
        self.board = [[None, None, None] for _ in range(3)]
        
        self.x_score = 0
        self.o_score = 0
        self.bot_mode = False
        self.difficulty_level = 3  # Niveau par défaut (facile)

        self.score_frame = tk.Frame(self.root, bg="#282828", bd=5, relief="solid", padx=10, pady=5)
        self.score_frame.grid(row=0, column=0, columnspan=3, pady=10)
        
        self.x_score_label = tk.Label(self.score_frame, text=f"X: {self.x_score}", font=("Arial", 18, "bold"), fg="blue", bg="#282828")
        self.x_score_label.grid(row=0, column=0)

        self.o_score_label = tk.Label(self.score_frame, text=f"O: {self.o_score}", font=("Arial", 18, "bold"), fg="red", bg="#282828")
        self.o_score_label.grid(row=0, column=2)
        
        self.turn_label = tk.Label(self.root, text=f"C'est au tour de {self.current_player}", font=("Arial", 14), fg="black", bg="#f0f0f0")
        self.turn_label.grid(row=1, column=0, columnspan=3, pady=10)
        
        self.bot_button = tk.Button(self.root, text="Jouer avec le Bot", font=("Arial", 12), command=self.toggle_bot_mode, bg="#28a745", fg="white")
        self.bot_button.grid(row=2, column=0, columnspan=3, pady=5)

        # Boutons pour sélectionner la difficulté (initialement cachés)
        self.easy_button = tk.Button(self.root, text="Facile", font=("Arial", 12), command=lambda: self.set_difficulty(3), bg="#ffcc00", fg="white")
        self.easy_button.grid(row=3, column=0, pady=5)
        self.easy_button.grid_remove()  # Cacher le bouton au départ
        
        self.medium_button = tk.Button(self.root, text="Moyen", font=("Arial", 12), command=lambda: self.set_difficulty(4), bg="#ff9900", fg="white")
        self.medium_button.grid(row=3, column=1, pady=5)
        self.medium_button.grid_remove()  # Cacher le bouton au départ
        
        self.hard_button = tk.Button(self.root, text="Difficile", font=("Arial", 12), command=lambda: self.set_difficulty(5), bg="#ff5733", fg="white")
        self.hard_button.grid(row=3, column=2, pady=5)
        self.hard_button.grid_remove()  # Cacher le bouton au départ

        self.restart_button = tk.Button(self.root, text="Recommencer", font=("Arial", 14), command=self.reset_score, bg="#007BFF", fg="white")
        self.restart_button.grid(row=7, column=0, columnspan=3, pady=10)  # Modifié pour placer le bouton dans une ligne séparée
        
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, text="", width=10, height=3, font=("Arial", 24, "bold"),
                                   command=lambda row=row, col=col: self.play_move(row, col))
                button.grid(row=row + 4, column=col, padx=5, pady=5)
                self.buttons[row][col] = button

    def set_difficulty(self, level):
        self.difficulty_level = level
        self.reset_game()

    def toggle_bot_mode(self):
        self.bot_mode = not self.bot_mode
        self.bot_button.config(text="Jouer avec un ami" if self.bot_mode else "Jouer avec le Bot")
        
        # Afficher ou masquer les boutons de difficulté selon le mode
        if self.bot_mode:
            self.easy_button.grid()
            self.medium_button.grid()
            self.hard_button.grid()
        else:
            self.easy_button.grid_remove()
            self.medium_button.grid_remove()
            self.hard_button.grid_remove()
        
        self.reset_game()

    def play_move(self, row, col):
        if self.board[row][col] is None:
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, fg="blue" if self.current_player == "X" else "red")
            winner_line = self.check_win()
            if winner_line:
                self.update_score()
                self.flash_winning_line(winner_line)
                messagebox.showinfo("Victoire", f"Le joueur {self.current_player} a gagné !")
                self.reset_game()
            elif self.check_draw():
                messagebox.showinfo("Match nul", "C'est un match nul !")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.turn_label.config(text=f"C'est au tour de {self.current_player}")
                if self.bot_mode and self.current_player == "O":
                    self.root.after(500, self.bot_play)

    def bot_play(self):
        best_score = float("-inf")
        best_move = None
        for r in range(3):
            for c in range(3):
                if self.board[r][c] is None:
                    self.board[r][c] = "O"
                    score = self.minimax(self.board, 0, False, float("-inf"), float("inf"), self.difficulty_level)
                    self.board[r][c] = None
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
        
        row, col = best_move
        self.play_move(row, col)

    def minimax(self, board, depth, is_maximizing, alpha, beta, max_depth):
        winner_line = self.check_win()
        if winner_line:
            if self.current_player == "X":
                return -1  # Si X gagne, O perd
            elif self.current_player == "O":
                return 1  # Si O gagne, O gagne
        if self.check_draw():
            return 0  # Match nul

        if depth >= max_depth:
            return 0  # Fin de la recherche lorsque la profondeur maximale est atteinte

        if is_maximizing:
            best_score = float("-inf")
            for r in range(3):
                for c in range(3):
                    if board[r][c] is None:
                        board[r][c] = "O"
                        score = self.minimax(board, depth + 1, False, alpha, beta, max_depth)
                        board[r][c] = None
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break  # Alpha-Beta Pruning
            return best_score
        else:
            best_score = float("inf")
            for r in range(3):
                for c in range(3):
                    if board[r][c] is None:
                        board[r][c] = "X"
                        score = self.minimax(board, depth + 1, True, alpha, beta, max_depth)
                        board[r][c] = None
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break  # Alpha-Beta Pruning
            return best_score

    def check_win(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] is not None:
                return [(row, 0), (row, 1), (row, 2)]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                return [(0, col), (1, col), (2, col)]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return [(0, 0), (1, 1), (2, 2)]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return [(0, 2), (1, 1), (2, 0)]
        return None

    def flash_winning_line(self, winning_line):
        for _ in range(3):
            for (row, col) in winning_line:
                self.buttons[row][col].config(bg="yellow")
            self.root.after(300)
            self.root.update()
            for (row, col) in winning_line:
                self.buttons[row][col].config(bg="white")
            self.root.after(300)

    def check_draw(self):
        return all(self.board[row][col] is not None for row in range(3) for col in range(3))

    def reset_game(self):
        self.board = [[None, None, None] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="", fg="black", bg="white")
        self.current_player = "X"
        self.turn_label.config(text=f"C'est au tour de {self.current_player}")

    def reset_score(self):
        self.x_score = 0
        self.o_score = 0
        self.x_score_label.config(text=f"X: {self.x_score}")
        self.o_score_label.config(text=f"O: {self.o_score}")
        self.reset_game()

    def update_score(self):
        if self.current_player == "X":
            self.x_score += 1
        else:
            self.o_score += 1
        self.x_score_label.config(text=f"X: {self.x_score}")
        self.o_score_label.config(text=f"O: {self.o_score}")

if __name__ == "__main__":
    root = tk.Tk()
    game = Morpion(root)
    root.mainloop()
