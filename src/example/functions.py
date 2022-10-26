import time
def factorial(n, sleep=False):
    if sleep:
        time.sleep(4)
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)