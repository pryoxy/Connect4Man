import time

print('hello')

#prompting the person to enter in 5 words 
#sets of each word is stored as a string. Each set of strings is stored in its own array
# while loop that continuously prompts for user input for guessing words

class Hangman:
    #init has everything that you want to keep in t
    def __init__(self,word):  #word is the word the user inputs
        self.word = word
        self.LIVES = 6

    def play_game(self):    #starts playing game
        guesses = ''    #guesses of player
        
        print('Start guessing') 

        
        lives = self.LIVES 
        while lives > 0:
            for char in self.word:  #checks guesses and compares to word
                if char in guesses:
                    print(char,end=''), #print guessed characters
                else:
                    print('_',end=''),  #print dash for unknown
                    failed += 1
            
            if failed == 0:   #player won 
                print('won')
                break

            guess = input('guess a letter')
            guesses += guess

            if guess not in self.word:
                #add timer decrease
                print('wrong'),
            else:
                cons_guess += 1
                if cons_guess > 2:
                    #add timeout




