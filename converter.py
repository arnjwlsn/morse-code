import os
import sys
import time

verbose = False
if len(sys.argv) > 1:
    if sys.argv[1] == '-v' or sys.argv[1] == '--verbose':
        verbose = True
    else:
        print(f'Illegal arguments: {sys.argv[1:]} -- optional -v,--verbose')
        sys.exit()


#
# Config Parameters
#

words_per_minute = 20
tone_frequency = 440  # Hertz

# Duration of 1 unit in seconds
base_duration = 1.2 / words_per_minute 
 
# Duration of dash and next letter pause (3 units)
triple_base_duration = base_duration * 3

#print('------')
#print(f'{words_per_minute} (word/min)')
#print(f'{base_duration} (sec/dot)')
#print('------\n')


#
# Actions
#

def pause():
    time.sleep(base_duration)

def next_letter(): 
    time.sleep(triple_base_duration)

def _play_sound(duration: float, frequency: float):
    # Suppress sounds stdout
    os.system(f'play -n synth {duration} sin {frequency} >/dev/null 2>&1')

def dot():
    _play_sound(base_duration, tone_frequency)

def dash():
    _play_sound(triple_base_duration, tone_frequency)


#
# Preprocessing
#

# Map of all letter values
letters = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
    'y': '-.--', 'z': '--..', '1': '.----', '2': '..---', '3': '...--', 
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', 
    '9': '----.', '0': '-----', ',': '--..--', '.': '.-.-.-', '?': '..--..',
    "'": '.----.', '"': '.-..-.', '/': '-..-.', '(': '-.--.', ')': '-.--.-', 
    '&': '.-..', ':': '---...', ';': '-.-.-.', '=': '-...-', '-': '-....-',
    '+': '.-.-.', '_': '..--.-', '$': '...-..-', '@': '.--.-.'
}

def get_character_function(character: str):
    return dot if character is '.' else dash

# Spaces get a single unit pause since they will be treated like letters and
#  surrounded by next letter pauses: "<next letter pause (3)> <pause (1)> 
#  <next letter pause (3)> = 7 units"
letter_functions = { ' ': [ pause ] } 

# Build function map from letter map
for letter in letters:
    functions = []
    letter_value = letters[letter]

    # Iterate through each letter to build function list
    for i in range(0, len(letter_value) - 1):
        functions.append(get_character_function(letter_value[i]))
        functions.append(pause)
        
    functions.append(get_character_function(letter_value[-1]))

    # Add function list to dictionary
    letter_functions[letter] = functions


#
# Processing
#

def process(value: str):
    actions = []

    for i in range(0, len(value)):
        functions = letter_functions.get(value[i].lower())
        if functions is None:
            print(f'Warning: Ignoring "{value[i]}" character')
            continue

        actions.extend(functions)
        actions.append(next_letter)
    
    [f() for f in actions]

def process_verbose(value: str):
    for i in range(0, len(value)):
        character = value[i].lower()

        functions = letter_functions.get(character)
        if functions is None:
            print(f'Warning: Ignoring "{value[i]}" character')
            continue
        
        actions = letters.get(character)
        if actions is None:
            print('')
        else:
            print(f'{character}: {letters[character]}')

        # Process all functions for character
        [f() for f in functions]
        
        # Pause for next letter
        next_letter()


#
# User Prompt
#

if verbose: 
    process_verbose(input('Enter text to encrypt (verbose):\n'))
else:
    process(input('Enter text to encrypt:\n'))

