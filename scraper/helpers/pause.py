'''
This module provides a function that pauses the program execution for a random amount of time, 
which is useful for loading things from a web page.
'''
# Python
import random
import time


def pause():
    '''Pause to load things from the page'''

    random_sleep = random.uniform(0.5, 1.4)
    time.sleep(random_sleep)
