import tkinter as tk

from hangman import Hangman
from connect4 import ConnectFour

class Connect4Man:
    ...


def main():
    root = tk.Tk()
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

    root.mainloop()


if __name__ == '__main__':
    main()