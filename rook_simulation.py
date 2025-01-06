from dataclasses import dataclass
import random

import matplotlib.pyplot as plt
import numpy as np

# this dataclass allows for easy accessing of coordinates.
# we can access Coordinate.x rather than doing coordinate[0] for easy readability
@dataclass
class Coordinate:
    x: int
    y: int

def check_if_two_challenge(rook1_coords: Coordinate, rook2_coords: Coordinate) -> bool:
    '''checks if the xs or the ys are the same, if so they are challenging each other'''
    return rook1_coords.x == rook2_coords.x or rook1_coords.y == rook2_coords.y

def display_chessboard_with_rooks(rook1: Coordinate, rook2: Coordinate):
    '''displays chessboard and challenging positions'''

    ax = plt.subplots(figsize=(6, 6))[1]

    for x in range(8):
        for y in range(8):
            color = 'white' if (x + y) % 2 == 0 else 'gray'
            ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color))

    r1x, r1y = rook1.x - 1, rook1.y - 1
    r2x, r2y = rook2.x - 1, rook2.y - 1

    for i in range(8):
        ax.add_patch(plt.Rectangle((i, r1y), 1, 1, color='red', alpha=0.3))
        ax.add_patch(plt.Rectangle((r1x, i), 1, 1, color='red', alpha=0.3))
        ax.add_patch(plt.Rectangle((i, r2y), 1, 1, color='blue', alpha=0.3))
        ax.add_patch(plt.Rectangle((r2x, i), 1, 1, color='blue', alpha=0.3))

    ax.text(r1x + 0.5, r1y + 0.5, 'R1', color='black', fontsize=12, ha='center', va='center')
    ax.text(r2x + 0.5, r2y + 0.5, 'R2', color='black', fontsize=12, ha='center', va='center')

    challenging = check_if_two_challenge(rook1, rook2)

    if challenging:
        ax.plot([r1x + 0.5, r2x + 0.5], [r1y + 0.5, r2y + 0.5], color='black', linestyle='--', linewidth=1.5)

    status_text = "Challenging" if challenging else "Not Challenging"
    ax.text(4, -1, f"Status: {status_text}", fontsize=12, ha='center', va='center', color='black')

    ax.set_xlim(0, 8)
    ax.set_ylim(-2, 8)
    ax.set_xticks(range(8))
    ax.set_yticks(range(8))
    ax.set_xticklabels(range(1, 9))
    ax.set_yticklabels(range(1, 9))
    ax.grid(False)

    plt.gca().invert_yaxis()
    plt.show()




def check_if_challenge(rook_coords: list[Coordinate]) -> bool:
    '''This checks for challenges in a list of coordinates of arbitrary length. If any challenge is found, it will return True'''

    max_index = len(rook_coords) - 1
    index1, index2 = (0, 1)

    while True:
        if check_if_two_challenge(
            rook_coords[index1],
            rook_coords[index2]
        ):
            return True
        
        if index2 >= max_index:
            index1 += 1
            if index1 == index2: # there is no more coordinates to check
                break
            index2 = index1 + 1

        else:
            index2 += 1

    return False

def allocate_random_positions(n: int) -> list[Coordinate]:
    '''Allocates n unique positions and returns the list of coordinates'''
    positions: set[tuple[int, int]] = set()

    while len(positions) < n:
        positions.add((random.randint(1, 8), random.randint(1, 8)))

    return [Coordinate(pos[0], pos[1]) for pos in positions]

def run_simulation(num_rooks: int, num_simulations: int) -> int:
    '''runs the simulation and returns the total challenges'''
    challenge_count = 0
    for _ in range(num_simulations):
        challenge_count += int(
            check_if_challenge(
                allocate_random_positions(num_rooks)
            )
        )

    return challenge_count
        
NUM_ROOKS = 8
NUM_SIMULATIONS = 10000

def main():

    # individual task 1
    display_chessboard_with_rooks(*allocate_random_positions(2))

    # individual task 2 & 3
    num_challenges = run_simulation(
        NUM_ROOKS,
        NUM_SIMULATIONS
    )

    print (f'Percentage Challenge = {(num_challenges / NUM_SIMULATIONS):.2%}')


if __name__ == '__main__':
    main()

