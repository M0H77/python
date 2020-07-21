"""
author: Mohammed Alhamadah
description: CSEC 201 lab1 part2
purpose: solving The Dining Philosophers problem
"""
import threading

forks_lst = []
philosopher_lst = []
forks = 10
philosophers = 100000


def create_lock(n):
    """
    create the lock objects
    """
    for fork in range(n):
        fork = threading.Lock()
        forks_lst.append(fork)


def create_philosophers(n):
    """
    create the philosophers threads
    """
    for i in range(n):
        philosopher_thread = threading.Thread(target=eat, args=(i, forks_lst[i % forks], (forks_lst[(i + 1) % forks])))
        philosopher_lst.append(philosopher_thread)


def eat(id, fork1, fork2):
    """
    allow philosophers threads to eat when they have 2 forks. check every
    time if the fork is blocked to avoid deadlock.
    """
    while True:
        print(f"philosopher {id} has one fork")
        fork2.acquire()
        locked = fork1.acquire(False)

        if locked:
            print(f"philosopher {id} has two forks")
            print(f"philosopher {id} is eating")
            fork2.release()
            fork1.release()
            print(f"philosopher {id} is done eating")
            print()
            break
        else:
            fork2.release()
            print(f"philosopher {id} put down the fork")


def main():
    create_lock(forks)
    create_philosophers(philosophers)

    for philosopher_thread in philosopher_lst:
       philosopher_thread.start()

    for philosopher_thread in philosopher_lst:
        philosopher_thread.join()

main()


