# Jesse Harris
# CSIS 1300-01
# Hangman game

# Required import.
import random

# Functions
def get_word():
    """
    Get a random word from the words.txt file. Returns a string.
    """
    # Attempt to open the word file
    try:
        lines = open('words.txt').read().splitlines()
    # Output an error if we can't open it.
    except:
        print("Unable to open word file!")
    else:
        # Pick a random word out of the file.
        output = random.choice(lines)
        return output

def check_guess(guess:str):
    """
    Checks to see if GUESS is in global ANSWER.
    """
    # Import needed globals.
    global guesses
    global answer
    global unmasked_word
    global guesses_remaining

    # Track if the guess was correct or not.
    correct_guess = False

    # See if this is an attempt to guess the word. We will assume this is
    # the case for any input longer than a single character. Also check to
    # see if it only contains alpha characters.
    if(len(guess) > 1 and guess.isalpha() == True):
        if(guess == answer):
            unmasked_word = answer
            return "Correct word guess! You won!"
        else:
            guesses_remaining = 0
            return "Incorrect word guess! You lost!"

    # Make sure we have good input if it's not a word. It must be a letter.
    if(guess.isalpha() == False):
        return "Invalid characters in the guess! Try again."

    # Check to see if this has already been guessed.
    if(guess in guesses):
        return "Already guessed!"
    # If not, add it to the set of guessed letters.
    guesses.add(guess)
    guess_index = 0
    # Iterate over the letters in the answer looking for a match.
    for letters in answer:
        if(letters == guess):
            correct_guess = True
            # We can rebuild the masked answer to reveal correct guesses.
            word_p1 = unmasked_word[0:guess_index]
            word_p2 = unmasked_word[guess_index+1: ]
            unmasked_word = word_p1 + guess + word_p2
        guess_index += 1
    if(correct_guess):
        return f"We found {guess}!"
    else:
        guesses_remaining -= 1
        return f"We did not find {guess}! "\
            "You have {guesses_remaining} guesses remaining."

def check_win():
    """
    See if the player won or not.
    """
    # Import needed globals
    global unmasked_word
    global guesses
    # Check for any masked characters remaining. If there are any, the
    # player has not yet won.
    for letter in unmasked_word:
        if(letter == '_'):
            return False
    print("You won!")
    return True

def draw_hangman():
    """
    Draws an ASCII representation of the hangman based on remaining guesses.
    """
    global guesses_remaining
    if(guesses_remaining == 10):
        print("|\n|\n|\n|\n|\n|")
    if(guesses_remaining == 9):
        print(" _\n|\n|\n|\n|\n|\n|")
    if(guesses_remaining == 8):
        print(" __\n|\n|\n|\n|\n|\n|")
    if(guesses_remaining == 7):
        print(" __\n|  |\n|\n|\n|\n|\n|")
    if(guesses_remaining == 6):
        print(" __\n|  |\n|  O\n|\n|\n|\n|")
    if(guesses_remaining == 5):
        print(" __\n|  |\n|  O\n|  |\n|\n|\n|")
    if(guesses_remaining == 4):
        print(" __\n|  |\n|  O\n| /|\n|\n|\n|")
    if(guesses_remaining == 3):
        print(" __\n|  |\n|  O\n| /|\\\n|\n|\n|")
    if(guesses_remaining == 2):
        print(" __\n|  |\n|  O\n| /|\\\n|  |\n|\n|")
    if(guesses_remaining == 1):
        print(" __\n|  |\n|  O\n| /|\\\n|  |\n| /\n|")
    if(guesses_remaining == 0):
        print(" __\n|  |\n|  O\n| /|\\\n|  |\n| / \\\n|")

def keep_playing():
    """
    Get input from the user to see if they want to keep playing the game.
    """
    global playing
    choice = input("Keep playing (Y/N)? ")
    # Validate the input. If it fails, call the function recursively until
    # it does not.
    if(choice.lower() != 'y' and choice.lower() != 'n'):
        print("Valid choices are Y or N! Try again")
        return keep_playing()
    elif(choice.lower() == 'y'):
        # Reset the game state if we're playing again.
        reset_game()
        return True
    elif(choice.lower() == 'n'):
        return False

def reset_game():
    """
    Reset the game state.
    """
    # Import needed globals.
    global answer
    global unmasked_word
    global guesses
    global guesses_remaining
    # Reset all of them to the initial game state.
    answer = get_word()
    unmasked_word = '_'*len(answer)
    guesses = set()
    guesses_remaining = 10
    # I would have liked to have used this function to intialize the
    # variables at the beginning, but it kept throwing errors at me. Why? Not
    # entirely sure. But I had the program working so well that I wasn't
    # particularly invested in spending a lot of time troubleshooting and
    # said "meh, good enough".

# Grab our random word
answer = get_word()
# Create a masked copy of the word
unmasked_word = '_'*len(answer)
# Create a set to store our guesses
guesses = set()
# Configurable number of remaining guesses.
guesses_remaining = 10

# Track if we're still playing the game
playing = True

# Welcome and instructions
print("Welcome to Hangman! When prompted, you can guess a letter.")
print("If it's in the word, it will be revealed. If it's not, you lose a")
print("guess and get closer to being hung!")
print("At any time you can attempt to guess the word.")
print("Guess the word wrong and you automatically lose!")

# Outer game loop. Allows choosing to play again.
while(playing == True):
    # Initial draw of the hangman and word to guess.
    draw_hangman()
    print(unmasked_word)
    # Main game loop. Continues until the game is won or lost.
    while(check_win() == False):
        # If they run out of guesses, we quit the game.
        if(guesses_remaining == 0):
            print("You lost! Better luck next time!")
            break
        # Get the user input, check the guess, and return the result.
        print(check_guess(input("Guess: ").lower()))
        # Redraw the hangman and unmasked word.
        draw_hangman()
        print(unmasked_word)
    # Evalute if we're going to keep playing.
    playing = keep_playing()

# Simple goodbye message.
print("Thanks for playing!")