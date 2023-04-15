import time
import string

print('hello')

#prompting the person to enter in 5 words 
#sets of each word is stored as a string. Each set of strings is stored in its own array
# while loop that continuously prompts for user input for guessing words

class Hangman:
    #init has everything that you want to keep in t
    def __init__(self):  #word is the word the user inputs
        self.LIVES = 6
        self.word = ''

    def play_game(self):    #starts playing game
        guesses = ''    #guesses of player
        print('Start guessing') 


        lives = self.LIVES 
        cons_guess = 0
        while 1:
            failed = 0

            for char in self.word:  #checks guesses and compares to word
                if char in guesses:
                    print(char,end='') #print guessed characters
                else:
                    print('_ ',end='')  #print dash for unknown
                    failed += 1
                    # failed = failed + 1
            
            if not failed:   #player won 
                print('\nYou guessed the word!\nWait for next word')
                break

            while 1:
                guess = input('\nGuess a letter: ')
                if guess not in guesses:
                    break
                else:
                    print('\nYou already guessed that')
           

            guesses += guess

            if guess not in self.word:
                #add timer decrease
                print('Incorrect guess\n')
                print('Lives left: ' + lives)
                lives -= 1
                if not lives:
                    lives = self.LIVES
                    print('Ran out of lives')
                    time.sleep(5)
            else:
                cons_guess += 1
                if cons_guess > 2:
                    time.sleep(5)

    def prompt_for_input(self):
        phrase = input('Enter in a word: ')
        while not phrase.isalpha():
            print('Invalid entry. Try again.')
            phrase = input('Enter in a word: ')

        self.accept_word(phrase.lower())
            
    def accept_word(self,word):
        self.word = word


def main():
    testGame = Hangman()
    testGame.prompt_for_input()
    testGame.play_game()
    

if __name__ == '__main__':
    main()
