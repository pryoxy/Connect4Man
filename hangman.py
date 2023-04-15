import tkinter as tk
import tkinter.ttk as ttk

from dialogues import HangmanWordEntry


class Hangman:
    def __init__(self, parent: tk.Widget) -> None:
        self.parent = parent

        self.LIVES = 6
        self.MAX_WORD_LENGTH = 12

        self.guessed_letters: set[str] = set()
        self.lives_remaining = self.LIVES

        self.word_frame = ttk.Frame(parent)
        self.button_frame = ttk.Frame(parent)
        self.button_mapping: dict[str, ttk.Button] = {}

        self.init_ui()

        self.word = self.prompt_for_input()

    def init_ui(self) -> None:
        s = ttk.Style()
        s.configure('TLabel', font=('Helvetica', 20, 'normal'))
        s.configure('TButton', font=('Helvetica', 16, 'normal'))
        m = s.map('TButton')
        s.map('Correct.TButton', foreground=[(tk.DISABLED, 'green')], **m)
        s.map('Wrong.TButton', foreground=[(tk.DISABLED, 'red')], **m)

        for i in range(self.MAX_WORD_LENGTH):
            l = ttk.Label(
                self.word_frame,
                text='_' if i < len(self.word) else ' ',
                width=2,
                padding=5,
                takefocus=False,
            )
            l.grid(row=0, column=i)

        alphabet = ['ABCDEFGHI', 'JKLMNOPQR', 'STUVWXYZ ']
        for r, sub_alpha in enumerate(alphabet):
            for c, letter in enumerate(sub_alpha):
                b = ttk.Button(
                    self.button_frame,
                    text=letter,
                    width=2,
                    takefocus=False,
                    padding=5,
                    command=lambda l=letter: self.guess_letter(l),  # type: ignore
                )
                b.grid(row=r, column=c)
                self.button_mapping[letter] = b
        self.button_mapping[' '].state([tk.DISABLED])

        self.word_frame.grid(row=0, column=0, padx=5, pady=5)
        self.button_frame.grid(row=1, column=0, padx=5, pady=5)

    def guess_letter(self, letter: str) -> None:
        button_pressed = self.button_mapping[letter]
        self.guessed_letters.add(letter)
        if letter in self.word:
            button_pressed.config(style='Correct.TButton')
        else:
            button_pressed.config(style='Wrong.TButton')
            self.lives_remaining -= 1
        button_pressed.state([tk.DISABLED])
        self.update_word_display()

    def update_word_display(self) -> None:
        for label, letter in zip(reversed(self.word_frame.grid_slaves()), self.word):
            if letter in self.guessed_letters:
                assert isinstance(label, ttk.Label)
                label.configure(text=letter)

    def prompt_for_input(self) -> str:
        word = tk.StringVar()
        HangmanWordEntry(self.parent.winfo_toplevel(), self.MAX_WORD_LENGTH, word)
        return word.get().upper()


def main():
    root = tk.Tk()
    root.title('Hangman')
    root.resizable(False, False)
    main_frame = tk.Frame(root)
    main_frame.grid(row=0, column=0)
    hg = Hangman(main_frame)
    root.mainloop()


if __name__ == '__main__':
    main()
