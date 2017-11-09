# import necessary libraries 
import os # to access our OS environment variables 
import twitter 

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

# followers = api.GetFollowers()

# for follower in followers: 
#     print "Name: ", follower.name
#     print "Number of Friends: ", follower.friends_count
#     if follower.geo_enabled: 
#         print follower.location


statuses_1 = api.GetUserTimeline(None,"WebMD")
statuses_2 = api.GetUserTimeline(None, "epicurious")

# read tweets and create corpus 
def create_corpus(text, text_2): 
    corpus = ""
    for s in text: 
        corpus += s.text 

    for s in text_2: 
        corpus += s.text 

    return corpus 


print create_corpus(statuses_1, statuses_2)
# make_chains 

# make text

# tweet it 