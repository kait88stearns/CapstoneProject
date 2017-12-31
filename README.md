# CapstoneProject

## 1. Scraping

As of right now, scraping.py has a function to scrape lyrics from Genius.com. My function scrape_songs has two inputs:

>> artist: the artist you want to scrape lyrics for, as string with words separated by dashes if more than one word. The first letter of the first name is capitalized, everything else is lower case. (Ex Kendrick Lamar is entered as 'Kendrick-lamar').

>> songs: a list of the names of the songs you want to scrape, all lowercase with words separated with dashes.

>>  Ex: scrape_songs('King-krule', ['logos', 'slush-puppy', 'easy-easy', 'a-slide-in'])


The Output will be a list of strings, each string being the lyrics of a song in the order they were entered into the songs input. 
