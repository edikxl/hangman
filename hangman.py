# Problem Set 2, hangman.py
# Name: Eduard Tsakhlo
# Collaborators:
# Time spent: 4 hours 30 minutes

# Hangman Game
# -----------------------------------
# Helper code
import random
from string import ascii_lowercase

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

    return ''.join( [ letter if letter in letters_guessed else '_ ' for letter in secret_word ] )

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''

    return ''.join( sorted( list( set( ascii_lowercase ) - set( letters_guessed ) ) ) )

def get_user_letter( warnings, guesses_remaining, secret_word, letters_guessed, is_with_hints = False ):

    letter = input( 'Please guess a letter: ' ).lower()

    while len( letter ) != 1 or not letter.isalpha() or letter in letters_guessed:

        guessed_word = get_guessed_word( secret_word, letters_guessed )

        if( letter == "*" and is_with_hints ):
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

            if guesses_remaining <= 0:
                guesses_remaining = 0
                return -1, warnings, guesses_remaining

        letter = input( 'Please guess a letter: ' ).lower()

    return letter, warnings, guesses_remaining


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
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

    while not( is_word_guessed( secret_word, letters_guessed ) or guesses_remaining <= 0 ):

        print( f'You have { guesses_remaining } guesses left. Available letters: { get_available_letters(letters_guessed) }' )

        user_letter, warnings, guesses_remaining = get_user_letter( warnings, guesses_remaining, secret_word, letters_guessed )

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

    my_word = my_word.replace( ' ', '' )

    if len( my_word ) == len( other_word ):
        # letters are equal OR this letter in my_word is equal to '_' but there is no
        # other letters in my_word like a letter with the same position in other_word 
        return all([ letter == other_word[index] or ( letter == '_' and my_word.count( other_word[index] ) == 0  ) for index, letter in enumerate( my_word ) ])

    return False

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''

    matches = [ other_word for other_word in wordlist if match_with_gaps( my_word, other_word ) ]

    print( *matches if matches else 'No matches found' )

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
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

    while not( is_word_guessed( secret_word, letters_guessed ) or guesses_remaining <= 0 ):

        print( f'You have { guesses_remaining } guesses left. Available letters: { get_available_letters(letters_guessed) }' )

        user_letter, warnings, guesses_remaining = get_user_letter( warnings, guesses_remaining, secret_word, letters_guessed, is_with_hints = True )

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


if __name__ == "__main__":

    secret_word = choose_word(wordlist)
    #hangman(secret_word)
    hangman_with_hints(secret_word)
