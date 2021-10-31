#!/usr/bin/env python

import random
import string
import time
from threading import Timer
import copy

from words import word_list  # This imports the list of words for gameplay from external file words.py 
from best_letter_guess import optimal_letter_guess # This imports the dictionary of optimal letter calling order from external file best_letter_guess.py



class Guess:
    # This class contains a collection of methods related to the guessing functionality

    def get_word():
        # This function randomly selects a word from the imported list for a new game round and returns this word
        word = random.choice(word_list).upper()        
        return word
    
        
    def optimal_guess_list(letters_hint):
        # This function selects a list of optimal letters to guess in order based on word length and returns that list
        for key, value in optimal_letter_guess.items():
            if key == letters_hint: # compares value of key to hint given by user
                return value
                

    def guess_optimal_letter(letters_hint):
        # This function selects a list of optimal letters to guess in order based on word length and returns the first letter in that list
        for key, value in optimal_letter_guess.items():
            if key == letters_hint: 
                guess = value[0] # value is first item in list
        return guess


    def guess_letter():
        # This function allows the computer to guess a random letter and returns this letter
        alphabet = string.ascii_letters.upper()
        guess = random.choice(alphabet)
        return guess


    def get_guessed_word(possible_words, hidden_actual_letters, correct_guessed):
        # This function allows the computer to shortlist the possible words based on indexes of guessed letters and choose final word from that list

        new_possible_words = [] # empty list intended to store new range of possible words to guess on last try

        for x in possible_words:

            full_word = list(x)
            
            # this variable stores array of indexes in partially guessed word that match the indexes of letters in each possible word 
            check = [index for index, (e1, e2) in enumerate(zip(full_word, hidden_actual_letters)) if e1 == e2]
            
            # appends word to new list if length of correct matching indexes list is equal to number of correctly guessed letters
            if (len(list(check))) == len(correct_guessed): 
                new_possible_words.append(x)  

        try:
            final_guess = random.choice(new_possible_words) # randomly selects a final word from the new list
        except IndexError: # error eventually raised if hint given at beginning of game was less than the length of actual word
            final_guess = "Oops! Looks like you gave the wrong hint, so the computer couldn't guess a word with the right length"

        return final_guess


    def loading_guess():
        # This function displays text that simulates the computer taking time to guess a letter
        for i in range(0, 30):
            
            if tries != 1:
                loading_text = "The computer is choosing a letter" + "." * i
            else:
                loading_text = "The computer is trying to guess the word" + "." * i
                
            # loading_text replaces previous loading_text for each iteration
            print(loading_text, end="\r")
            
            time.sleep(0.1)




class PrintImage:
    # This class contains a method that displays gameplay image

    def display_hangman(tries):
        # This function returns a specific hangman game image based on the number of tries left
        
        # this list contains different image stages
        stages = [  
            # final state: head, torso, both arms, and both legs
            """
                --------
                |      |
                |      O
                |     \\|/
                |      |
                |     / \\
                -
                """,
            # head, torso, both arms, and one leg
            """
                --------
                |      |
                |      O
                |     \\|/
                |      |
                |     /
                -
                """,
            # head, torso, and both arms
            """
                --------
                |      |
                |      O
                |     \\|/
                |      |
                |
                -
                """,
            # head, torso, and one arm
            """
                --------
                |      |
                |      O
                |     \\|
                |      |
                |
                -
                """,
            # head and torso
            """
                --------
                |      |
                |      O
                |      |
                |      |
                |
                -
                """,
            # head
            """
                --------
                |      |
                |      O
                |
                |
                |
                -
                """,
            # initial empty state
            """
                --------
                |      |
                |
                |
                |
                |
                -
                """
        ]
        return stages[tries]




class PlayHangman(Guess, PrintImage):
    # This class contains a collection of methods related to the main hangman gameplay

    def __init__(self, attempts):
        # Creating constructor
        self.attempts = attempts


    def reduce_optimal_list(self, optimal_left, current_guess):
        # This function removes the currently guessed letter from the list of optimal letters to guess, as long as there are still items in that list
        if len(optimal_left) != 0:
            optimal_left.remove(current_guess)
        else:
            pass 


    def game_start(self, actual_word):
        # This function displays the text at start of game, prompts user for hint input, and creates list of entire word list lengths
       
        global letters_hint # variable storing the hint that user enters
        global tries
        tries = self.attempts # variable storing number of tries left in gameplay
        start = False # variable storing state that decides if gameplay logic starts

        print("\n")
        print("Let's play Hangman! \n")
        time.sleep(0.5)
        print(PrintImage.display_hangman(tries)) # displays initial hangman image
        time.sleep(0.5)
        # shows user randomly selected word for game
        print("Let's see if the computer can figure out what your word is. (It's {}"")".format(actual_word))
        time.sleep(1.5)
        
        # this list stores the length of each word in word_list from words.py
        word_list_lengths = [len(x) for x in word_list]

        # this loop allows the user to give the computer a hint before gameplay logic starts
        while start == False:
            
            try:
                
                letters_hint = int(input(
                    "Give the computer a hint. How many letters are there in your chosen word?:  "))
                # this if statement checks validity of hint: hint must be less than or equal to max possible word length AND more than or equal to min possible word length
                if letters_hint > max(word_list_lengths) or letters_hint < min(word_list_lengths):
                    raise ValueError # error raised if hint is not valid integer
                else:
                    start = True # state change will cause loop exit
            
            except ValueError: 
                print("Please make sure you enter a valid number \n")


    def show_result(self, actual_word, actual_letters, hidden_actual_letters, letters_hint, tries):
        # This function shows the results of gameplay; whether computer won or not
    
        if answer == actual_word: # result if final guess is equal to the actual word
            print("The computer guessed {}\n".format(answer))
            print("Yay! The computer won! It guessed the correct word.")
            print(PrintImage.display_hangman(tries))

        elif hidden_actual_letters == actual_letters: # result if computer filled in all letters before tries were finished
            print("\n")
            print("Yay! The computer completed the word {} before all tries were up!".format(actual_word))
            print(PrintImage.display_hangman(tries))

        elif len(actual_letters) != letters_hint: # result if a wrong hint was given at start of game
            if len(actual_letters) < letters_hint:
                print("Oops! Looks like you gave the wrong hint, so the computer couldn't guess a word with the right length")
            else:
                print(answer)
            print("Try starting over")
            tries -= 1
            print(PrintImage.display_hangman(tries))

        else: # result if all guesses were wrong
            print("The computer guessed {}\n".format(answer))
            print("This was too many wrong guesses, sorry.")
            tries -= 1
            print(PrintImage.display_hangman(tries))
            print("               GAMEOVER\n")



    def game_play(self):
        # This function contains the code for the main hangman gameplay and logic

        global tries
        global answer
        playing = True # variable that stores current game state
        actual_word = Guess.get_word()  # variable storing word that must be solved
        actual_letters = list(actual_word)  # variable storing list of letters in actual word chosen for game
        letters_guessed = []  # variable intended to store already guessed letters in game
        correct_guessed = []  # variable intended to store list of correctly guessed letters
        value_list = []  # variable intended to store optimal calling order of letters
        possible_words = []  # variable intended to store a list of possible words that have the same length as the given hint
        

        self.game_start(actual_word) # this calls the game_start function
        
        # this block of code establishes various lists
        value_list = Guess.optimal_guess_list(letters_hint)
        optimal_left = copy.deepcopy(value_list) # creates copy of value_list
        hidden_actual_letters = copy.deepcopy(actual_letters) # creates copy of actual_letters list
        hidden_actual_letters =  ["__" for i in range(len(hidden_actual_letters)) if actual_letters[i] != ""] # replaces letters from copy of actual_letters list with blank lines
        possible_words = [x.upper() for x in word_list if len(x) == letters_hint] # adds each word with appropriate length to list of possible words
        
        
        #this loop allows the computer to guess another letter until the word is completed or there are no more tries left
        while playing == True and tries > 0:
            
            # this block of code displays the number of tries and the start of the computer guessing
            time.sleep(1)
            print("\n")
            print("Number of tries left: {}".format(tries))
            print("Here we go!")
            Timer(3, Guess.loading_guess).start() # creates new thread where loading_guess function is called
            time.sleep(7)
            print("\n", end="\n")

            # this if statement allows the current guess to be any random letter once all the letters in optimal guess list(optimal_left) have been used
            if len(optimal_left) > 0:
                current_guess = optimal_left[0]
            else:
                current_guess = Guess.guess_letter()

            # this if statement prints the guessed letter if there is more than one try available
            if tries > 1:
                print("The computer guessed {} \n".format(current_guess))
            else:
                print("")

            partial_word = '   ' + ' '.join(hidden_actual_letters) # joins the blank lines and/or correctly guessed letters and prints as one string


            # the following statements check whether the letter guessed is correct
            
            # this if statement checks if the current guess is in list of actual letters and that it has not already been guessed, while the number of tries is more than one
            if current_guess in actual_letters and current_guess not in letters_guessed and tries > 1:
                
                print("Good job. {} is in the word!".format(current_guess))
                print(PrintImage.display_hangman(tries))
                
                # this for loop replaces each blank line with the correctly guessed letter
                for i in range(len(actual_letters)):
                    if actual_letters[i] == current_guess:
                        hidden_actual_letters[i] = current_guess # blank line in hidden_actual_letters becomes current guess
     
                partial_word = '   ' + ' '.join(hidden_actual_letters)
                print(partial_word)
                
                # this if statement checks if all letters in actual word have have been guessed
                if hidden_actual_letters == actual_letters:
                    playing = False # exit loop as game will no longer be played
                    answer = partial_word

                letters_guessed.append(current_guess) # adds to list of previous guesses
       
                self.reduce_optimal_list(optimal_left, current_guess) # calls the reduce_optimal_list function


            # this elif statement displays text if current guess is already in list of guessed letters and displays unchanged hangman image stage
            elif current_guess in letters_guessed and tries > 1:
                print("This letter was already guessed. Try again.")
                print(PrintImage.display_hangman(tries))
                print(partial_word)


            # this elif statement displays wrong guess, new hangman image stage and reduces number of tries if current guess is not in list of actual letters
            elif current_guess not in actual_letters and tries > 1:
                print("Sorry, {} isn't in the word".format(current_guess))
                tries -= 1
                letters_guessed.append(current_guess)
                print(PrintImage.display_hangman(tries))
                print(partial_word)
                self.reduce_optimal_list(optimal_left, current_guess)

            # this elif statement displays the actual word and new hangman image stage, creates list of correctly guessed letters, and guesses full word if the number of tries is one
            elif tries == 1:
                          
                correct_guessed = [character for character in hidden_actual_letters if character != "__"] # add all correct letters to list   
   
                print("The actual word was " + "".join(actual_letters))

                answer = Guess.get_guessed_word(possible_words, hidden_actual_letters, correct_guessed) # variable storing the word the computer chose as final guess

                playing = False # exit loop as state changes
                
                
        self.show_result(actual_word, actual_letters, hidden_actual_letters, letters_hint, tries) # calls the show_result function




def main():
    # This function starts entire gameplay by creating a new instance of the PlayHangman class and repeats it when the user says yes
    
    new_game_instance = PlayHangman(6)
    new_game_instance.game_play()
    replay = True

    # this loop asks the user if they want to play again
    while replay == True:
        answer = input("Do you want to play again? (Yes/No) - ")
        if answer.upper() == "YES" or answer.upper() == "Y":
            # this prints horizontal line to separate previous game round from new one
            print("----------------------------------------------------------------------------------------------------------------- \n")
            new_game_instance.game_play()
        else:
            replay = False # game permanently ends once state change occurs 
   
    print("\n")
    print("Thank you for playing!")


if __name__ == "__main__":
    main()