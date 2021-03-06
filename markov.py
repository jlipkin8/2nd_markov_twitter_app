# import necessary libraries 
import os # to access our OS environment variables 
import twitter 
from random import choice
import sys

#use os.environ to get environmental variables 
# run source secrets.sh before running this file 

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'], 
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'], 
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']
)

# This will print info about credentials to make sure they're correct 
# print api.VerifyCredentials()

statuses_1 = api.GetUserTimeline(None,"WebMD")
statuses_2 = api.GetUserTimeline(None, "epicurious")
statuses_3 = api.GetSearch(term="cheese", lang="en")
statuses_4 = api.GetSearch(term="foodies", lang="en")
statuses_5 = api.GetSearch(term="silly", lang="en")

# read tweets and create corpus 
def create_corpus(text): 
    corpus = ""
    for s in text: 
        en_text = s.text.encode('utf-8')
        corpus += en_text 

    return corpus 

def extract_entities(results): 
    entities = []
    for result in results: 
        if result.entities: 
            entities.append(result.entities)

    return entities


# contents =  create_corpus(statuses_3)
# contents_2 = create_corpus(statuses_4)
# contents_3 = create_corpus(statuses_5)
# everything was in unicode
# this lead me to this article 
# http://www.pgbovine.net/unicode-python.htm

# combine all contents 
# all_contents = contents + contents_2 + contents_3


def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


files = sys.argv[1:]

contents = open_and_read_file(files)

# make_chains 
def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


# chains = make_chains(all_contents)


# make text
def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    key = choice(chains.keys())
    words = [key[0], key[1]]
    char_count = 0
    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text)
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.

        word = choice(chains[key])
        char_count += len(word)
        if char_count > 100:
            break
        words.append(word)
        key = (key[1], word)

    return " ".join(words)


# The Project Gutenberg EBook of Hints on cheese-making, by Thomas Day Curtis
# print make_text(chains) 
# # tweet it 