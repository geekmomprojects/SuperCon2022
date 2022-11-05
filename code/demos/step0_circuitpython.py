'''
This step is to demonstrate serial output from your
CircuitPython program.
'''
import time

print("Testing 1... 2... 3...")
count = 0
while(True):
    print("Counting ", count)
    count = count + 1
    time.sleep(0.5)
