print('hello')

#prompting the person to enter in 5 words 
#sets of each word is stored as a string. Each set of strings is stored in its own array
# while loop that continuously prompts for user input for guessing words

class Hangman:
    
    def __init__(self,words):  #words is an array of the phrases that the user enter
        self.wordlist = words
        

