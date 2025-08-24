import random

for i in range(10):
    number = random.randrange(0, 101) / 100
    epsilon = 0.1
    print(number, epsilon)
    if number <= epsilon:
        print("True")
    else:
        print("False")

