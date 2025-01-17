import time


def task():
    print("Start of sync task")
    time.sleep(5)
    print("After 5 seconds of sleep")


start = time.time()
for _ in range(3):
    task()
duration = time.time() - start
print(f"\nProcess completed in: {duration} seconds")
"""
Start of sync task
After 5 seconds of sleep
Start of sync task
After 5 seconds of sleep
Start of sync task
After 5 seconds of sleep

Process completed in: 15.014271020889282 seconds
"""
