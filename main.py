"""
    Searches deep inside a directory structure, looking for duplicate file.
    Duplicates aka copies have the same content, but not necessarily the same name.
"""
__author__ = ""
__email__ = ""
__version__ = "1.0"

# noinspection PyUnresolvedReferences
from os.path import getsize, join
from time import time

# noinspection PyUnresolvedReferences
from p1utils import all_files, compare


def search(file_list):
    """Looking for duplicate files in the provided list of files
    :returns a list of lists, where each list contains files with the same content

    Basic search strategy goes like this:
    - until the provided list is empty.
    - remove the 1st item from the provided file_list
    - search for its duplicates in the remaining list and put the item and all its duplicates into a new list
    - if that new list has more than one item (i.e. we did find duplicates) save the list in the list of lists
    As a result we have a list, each item of that list is a list,
    each of those lists contains files that have the same content
    """
    lol = []
    while 0 < len(file_list):

        dups = list(filter(lambda x: compare(file_list[0], x), file_list))

        if len(dups) > 1:
            lol.append(dups)

        # continuously updating file_list so it's not an infinite loop
        file_list = list(filter(lambda x: not compare(file_list[0], x), file_list))

    return lol


def faster_search(file_list):
    """Looking for duplicate files in the provided list of files
    :returns a list of lists, where each list contains files with the same content

    Here's an idea: executing the compare() function seems to take a lot of time.
    Therefore, let's optimize and try to call it a little less often.
    """
    lol = []

    while 0 < len(file_list):

        dups = []
        name = file_list.pop(0)  # Removes the 1st item from the provided file_list

        dups = [name] # Beginning the search for any duplicates in the remaining list

        for i in range(len(file_list) - 1, -1, -1):

            if compare(name, file_list[i]):

                dups.append(file_list.pop(i))
        if len(dups) > 1:
            lol.append(dups)

    return lol


def report(lol):
    """ Prints a report
    :param lol: list of lists (each containing files with equal content)
    :return: None
    Prints a report:
    - longest list, i.e. the files with the most duplicates
    - list where the items require the largest amount or disk-space
    """
    print("== == Duplicate File Finder Report == ==")
    print("The file with most duplicates is:")

    maximum = max(lol, key=lambda x: len(x))

    print(maximum[0])

    rest_max = sorted(maximum[1:])

    print(f"Here are it's {len(rest_max)} copies: ")

    for i in rest_max:
        print(i)
 #************************
 # The following code is now finding the items that take up the largest disk space

    max_size_list = max(lol, key=lambda x : sum(getsize(i) for i in x))

    rest_max_size = sorted(max_size_list[1:])

    max_size = sum([getsize(i) for i in rest_max_size]) # Creates the KB sum of the remaining files in rest_max_size

    print(f"\nThe most disk space ({max_size}) could be recovered, Deleting this files copies:")

    print(max_size_list[0])

    print(f"Here are it's {len(rest_max_size)} copies: ")

    for i in rest_max_size:
        print(i)

if __name__ == '__main__':
    path = join(".", "images")
    # measure how long the search and reporting takes:
    t0 = time()
    report(search(all_files(path)))
    print(f"Complete Runtime: {time() - t0:.2f} seconds")

    print("\n\n .. and now with a faster search implementation:")

    # measure how long the search and reporting takes:
    t0 = time()
    report(faster_search(all_files(path)))
    print(f"Complete Runtime: {time() - t0:.2f} seconds")
