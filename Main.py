import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import random

def standard(num1, num2):
    result = 0
    ten_multiplier = 1

    # convert the inputs to strings and reverse them
    num1 = str(num1)[::-1]
    num2 = str(num2)[::-1]

    for i in range(len(num1)):
        temp_res = 0
        carry = 0
        for j in range(len(num2)):
            # multiply each digit and add carry from the previous operation
            val = int(num1[i]) * int(num2[j]) + carry
            digit = val % 10
            carry = val // 10

            # shift the result to the left by j places
            temp_res += digit * (10 ** j)

        # if there is a remaining carry, add it to the result
        if carry > 0:
            temp_res += carry * (10 ** len(num2))

        # shift the result to the left by i places and add to the total result
        result += temp_res * (10 ** i)

    return int(result)  # convert the result back to integer before returning it


def karatsuba(x, y):
    # base case:
    # when one number only has one digit
    if x < 10 or y < 10:
        return x * y

    else:
        # calculate the size of the numbers
        n = max(len(str(x)), len(str(y)))
        half = n // 2

        a = x // (10 ** (half))  # left part of x
        b = x % (10 ** (half))  # right part of x
        c = y // (10 ** (half))  # left part of y
        d = y % (10 ** (half))  # right part of y

        ac = karatsuba(a, c)
        bd = karatsuba(b, d)
        ad_plus_bc = karatsuba(a + b, c + d, ) - ac - bd
        return ac * (10 ** (2 * half)) + (ad_plus_bc * (10 ** half)) + bd


def divide_and_conquer(x, y):
    # base case:
    # when one number only has one digit
    if x < 10 or y < 10:
        return x * y

    else:
        n = max(len(str(x)), len(str(y)))
        half = n // 2

        a = x // (10 ** half)  # left part of x
        b = x % (10 ** half)  # right part of x
        c = y // (10 ** half)  # left part of y
        d = y % (10 ** half)  # right part of y

        # Recursively compute the four products
        ac = divide_and_conquer(a, c)
        ad = divide_and_conquer(a, d)
        bc = divide_and_conquer(b, c)
        bd = divide_and_conquer(b, d)

        # Combine the results
        return (ac * 10 ** (2 * half)) + ((ad + bc) * 10 ** half) + bd


def compare():
    num_tests = int(num_tests_entry.get())
    base = 10

    x_values = []  # Sizes of the inputs
    times_standard = []  # Times for standard method
    times_karatsuba = []  # Times for Karatsuba method
    times_divide_and_conquer = []  # Times for Divide and Conquer method

    for i in range(1, num_tests + 1):
        x = random.randint(base ** i, base ** (i + 1) - 1)
        y = random.randint(base ** i, base ** (i + 1) - 1)

        size = max(len(str(x)), len(str(y)))  # Size of the inputs
        x_values.append(size)

        # Measure the start time for standard
        start_time = time.time()
        result_standard = standard(x, y)
        elapsed_time_standard = time.time() - start_time
        times_standard.append(elapsed_time_standard)

        print(
            f"For {x} * {y}, the result is {result_standard} and standard multiplication took {elapsed_time_standard} seconds.")

        # Measure the start time for Karatsuba
        start_time = time.time()
        result_karatsuba = karatsuba(x, y)
        elapsed_time_karatsuba = time.time() - start_time
        times_karatsuba.append(elapsed_time_karatsuba)

        print(
            f"For {x} * {y}, the result is {result_karatsuba} and karatsuba multiplication took {elapsed_time_karatsuba} seconds.")

        # Measure the start time for Divide and Conquer
        start_time = time.time()
        result_divide_and_conquer = divide_and_conquer(x, y)
        elapsed_time_divide_and_conquer = time.time() - start_time
        times_divide_and_conquer.append(elapsed_time_divide_and_conquer)

        print(
            f"For {x} * {y}, the result is {result_divide_and_conquer} and divide_and_conquer multiplication took {elapsed_time_divide_and_conquer} seconds.")
        print()

    # Create the plot
    fig = plt.Figure(figsize=(10, 6))
    a = fig.add_subplot(111)
    a.plot(x_values, times_standard, label='Standard')
    a.plot(x_values, times_karatsuba, label='Karatsuba')
    a.plot(x_values, times_divide_and_conquer, label='Divide and Conquer')
    a.set_xlabel('Size of input')
    a.set_ylabel('Time taken (seconds)')
    a.set_title('Time complexity of multiplication methods')
    a.legend()

    # Display the plot in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

root = tk.Tk()
root.title('Multiplication methods comparison')

# Create a Label and an Entry for user to enter the number of tests
num_tests_label = tk.Label(root, text='Enter number of tests:')
num_tests_label.pack()
num_tests_entry = tk.Entry(root)
num_tests_entry.pack()

# Create a button to run the comparison
compare_button = tk.Button(root, text='Compare methods', command=compare)
compare_button.pack()

root.mainloop()