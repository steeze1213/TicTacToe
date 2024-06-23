import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.buttons = []
        self.game_mode = None

        self.mode_label = tk.Label(self.root, text="", font='Arial 20 bold')
        self.mode_label.grid(row=0, column=0, columnspan=3)
        
        self.choose_game_mode()
        self.create_board()

    def choose_game_mode(self):
        self.game_mode = simpledialog.askstring("게임 모드", "게임 모드를 선택하시오: 플레이어 vs 플레이어 (PVP) or 플레이어 vs AI (AI)").upper()
        if self.game_mode not in ["PVP", "AI"]:
            messagebox.showerror("올바르지지 않은 모드", "올바른 게임 모드를 선택하십시오.")
            self.choose_game_mode()
        else:
            self.mode_label.config(text=f"모드: {self.game_mode}")

    def create_board(self):
        for i in range(9):
            button = tk.Button(self.root, text=' ', font='Arial 20', width=5, height=2,
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=(i//3)+1, column=i%3)
            self.buttons.append(button)

    def on_button_click(self, index):
        if self.board[index] == ' ':
            self.board[index] = self.current_player
            if self.current_player == 'X':
                self.buttons[index].config(text=self.current_player, fg='red')
            else:
                self.buttons[index].config(text=self.current_player, fg='blue')
            
            if self.check_winner():
                messagebox.showinfo("게임 오버", f"플레이어 {self.current_player}가 이겼습니다!")
                self.end_game()
            elif ' ' not in self.board:
                messagebox.showinfo("게임 오버", "무승부 입니다!")
                self.end_game()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == 'O' and self.game_mode == 'AI':
                    self.ai_move()

    def check_winner(self):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        for a, b, c in win_conditions:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != ' ':
                return True
        return False

    def reset_board(self):
        self.board = [' ' for _ in range(9)]
        for button in self.buttons:
            button.config(text=' ')
        self.current_player = 'X'

    def end_game(self):
        play_again = messagebox.askyesno("게임 오버", "다시 플레이하시겠습니까?")
        if play_again:
            self.choose_game_mode()
            self.reset_board()
        else:
            self.root.quit()

    def ai_move(self):
        #Check and Block
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'X'
                if self.check_winner():
                    self.board[i] = 'O'
                    self.buttons[i].config(text='O', fg='blue')
                    self.board[i] = 'O'
                    self.current_player = 'X'
                    if self.check_winner():
                        messagebox.showinfo("게임 오버", f"플레이어 {self.current_player}가 이겼습니다!")
                        self.end_game()
                    return
                self.board[i] = ' '

        #Random Empty Spot
        empty_indices = [i for i, x in enumerate(self.board) if x == ' ']
        if empty_indices:
            ai_choice = random.choice(empty_indices)
            self.on_button_click(ai_choice)

root = tk.Tk()
game = TicTacToe(root)
root.mainloop()
