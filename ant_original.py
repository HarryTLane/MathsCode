'''
Problem:
- Annie the ant is on a Pentagon
- Pentagon is labelled anticlockwise from 0 to 4
- She starts at 0
- She moves 7 times either forwards or backwards
- We are interested in frequencies of finishing on each vertex
'''

import random

MAX_ITERATIONS = 100_000 # number of simulations
SIDES = 5 # for a pentagon
STEPS = 7 # number of steps the ant takes

def main():

    # initializing frequency dictionary
    frequencies: dict[int, int] = {}
    for vertex in range(SIDES):
        frequencies[vertex] = 0

    # the _ is just used because I don't care about the value
    for _ in range(MAX_ITERATIONS):
        # this is where Annie starts
        current_vertex = 0
        for _ in range(STEPS):
            # to add is 1 50% of the time and -1 the other 50%
            to_add = 1 if (random.randint(0, 1) == 1) else -1
            # adds this number to the current vertex
            current_vertex += to_add

            # keeps this number in the set 0 to (SIDES - 1) or 4 if you left as pentagon
            current_vertex %= SIDES

        # this accesses the vertex number in the frequency dictionary and adds 1 to it
        frequencies[current_vertex] += 1

    # this formats the output nicely
    # frequencies.items() allows me to iterate over the dictionary
    # and assign number and frequency to all key value pairs.
    for number, frequency in frequencies.items():
        probability = frequency / MAX_ITERATIONS
        print (f'p({number}): {probability:.2%}')

# Having code inside a main function is good practice
if __name__ == '__main__':
    main()
