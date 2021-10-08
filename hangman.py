#!/usr/bin/env python

import random
import string
import time
from threading import Timer
# This imports the list of words from external python file
from words import word_list


def get_word():
    # This function randomly selects a word from the imported list a new game round and returns this word
    word = random.choice(word_list).upper()
    return word


def guess_letter():
    # This function allows the computer player to guess a random letter and returns this letter
    alphabet = string.ascii_letters.upper()
    guess = random.choice(alphabet)
    return guess


def loading_guess():
    # This function displays text that simulates the computer taking time to guess a letter
    for i in range(0, 30):
        loading_text = "The computer is choosing a letter" + "." * i
        # loading_text replaces previous loading_text for each iteration
        print(loading_text, end="\r")
        time.sleep(0.1)


def play_hangman():
    # This function contains the code for the main hangman gameplay and logic
    playing = True
    start = False
    tries = 6
    letters_guessed = list(get_word())
    words_guessed = []

    word_list_lengths = []
    for x in word_list:
        # creates list of all word lengths
        word_list_lengths.append(len(x))

    print("\n")
    print("Let's play Hangman! \n")
    time.sleep(0.5)
    # shows user randomly selected word for game
    print("Let's see if the computer can figure out what your word is. (It's {}"")".format(get_word()))
    time.sleep(1.5)

    # this loop allows the computer to guess another letter until the word is completed or there are no more tries left
    while playing == True and tries > 0:

        # this loop allows the user to give the computer a hint before guessing starts
        while start == False:
            try:
                letters_hint = int(input(
                    "Give the computer a hint. How many letters are there in your chosen word?:  "))
                # this if statement checks validity of hint: hint must be less than or equal to max possible word length AND more than or equal to min possible word length
                if letters_hint > max(word_list_lengths) or letters_hint < min(word_list_lengths):
                    raise ValueError
                else:
                    start = True
            # error raised if hint is not valid integer
            except ValueError:
                print("Please make sure you enter a valid number \n")

        time.sleep(1)
        print("\n")
        print("Number of tries left: {}".format(tries))
        print("Here we go!")

        # creates new thread where loading_guess function is called
        Timer(3, loading_guess).start()
        time.sleep(7)
        print("\n", end="\n")
        print("The computer guessed {} \n".format(guess_letter()))
        tries -= 1  # the number of tries remaining decreases by 1 each loop

        # Rest of code goes here

    print("End of current code \n")


def main():
    # this function calls the play_hangman function and repeats it when the user says yes
    play_hangman()
    replay = True

    # this loop asks the user if they want to play again
    while replay == True:
        answer = input("Do you want to play again? (Yes/No) - ")
        if answer.upper() == "YES" or answer.upper() == "Y":
            print("----------------------------------------------------------------------------------------------------------------- \n")
            play_hangman()
        else:
            replay = False
    print("\n")
    print("Thank you for playing!")


if __name__ == "__main__":
    main()
