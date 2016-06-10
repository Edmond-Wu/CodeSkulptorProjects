"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    answer = []
    for item in list1:
        if item not in answer:
            answer.append(item)
    return answer

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    list1_index = 0
    list2_index = 0
    intersection = []
    while list1_index < len(list1) and list2_index < len(list2):
        if list1[list1_index] < list2[list2_index]:
            list1_index += 1
        elif list1[list1_index] > list2[list2_index]:
            list2_index += 1
        else:
            intersection.append(list1[list1_index])
            list1_index += 1
            list2_index += 1
    return intersection
        

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    list1_index = 0
    list2_index = 0
    merged = []
    while list1_index < len(list1) and list2_index < len(list2):
        if list1[list1_index] < list2[list2_index]:
            merged.append(list1[list1_index])
            list1_index += 1
        elif list1[list1_index] > list2[list2_index]:
            merged.append(list2[list2_index])
            list2_index += 1
        else:
            merged.append(list1[list1_index])
            merged.append(list2[list2_index])
            list1_index += 1
            list2_index += 1
    if list1_index == len(list1):
        while list2_index < len(list2):
            merged.append(list2[list2_index])
            list2_index += 1
    if list2_index == len(list2):
        while list1_index < len(list1):
            merged.append(list1[list1_index])
            list1_index += 1
    return merged
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    middle = len(list1)/2
    first_half = list1[:middle]
    second_half = list1[middle:]
    first_half = merge_sort(first_half)
    second_half = merge_sort(second_half)
    return merge(first_half, second_half)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [""]
    elif len(word) == 1:
        return ["", word]
    first_char = word[0]
    rest = word[1:]
    rest_strings = gen_all_strings(rest)
    new_list = []
    for string in rest_strings:
        for index in range(len(string) + 1):
            left_slice = string[0:index]
            right_slice = string[index:len(string)]
            new_string = left_slice + first_char + right_slice
            new_list.append(new_string)
            
    return rest_strings + new_list

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    result = []
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    data = netfile.readlines()
    for line in data:
        result.append(line[:-1])
    return result

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()
