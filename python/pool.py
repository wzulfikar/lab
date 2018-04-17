from multiprocessing import Pool
import time


def square(x):
    print("square: sleeping for 2 second")
    time.sleep(2)
    # calculate the square of the value of x
    return x * x


def add(x, y):
    print("add: sleeping for 2 second")
    time.sleep(2)
    # sum the value of x and y
    return x + y


if __name__ == '__main__':

    # Define the dataset
    dataset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    # Output the dataset
    print('Dataset: ' + str(dataset))

    # Run function of single arg with a pool of 5 agents
    # having a chunksize of 3 until finished
    agents = 5
    chunksize = 3
    with Pool(processes=agents) as pool:
        square_result = pool.map(square, dataset, chunksize)

    # run same pool config for function with multiple args
    with Pool(processes=agents) as pool:
        add_result = pool.starmap(add, [
            (1, 2),
            (2, 1),
            (2, 1),
            (2, 1),
            (2, 1),
            (2, 1),
            (2, 1),
            (2, 1),
            (2, 1),
            (3, 1)])

    # Output the result
    print('Square result:  ' + str(square_result))
    print('Sum result:  ' + str(add_result))
