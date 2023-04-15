import tkinter as tk
import time

from hangman import Hangman
from connect4 import ConnectFour

class Connect4Man:
    def __init__(self, lh: Hangman, rh: Hangman, c: ConnectFour):
        self.lh = lh
        self.c = c
        self.rh = rh

        self.c.locked = True

        lh.prompt_for_input('Player 1 enter a word')
        rh.prompt_for_input('Player 2 enter a word')
    
    def player_state_change(self, lh: Hangman, rh: Hangman, c: ConnectFour):
        if(self.lh.a)

def main():
    root = tk.Tk()
    root.resizable(False, False)
    main_frame = tk.Frame(root)
    left_hm_f = tk.Frame(main_frame)
    c4_f = tk.Frame(main_frame)
    right_hm_f = tk.Frame(main_frame)


    left_hangman = Hangman(left_hm_f)
    connect_4 = ConnectFour(c4_f)
    right_hangman = Hangman(right_hm_f)

    main_frame.grid(row=0, column=0)
    left_hm_f.grid(row=0, column=0)
    c4_f.grid(row=0, column=1)
    right_hm_f.grid(row=0, column=2)

    Connect4Man(left_hangman, right_hangman, connect_4)

    root.mainloop()


if __name__ == '__main__':
    main()