# Word Suggestion
A primitive autocorrect mechanism. Reads a list of words and frequencies from a CSV, and uses that to suggest the 5 most likely corrections for misspelled words

## Example 

### Content of dictionary.csv 
```
Hello, 300
World, 50
Hi, 600
How, 500
Are, 900
You, 200
```

### Command
```python ./word_suggestion.py dict.csv hellp```

### Output
```hello, hi, how, world, are```

## Running
Use chmod to make the file executable and run `./word_suggestion.py [dictionaryname.csv] [misspelled word]`
Alternatively, don't use chmod and instead run `python3 ./word_suggestion.py [dictionaryname.csv] [misspelled word]`



## Notes
Uses the external python-Levenshtein library:  https://pypi.org/project/python-Levenshtein/
<br>

## Adjusting the weights of both parameters
There is an optional command-line parameter Levenshtein_weighting. This parameter should be the third and final arg if supplied.
It accepts a float in between -1 and 1. <br><br>

In general, giving both Levenshtein distance and frequency equal weight leads to results which conflict with common sense.
Increasing this parameter increases the significance of the Levenshtein distance in the total score, and thus leads to words with lower levenshtein distance being higher ranked in general. <br>
0 means to weight both frequency and Levenshtein distance equally. 1 means to ignore frequency, and -1 means to ignore Levenshtein distance.<br><br>

If the results given seem strange, the parameter can be adjusted as an optional command-line argument. For instance
```./word_suggestion.py dict.csv hellp 0 ``` <br>
It defaults to 0.42 partly because that yielded results most in line with common sense, and partly because 42 is the answer to life, the universe, and everything.

