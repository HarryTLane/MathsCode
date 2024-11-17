import random

MAX_ITERATIONS = 100_000 # number of simulations
ADJACENCY_DICTIONARY: dict[int, tuple[int, ...]] = {
    0: (1, 3, 4),
    1: (0, 2, 5),
    2: (1, 3, 6),
    3: (0, 2, 7),
    4: (0, 5, 7),
    5: (1, 4, 6),
    6: (2, 5, 7),
    7: (3, 4, 6)
}
STEPS = 7 # number of steps the ant takes

def main():
    frequencies: dict[int, int] = {}
    for vertex in range(8): # 8 vertices of a cube
        frequencies[vertex] = 0

    for _ in range(MAX_ITERATIONS):
        current_vertex = 0
        for _ in range(STEPS):
            # finds all possible vertices to go to with ADJACENCY_DICTIONARY[current_vertex]
            # then selects random one with random.choice
            current_vertex = random.choice(ADJACENCY_DICTIONARY[current_vertex])

        frequencies[current_vertex] += 1

        
    # frequencies.items() allows me to iterate over the dictionary
    # and assign number and frequency to all key value pairs.
    for number, frequency in frequencies.items():
        probability = frequency / MAX_ITERATIONS
        print (f'p({number}): {probability:.2%}')


if __name__ == '__main__':

    main()