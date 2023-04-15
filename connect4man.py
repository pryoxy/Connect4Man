import time
import tkinter as tk
import tkinter.messagebox as tkmb

from connect4 import ConnectFour
from hangman import Hangman


class Connect4Man:
    def __init__(self, lh: Hangman, rh: Hangman, c: ConnectFour):
        self.lh = lh
        self.c = c
        self.rh = rh

        self.lh.last_button_press_status.trace_add(
            'write', lambda *_: self.handle_lh_guess()
        )
        self.rh.last_button_press_status.trace_add(
            'write', lambda *_: self.handle_rh_guess()
        )

        self.c.checker_var.trace_add('write', lambda *_: self.checker_dropped())

        self.c.locked = True

        self.rh.prompt_for_input('Player 1 enter a word')
        self.lh.prompt_for_input('Player 2 enter a word')

        self.lh.lost.trace_add('write', lambda *_: self.end_game(lh, 'Yellow'))
        self.rh.lost.trace_add('write', lambda *_: self.end_game(rh, 'Red'))

        self.running = True

    def handle_lh_guess(self):
        if self.lh.last_button_press_status.get() == 'correct':
            self.lh.alive = False
            self.rh.alive = False
            self.c.locked = False
            if self.c.current_player is self.c.Player.RED:
                self.c.switch_player()
            if self.lh.guessed_letters.issuperset(set(self.lh.word)):
                self.lh.reset('Player 2 enter new word')
        else:
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
                self.rh.reset('Player 1 enter new word')
        else:
            self.rh.alive = False
            self.lh.alive = True

    def checker_dropped(self):
        if self.c.check_wins(*self.c.last_pos):
            tkmb.showinfo(
                title='Connect4Man',
                message=f'{self.c.current_player.name.title()} wins!',
            )
            self.running = False
        self.c.unhighlight_columns()
        self.c.locked = True
        if self.c.current_player is self.c.Player.RED:
            self.lh.alive = True
        else:
            self.rh.alive = True

    def end_game(self, hm, p):
        if hm.lives_remaining:
            return
        tkmb.showinfo(title='Connect4Man', message=f'{p.title()} lost!')
        self.running = False

    def mainloop(self, root):
        while self.running:
            try:
                root.update_idletasks()
                root.update()
                time.sleep(0.01)
            except tk.TclError:
                return


def main():
    root = tk.Tk()
    root.title('Connect4Man')
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

    c4m = Connect4Man(left_hangman, right_hangman, connect_4)
    c4m.mainloop(root)


if __name__ == '__main__':
    main()
