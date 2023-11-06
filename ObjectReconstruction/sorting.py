## Author : Filip Lindhe

import numpy as np
import time
import matplotlib.pyplot as plt
import winsound
import random


def bogo_sort():
    size = 100
    array = np.random.randint(1, size, 100)
    plt.ion
    sortedarray = []
    sortedarray = np.sort(array)
    x = np.arange(size)
    figure, ax = plt.subplots()
    line1 = ax.bar(x, array)
    t = time.time()
    plt.title("Geeks For Geeks", fontsize=20)
    line1.remove()

    figure.show()
    i = 1
    while not (sortedarray == array).all():
        np.random.shuffle(array)
        plt.title("Bogosort - # of swaps :%i" % i, fontsize=20)
        line1 = ax.bar(x, array, color="grey", width=1)
        figure.canvas.draw()
        figure.canvas.flush_events()

        # duration = 50
        # time.sleep(0.01)
        # sum = np.sum(sortedarray == array)
        # frequency = 200 + 40 * (sum * 10)
        # winsound.Beep(frequency, duration)
        line1.remove()
        i = i + 1
    totalElapsed = time.time() - t
    plt.title("Bogosort - # of swaps :%i" % i, fontsize=20)
    line1 = ax.bar(x, array, color="grey", width=0.1)
    figure.canvas.draw()
    # figure.canvas.flush_events()
    plt.show()
    print("Time to complete bogosort : ", totalElapsed, "Swaps needed :", i)
    print("hello")


def bubble_sort():
    size = 30
    array = np.random.randint(1, size, size)
    plt.ion
    sortedarray = []
    sortedarray = np.sort(array)
    x = np.arange(size)
    figure, ax = plt.subplots()
    line1 = ax.bar(x, array)
    t = time.time()
    plt.title("Bubble sort", fontsize=20)
    line1.remove()

    figure.show()
    i = 1
    while not (sortedarray == array).all():
        for i in range(len(array) - 1):
            if array[i] > array[i + 1]:
                temp = array[i]
                array[i] = array[i + 1]
                array[i + 1] = temp
                # plt.title("Bubble sort")
                line1 = ax.bar(x, array, color="grey", width=1)
                figure.canvas.draw()
                figure.canvas.flush_events()

                # duration = 50
                # time.sleep(0.01)
                # sum = np.sum(sortedarray == array)
                # frequency = 200 + 40 * (sum * 10)
                # winsound.Beep(frequency, duration)
                line1.remove()
                i = i + 1

    totalElapsed = time.time() - t
    plt.title("Bubble sort")
    line1 = ax.bar(x, array, color="grey", width=1)
    figure.canvas.draw()
    # figure.canvas.flush_events()
    plt.show()
    print("Time to complete bubble sort : ", totalElapsed)


def selection_sort():
    size = 50
    array = np.random.randint(1, size, size)
    plt.ion
    sortedarray = []
    sortedarray = np.sort(array)
    x = np.arange(size)
    x1 = np.arange(size)
    figure, (ax, ax_2) = plt.subplots(1, 2)

    line1 = ax.bar(x, array)
    line2 = ax_2.bar(x, array)
    t = time.time()
    plt.title("Bubble sort", fontsize=20)
    line1.remove()
    line2.remove()
    new_array = []
    new_array = np.zeros_like(array)
    test_array = []
    figure.show()

    i = 1
    while not (sortedarray == new_array).all():
        if len(array) != 0 and i > 0:
            x1 = np.arange(size - i)
            max_value = array[np.argmax(array)]
            # temp = new_array[len(new_array) - i]
            # new_array[np.argmax(array)] = temp
            # temp = new_array[len(new_array) - i]
            new_array[len(new_array) - i] = max_value
            # new_array[max_index] = temp
            array = np.delete(array, np.argmax(array), None)

            plt.title("Test sort")
            line1 = ax.bar(x, new_array, color="grey", width=1)
            line2 = ax_2.bar(x1, array, color="grey", width=1)
            figure.canvas.draw()
            figure.canvas.flush_events()

            # duration = 50
            # time.sleep(0.01)
            # sum = np.sum(sortedarray == array)
            # frequency = 200 + 40 * (sum * 10)
            # winsound.Beep(frequency, duration)
            line1.remove()
            line2.remove()
            i = i + 1

    totalElapsed = time.time() - t
    plt.title("Test sort")
    line1 = ax.bar(x, new_array, color="grey", width=1)

    figure.canvas.draw()
    # figure.canvas.flush_events()
    plt.show()
    print("Time to complete selection sort : ", totalElapsed)


selection_sort()
