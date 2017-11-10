# import necessary libraries 
import os # to access our OS environment variables 
import twitter 
from random import choice

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

# read tweets and create corpus 
def create_corpus(text): 
    corpus = ""
    for s in text: 
        en_text = s.text.encode('utf-8')
        corpus += en_text 

    return corpus 

contents =  create_corpus(statuses_3)
# everything was in unicode
# this lead me to this article 
# http://www.pgbovine.net/unicode-python.htm

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


# chains = make_chains(contents)


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


# print make_text(chains) 
# # tweet it 