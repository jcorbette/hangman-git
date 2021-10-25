#!/usr/bin/env python

import random
import string
import time
from threading import Timer
import copy
# This imports the list of words and optimal letter guesses from external python files
from words import word_list
from best_letter_guess import optimal_letter_guess


def get_word():
    # This function randomly selects a word from the imported list a new game round and returns this word
    word = random.choice(word_list).upper()
    return word


class Guess:

    # def __init__(self, hint):
    #     self.hint = hint

    def guess_optimal_letter(hint):
        # This function selects a list of optimal letters to guess in order based on word length and returns the first letter in that list
        for key, value in optimal_letter_guess.items():
            if key == hint:
                guess = value[0]
        return guess

    def optimal_guess_list(hint):
        # This function selects a list of optimal letters to guess in order based on word length and returns that list

        for key, value in optimal_letter_guess.items():
            if key == hint:
                return value

    def guess_letter():
        # This function allows the computer player to guess a random letter and returns this letter
        alphabet = string.ascii_letters.upper()
        guess = random.choice(alphabet)
        return guess

    def display_hangman(self):
        stages = [  # final state: head, torso, both arms, and both legs
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


def loading_guess():
    # This function displays text that simulates the computer taking time to guess a letter
    for i in range(0, 30):
        if tries > 1:
            loading_text = "The computer is choosing a letter" + "." * i
        else:
            loading_text = "The computer is trying to guess the word" + "." * i
        # loading_text replaces previous loading_text for each iteration
        print(loading_text, end="\r")
        time.sleep(0.1)


def get_guessed_word(possible_words, hidden_actual_letters, correct_guessed):
    # This function

    new_possible_words = []

    for x in possible_words:

        full_word = list(x)

        check = [index for index, (e1, e2) in enumerate(
            zip(full_word, hidden_actual_letters)) if e1 == e2]

        if (len(list(check))) == len(correct_guessed):

            new_possible_words.append(x)

    return new_possible_words


class PlayHangman(Guess):

    def __init__(self, tries):
        self.tries = tries

    def game_play(self):
        # This function contains the code for the main hangman gameplay and logic
        playing = True
        start = False
        global tries
        tries = 6  # variable storing number of attempts left in gameplay
        actual_word = get_word()  # variable storing word that must be solved
        # variable storing list of letters in game word
        actual_letters = list(actual_word)
        letters_guessed = []  # variable intended to store already guessed letters in game
        correct_guessed = []  # variable intended to store list of correctly guessed letters
        value_list = []  # variable intended to store optimal calling order of letters
        possible_words = []  # this variable contains a list of possible words based on hint

        word_list_lengths = []
        for x in word_list:
            # creates list of all word lengths in words.py
            word_list_lengths.append(len(x))

        print("\n")
        print("Let's play Hangman! \n")
        time.sleep(0.5)
        print(Guess.display_hangman(tries))
        time.sleep(0.5)
        # shows user randomly selected word for game
        print("Let's see if the computer can figure out what your word is. (It's {}"")".format(
            actual_word))
        time.sleep(1.5)

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

        value_list = Guess.optimal_guess_list(letters_hint)
        optimal_left = copy.deepcopy(value_list)

        hidden_actual_letters = copy.deepcopy(actual_letters)
        # this for loop replaces leters from copy of actual word list with blank lines
        for i in range(len(hidden_actual_letters)):
            if actual_letters[i] != "":
                # replace letters with this string
                hidden_actual_letters[i] = "__"

        for x in word_list:
            if len(x) == letters_hint:
                possible_words.append(x.upper())

        # this loop allows the computer to guess another letter until the word is completed or there are no more tries left
        while playing == True and tries > 0:

            time.sleep(1)
            print("\n")
            print("Number of tries left: {}".format(tries))
            print("Here we go!")

            # creates new thread where loading_guess function is called
            Timer(3, loading_guess).start()
            time.sleep(7)
            print("\n", end="\n")

            # this if statement allows current guess to be any random letter once all the letters in optimal guess list have been used
            if len(optimal_left) > 0:
                current_guess = optimal_left[0]
            else:
                current_guess = Guess.guess_letter()

            # this if statement checks the number of tries to see if a normal guess should be word or the entire word
            if tries > 1:
                print("The computer guessed {} \n".format(current_guess))
            else:
                print("")

            # this if statement checks if guess is correct
            if current_guess in actual_letters and current_guess not in letters_guessed and tries > 1:
                print("Good job. {} is in the word!".format(current_guess))
                print(Guess.display_hangman(tries))

                for i in range(len(actual_letters)):
                    if actual_letters[i] == current_guess:
                        hidden_actual_letters[i] = current_guess

                print('   ' + ' '.join(hidden_actual_letters))

                if hidden_actual_letters == actual_letters:
                    playing == False

                # adds to list of previous guesses
                letters_guessed.append(current_guess)
                # this if statement checks to see if there are optimal guesses left and removes current letter from optimal list after each use
                if len(optimal_left) != 0:
                    optimal_left.remove(current_guess)
                else:
                    continue

            # this if statement displays wrong guess, new hangman stage and reduces number of tries
            elif current_guess in letters_guessed and tries > 1:
                print("This letter was already guessed. Try again.")
                print(Guess.display_hangman(tries))
                print("   " + " ".join(hidden_actual_letters))

            elif current_guess not in actual_letters and tries > 1:
                print("Sorry, {} isn't in the word".format(current_guess))
                tries -= 1
                letters_guessed.append(current_guess)
                print(Guess.display_hangman(tries))  # prints hangman stage
                print('   ' + ' '.join(hidden_actual_letters))
                if len(optimal_left) != 0:
                    optimal_left.remove(current_guess)
                else:
                    continue

            elif tries == 1:
                for character in hidden_actual_letters:
                    if character != "__":
                        correct_guessed.append(character)
                answer = random.choice(get_guessed_word(
                    possible_words, hidden_actual_letters, correct_guessed))
                print("The actual word was " + "".join(actual_letters))
                playing = False

        # Rest of code goes here
        if answer == actual_word:
            print("The computer guessed {}\n".format(answer))
            print("Yay! The computer won! It guessed the correct word.")
            print(Guess.display_hangman(tries))

        else:
            print("The computer guessed {}\n".format(answer))
            print("This was too many wrong guesses, sorry.")
            tries -= 1
            print(Guess.display_hangman(tries))
            print("               GAMEOVER")


def main():
    # this function calls the play_hangman function and repeats it when the user says yes

    PlayHangman(6).game_play()
    replay = True

    # this loop asks the user if they want to play again
    while replay == True:
        answer = input("Do you want to play again? (Yes/No) - ")
        if answer.upper() == "YES" or answer.upper() == "Y":
            print("----------------------------------------------------------------------------------------------------------------- \n")
            PlayHangman(6).game_play()
        else:
            replay = False
    print("\n")
    print("Thank you for playing!")


if __name__ == "__main__":
    main()
