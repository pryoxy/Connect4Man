class Hangman:
    def __init__(self) -> None:
        self.LIVES = 6
        self.word = self.prompt_for_input()

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
    testGame = Hangman()
    testGame.play_game()


if __name__ == '__main__':
    main()
