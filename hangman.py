import tkinter as tk
import tkinter.ttk as ttk
import time

from dialogues import HangmanWordEntry


class Hangman:
    def __init__(self, parent: tk.Widget) -> None:
        self.parent = parent

        self.LIVES = 6
        self.MAX_WORD_LENGTH = 12

        self.guessed_letters: set[str] = set()
        self.lives_remaining = self.LIVES
        self.lost = False
        self.alive = False

        self.man_label = ttk.Label(self.parent)
        self.word_frame = ttk.Frame(self.parent)
        self.button_frame = ttk.Frame(self.parent)
        self.button_mapping: dict[str, ttk.Button] = {}
        self.images = [
            tk.PhotoImage(file=f)
            for f in (
                'Hangman_1.png',
                'Hangman_2.png',
                'Hangman_3.png',
                'Hangman_4.png',
                'Hangman_5.png',
                'Hangman_6.png',
                'Hangman_7.png',
            )
        ]

        s = ttk.Style()
        s.configure('TLabel', font=('Courier', 16, 'normal'))
        s.configure('TButton', font=('Courier', 12, 'normal'))
        m = s.map('TButton')
        s.map('Correct.TButton', foreground=[(tk.DISABLED, 'green')], **m)
        s.map('Wrong.TButton', foreground=[(tk.DISABLED, 'red')], **m)

        self.last_button_press_status = tk.StringVar()
        self.word = ''
        self.init_labels()
        self.init_ui()

    def init_labels(self) -> None:
        for i in range(self.MAX_WORD_LENGTH):
            l = ttk.Label(
                self.word_frame,
                text='_' if i < len(self.word) else ' ',
                width=2,
                padding=1,
                takefocus=False,
            )
            l.grid(row=0, column=i)

    def init_ui(self) -> None:
        alphabet = ['ABCDEFGHI', 'JKLMNOPQR', 'STUVWXYZ ']
        for r, sub_alpha in enumerate(alphabet):
            for c, letter in enumerate(sub_alpha):
                b = ttk.Button(
                    self.button_frame,
                    text=letter,
                    width=2,
                    takefocus=False,
                    padding=3,
                    command=lambda l=letter: self.guess_letter(l),  # type: ignore
                )
                b.grid(row=r, column=c)
                self.button_mapping[letter] = b
        self.button_mapping[' '].state([tk.DISABLED])

        self.man_label.config(image=self.images[0])

        self.man_label.grid(row=0, column=0, padx=5, pady=5)
        self.word_frame.grid(row=1, column=0, padx=5, pady=5)
        self.button_frame.grid(row=2, column=0, padx=5, pady=5)

        self.parent.winfo_toplevel().bind('r', lambda *_: self.reset())

    def guess_letter(self, letter: str) -> None:
        if self.lost or not self.alive:
            return
        button_pressed = self.button_mapping[letter]
        self.guessed_letters.add(letter)
        if letter in self.word:
            button_pressed.config(style='Correct.TButton')
            self.last_button_press_status.set('correct')
        else:
            button_pressed.config(style='Wrong.TButton')
            self.last_button_press_status.set('wrong')
            self.lives_remaining -= 1
            self.man_label.config(image=self.images[6 - self.lives_remaining])
            if not self.lives_remaining:
                self.lost = True
        button_pressed.state([tk.DISABLED])
        self.update_word_display()

    def update_word_display(self) -> None:
        for label, letter in zip(reversed(self.word_frame.grid_slaves()), self.word):
            if letter in self.guessed_letters:
                assert isinstance(label, ttk.Label)
                label.configure(text=letter)

    def prompt_for_input(self, prompt='Provide a Word') -> None:
        word = tk.StringVar()
        while not word.get():
            HangmanWordEntry(
                self.parent.winfo_toplevel(),
                self.MAX_WORD_LENGTH,
                word,
                prompt,
            )
        labels = [w for w in self.word_frame.grid_slaves() if isinstance(w, ttk.Label)]
        labels.reverse()
        for i, label in enumerate(labels):
            label.configure(text='_' if i < len(word.get()) else ' ')
        self.alive = True
        self.word = word.get().upper()

    def reset(self, msg='Provide a Word') -> None:
        self.lost = False
        self.prompt_for_input(msg)
        self.guessed_letters = set()
        self.lives_remaining = self.LIVES
        self.man_label.config(image=self.images[0])
        for button in self.button_mapping.values():
            button.state([f'!{tk.DISABLED}'])
        labels = [w for w in self.word_frame.grid_slaves() if isinstance(w, ttk.Label)]
        labels.reverse()
        for i, label in enumerate(labels):
            label.configure(text='_' if i < len(self.word) else ' ')


def main():
    root = tk.Tk()
    root.title('Hangman')
    root.resizable(False, False)
    main_frame = tk.Frame(root)
    main_frame.grid(row=0, column=0)
    hg = Hangman(main_frame)
    hg.prompt_for_input()
    root.mainloop()


if __name__ == '__main__':
    main()
