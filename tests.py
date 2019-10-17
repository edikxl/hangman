from hangman import *

dataset = [ [ 'hi', [ 'h','o','i' ] ], [ 'notme', ['n','o','d','k'] ], [ 'check', ['c','e','c'] ] ]

template = """------------------------------
Word:{}
Used letters:{}

Is word guessed: {}
Guessed word: {}
Available letters: {}"""

for elem in dataset:
	print( template.format( *elem, is_word_guessed( *elem ), get_guessed_word( *elem ), get_available_letters( elem[1] ) ) )

#...

dataset = [ [ 'a_ _ le', 'apple' ], [ 'a_ _ le', 'appla' ], [ 'h_ ', 'h' ] ]

template = """------------------------------
My word:{}
Other word:{}

Does matche: {}"""

for elem in dataset:

    print( template.format( *elem, match_with_gaps( *elem ) ) )
    show_possible_matches( elem[0] )