import random as rd
from matplotlib import pyplot as plt


def simulate_dice_rolls(N):
    roll_counts = [0, 0, 0, 0, 0, 0]
    for i in range(N):
        roll = rd.choice([1, 2, 3, 4, 5, 6])
        index = roll - 1
        roll_counts[index] = roll_counts[index] + 1
    return roll_counts


def show_roll_data(roll_counts):
    number_of_sides_on_die = len(roll_counts)
    for i in range(number_of_sides_on_die):
        number_of_rolls = roll_counts[i]
        number_on_die = i + 1
        print(number_on_die, "came up", number_of_rolls, "times")


def visualize_one_die(roll_data):
    roll_outcomes = [1, 2, 3, 4, 5, 6]
    fig, ax = plt.subplots()
    ax.bar(roll_outcomes, roll_data)
    ax.set_xlabel("Value on Die")
    ax.set_ylabel("# rolls")
    ax.set_title("Simulated Counts of Rolls")
    plt.show()


roll_data = simulate_dice_rolls(1000)
show_roll_data(roll_data)
visualize_one_die(roll_data)
