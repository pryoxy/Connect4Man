import tkinter as tk
import time
import tkinter.messagebox as tkmb


from hangman import Hangman
from connect4 import ConnectFour

class Connect4Man:
    def __init__(self, lh: Hangman, rh: Hangman, c: ConnectFour):
        self.lh = lh
        self.c = c
        self.rh = rh

        self.lh.last_button_press_status.trace_add('write', lambda *_: self.handle_lh_guess())
        self.rh.last_button_press_status.trace_add('write', lambda *_: self.handle_rh_guess())
        self.c.checker_var.trace_add('write', lambda *_: self.checker_dropped())

        self.c.locked = True

        self.rh.prompt_for_input('Player 1 enter a word')
        self.lh.prompt_for_input('Player 2 enter a word')

    def handle_lh_guess(self):
        if self.lh.last_button_press_status.get() == 'correct':
            self.lh.alive = False
            self.rh.alive = False
            self.c.locked = False
            if self.c.current_player is self.c.Player.RED:
                self.c.switch_player()
            if self.lh.guessed_letters.issuperset(set(self.lh.word)):
                self.lh.prompt_for_input('Player 2 enter a new word')
        else:
            #print incorrect guess mesage and yellow player turn
            self.lh.alive = False
            self.rh.alive = True
            
            

        
    def handle_rh_guess(self):
        if self.rh.last_button_press_status.get() == 'correct':
            self.lh.alive = False
            self.rh.alive = False
            self.c.locked = False
            if self.c.current_player is self.c.Player.YELLOW:
                self.c.switch_player()
            if self.rh.guessed_letters.issuperset(set(self.rh.word)):
                self.rh.prompt_for_input('Player 1 enter a new word')                
        else:
            #print incorrect guess mesage and red player turn
            self.rh.alive = False
            self.lh.alive = True

    def checker_dropped(self):
        if self.c.check_wins():
            #message box you win self.current_player.name
            ...
        self.c.locked = True
    
    # def player_state_change(self, lh: Hangman, rh: Hangman, c: ConnectFour):
    #     if(self.lh.a)

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