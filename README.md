# The Hangman Game

## About the Project/Problem Statement

In this game, the user only enters the number of letters existing in that word, and the computer tries to guess them based on a fixed number of attempts. The game ends if the computer correctly guessed all the letters in order or used all of the given attempts. 

- A random word will be selected from a list of words for gameplay
- There are six (6) attempts in gameplay; on the last try the computer will try to guess the full word
- Part of a hangman drawing will be displayed as wrong guesses are made
- The game will end prematurely if all letters are guessed before all attempts are used 
-  There will be an option to play again once the game is over

## Prerequisites

Install Python 3


## Usage
- git clone https://github.com/jcorbette/hangman-git.git
- cd hangman-git
- run on Windows (run hangman.py) 
```bash
 ./hangman.py
```
- run on Linux (change default shebang statement in hangman.py to the following and make file executable)
```bash
nano hangman.py
#!/usr/bin/env python

#!/usr/bin/env python3

sudo chmod +x hangman.py

./hangman.py
```

## Project Images
![Game Start Screenshot](/images/screenshot-1.jpeg?raw=true "Game Start")
![Correct Guess Screenshot](/images/screenshot-2.jpeg?raw=true "Correct Guess")
![Wrong Guess Screenshot](/images/screenshot-3.jpeg?raw=true "Wrong Guess")
![Game Won Screenshot](/images/screenshot-4.jpeg?raw=true "Game Won")
![Game Lost Screenshot](/images/screenshot-5.jpeg?raw=true "Game Lost")
![Wrong Hint Screenshot](/images/screenshot-6.jpeg?raw=true "Wrong Hint")


## Resources
Want to learn about how guessing was made more efficient in this hangman game? Check out this link:

https://datagenetics.com/blog/april12012/index.html

Here you will find info on how to increase your chances of guessing the correct letters based on the length of the given word. It's called an Optimal Calling Order.
