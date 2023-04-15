import tkinter as tk
import tkinter.ttk as ttk

class Hangman:
    def __init__(self, parent: tk.Widget) -> None:
        self.LIVES = 6
        self.word = self.prompt_for_input()

        self.parent = parent
        self.button_frame = ttk.Frame(parent)
        self.button_mapping: dict[str, ttk.Button] = {}

        self.init_ui()

    def init_ui(self) -> None:
        ttk.Style().configure('TButton', font=('Helvetica', 16, 'normal'))
        alphabet = ['ABCDEFGHI', 'JKLMNOPQR', 'STUVWXYZ ']
        for r, sub_alpha in enumerate(alphabet):
            for c, letter in enumerate(sub_alpha):
                b = ttk.Button(
                    self.button_frame,
                    text=letter,
                    width=2,
                    takefocus=False,
                    padding=5,
                    command=lambda l=letter: self.guess_letter(l)  # type: ignore
                )
                b.grid(row=r, column=c)
                self.button_mapping[letter] = b
        self.button_mapping[' '].state([tk.DISABLED])
        self.button_frame.grid(row=1, column=0)

    def guess_letter(self, letter: str) -> None:
         button_pressed = self.button_mapping[letter]
         button_pressed.state([tk.DISABLED])

    def play_game(self) -> None:
        print('Start guessing')
        guesses: set[str] = set()
        lives_remaining = self.LIVES

        while lives_remaining:
            unknown_letters = 0
            for char in self.word:
                if char in guesses:
                    print(char, end='')
                else:
                    print('_', end='')
                    unknown_letters += 1
            print()

            if not unknown_letters:
                print('You guessed the word!')
                print('Wait for next word')
                break

            guess = input('Guess a letter: ')
            while guess in guesses:
                guess = input('You already guessed that. Guess a different letter: ')
            guesses.add(guess)

            if guess not in self.word:
                print('Incorrect guess.')
                lives_remaining -= 1
                print(f'You have lives left: {lives_remaining}')

        print('Ran out of lives.')

    def prompt_for_input(self) -> str:
        phrase = input('Enter in a word: ')
        while not phrase.isalpha():
            print('Invalid entry. Try again.')
            phrase = input('Enter in a word: ')
        return phrase.lower()


def main():
    root = tk.Tk()
    root.title('Hangman')
    root.resizable(False, False)
    main_frame = tk.Frame(root)
    main_frame.grid(row=0, column=0)
    hg = Hangman(main_frame)
    hg.play_game()
    root.mainloop()


if __name__ == '__main__':
    main()
