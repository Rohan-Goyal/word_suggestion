#!/usr/bin/env python3
# Tested on Anaconda Python 3.7.3 on Manjaro Linux
"""
Goal: Given a list of words (say dictionary) in a csv file along with its frequency. 
Take a word as input and suggest five closest words from the dictionary sorted in order of relevance.
Assume that the user is trying to type a dictionary word which they misspelled, and you have to suggest the correct word. `
Language: Any
Example Input file:
Content of dictionary.csv
Hello, 300
World, 50
Hi, 600
How, 500
Are, 900
You, 200
Expected CLI Input:
> ./executable dictionary.csv hellp
Hello, word2, word3, word4, word5
"""

from sys import argv
from csv import reader
from Levenshtein import distance

# Using the python-Levenshtein library for efficiency and convenience.
# It's written in C, providing significant performance improvements.
# Credit: https://pypi.org/project/python-Levenshtein/


def csv_to_matrix(filename):
    """Simple utility to load a CSV and convert it into an array of arrays

    :param filename: Name of csv file to load
    :returns: Matrix representation of CSV
    :rtype: Array of arrays

    """
    with open(filename, newline="") as csvfile:
        return [row for row in reader(csvfile)]


def clean_dict(matrix):
    """Converts the dictionary matrix to an easier to process format, and casts all frequencies to integers

    :param matrix: The dictionary matrix to clean up
    :returns: A modified, easier-to-process version of that same matrix
    :rtype: Array of arrays
    NOTE: Only works on a specific format of matrix, based on the CSV format specified in the example
    """

    for row in matrix:
        row[0] = row[0].lower().strip()
        row[1] = int(row[1].strip())
    return matrix


dictionary = clean_dict(csv_to_matrix(argv[1]))
inputword = argv[2].lower()
lev_weight_param = float(argv[3].strip()) if len(argv) > 3 else 0.42
# Variables introduced globally, to make it easier to handle parameters
# Lev_weighting decides how much to weight the levenshtein distance when scoring possibilities. 
# Explained more thoroughly in README and in line 89


def scale_freq(freq):
    """Scales the frequency of a given word to between 0 and 1 based on the sum of all frequencies in the dictionary.
    Effectively, it returns the frequency of that word as a fraction of the size of the corpus

    :param freq: The number we want to scale
    :param freq_range: As calculated above, the maxima and minima with which to scale
    :returns: The normalised frequency of a given word in the dictionary
    :rtype: Float, between 0 and 1 inclusive

    """
    return freq / sum([word[1] for word in dictionary])


def total_score(inputword, dictword, lev_weighting=lev_weight_param):
    """Given an input and a dictionary word, it returns a rough estimate of the "likelihood" that that was the intended word.
    Doesn't reflect actual probability, but the ranking system is valid.

    :param inputword: The incorrect word input via cli, which we want to find a match for
    :param dictword: An array, first element being a word/string and the second an integer representing its frequency
    :param lev_weighting: If you want the score to weight the Levenshtein distance higher or lower. Defaults to 0.42. 
    Setting it to 1 means to disregard the frequency completely, and setting it to -1 means to disregard Lev distance completely
    
    :returns: The total, weighted "likelihood" that the given dictionary word was intended
    :rtype: A float between -1 and 1, inclusive

    """
    lev = distance(inputword, dictword[0])
    lev_scaled = lev / len(inputword)
    freq = scale_freq(dictword[1])
    weighted_lev = (1 + lev_weighting) * lev_scaled
    weighted_freq = (1 - lev_weighting) * freq
    return weighted_freq - weighted_lev


# Lev distance is negative, as we want to minimise it
"""
A note on the lev_weighting parameter:
In general, giving both Levenshtein distance and frequency equal weight leads to results which conflict with common sense. 
To solve that, I introduced a parameter lev_weighting above.

It basically increases the significance of the Levenshtein distance in the total score, 
and thus leads to words with lower levenshtein distance being higher ranked in general.

If the results given seem strange, the parameter can be adjusted as an optional command-line argument.
Eg: ./word_suggestion.py dict.csv hellp 0

It defaults to 0.42 partly because that yielded results most in line with common sense, 
and partly because 42 is the answer to life, the universe, and everything.
"""


def ranking(inputword, dictionary):
    """Given an input word, ranks every word in the dictionary by likelihood that that was the intended word 
    (a function of the frequency and levenshtein distance)

    :param inputword: input via CLI
    :param dictionary: The dictionary of words and freqs to compare this to.
    :returns: List of tuples. Each tuple contains a word/string and a score between -1 and 1.
    :rtype: List of tuples. Each tuple contains a string and a float

    """
    score_array = [(word[0], total_score(inputword, word))
                   for word in dictionary]
    # Generates a list of tuples.
    # Each tuple has the word itself as the first element, and its total score as the second

    return sorted(score_array, key=lambda elem: elem[1], reverse=True)[:5]
    # Sorting by total score, from max to min and taking only the first 5 elems


if __name__ == "__main__":
    ranks = ranking(inputword, dictionary)
    print(", ".join([r[0] for r in ranks]))
