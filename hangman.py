# Problem Set 2, hangman.py
# Name: Eduard Tsakhlo
# Collaborators:
# Time spent: 4 hours 30 minutes

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
from string import ascii_lowercase
from re import sub, match

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    return set( secret_word ).issubset( set( letters_guessed ) )



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = secret_word
    inter = set( guessed_word ).intersection( set( letters_guessed ) )

    for index, char in enumerate( guessed_word ):
        if not char in inter:
            guessed_word = guessed_word[ :index ] + "_" + guessed_word[ index + 1: ]

    guessed_word = guessed_word.replace( '_', '_ ' )

    return guessed_word


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    
    if letters_guessed:
        characters_to_remove = rf'[{ "".join( letters_guessed ) }]'
        available_letters = sub( characters_to_remove, '', ascii_lowercase )

    else:
        available_letters = ascii_lowercase

    return available_letters

def get_user_letter( warnings, guesses_remaining, secret_word, letters_guessed, is_with_hints ):

    letter = input( 'Please guess a letter: ' ).lower()

    while len( letter ) != 1 or not letter.isalpha() or letter in letters_guessed:

        guessed_word = get_guessed_word( secret_word, letters_guessed )

        if( letter == "*" ):
            show_possible_matches( guessed_word )
            letter = input( 'Please guess a letter: ' ).lower()
            continue

        warnings -= 1

        if warnings != 0:
            if letter in letters_guessed:
                print( f'Oops! You\'ve already guessed that letter. You have { warnings } warnings left: {guessed_word}' )

            else:
                print( f'Oops! That is not a valid letter. You have { warnings } warnings left: {guessed_word}' )
        
        else:
            guesses_remaining -= 1
            print( f'You have no warnings left so you lose one guess. { guesses_remaining } guesses left: {guessed_word}' )

            if guesses_remaining == 0:
                return -1, warnings, guesses_remaining

        letter = input( 'Please guess a letter: ' ).lower()

    return letter, warnings, guesses_remaining


def hangman(secret_word, is_with_hints=False):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    vowels = 'aeiou'
    filler = '-' * 10
    warnings = 3
    guesses_remaining = 6
    letters_guessed = []
    is_game_ended = False

    print( f"""Welcome to the game Hangman!
You are allowed to write only one alphabetical symbol in any case.
I am thinking of a word that is { len(secret_word) } letters long.
You have { warnings } warnings left.
{filler}""" )

    while not( is_word_guessed( secret_word, letters_guessed ) or guesses_remaining == 0 ):

        print( f'You have { guesses_remaining } guesses left. Available letters: { get_available_letters(letters_guessed) }' )

        user_letter, warnings, guesses_remaining = get_user_letter( warnings, guesses_remaining, secret_word, letters_guessed, is_with_hints )

        if user_letter == -1: # User ran out of guesses
            print( filler )
            break

        letters_guessed.append( user_letter )

        if user_letter in secret_word:
            print( f'Good guess: { get_guessed_word( secret_word, letters_guessed ) }' )

        else:

            guesses_remaining -= 2 if user_letter in vowels else 1

            print( f'Oops! That letter is not in my word: { get_guessed_word( secret_word, letters_guessed ) }' )

        print( filler )

    if guesses_remaining > 0:
        score = guesses_remaining * len( set( secret_word ) )
        print( f'Congratulations, you won!\nYour total score for this game is: { score }' )

    else:
        print( f'Sorry, you ran out of guesses. The word was { secret_word }' )


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''

    does_match = True if match( my_word.replace( '_ ', '.' ), other_word ) else False

    if len( my_word.replace(' ', '') ) != len( other_word ): does_match = False
    
    return does_match


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    possible_words = []

    for other_word in wordlist:
        if match_with_gaps( my_word, other_word ):
            possible_words.append( other_word )

    print( *possible_words )

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    hangman( secret_word, True )


if __name__ == "__main__":

    secret_word = choose_word(wordlist)
    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)
