import tweepy
import time
import atexit
import sys
import random
from random_words import RandomWords
from PyDictionary import PyDictionary
import datetime

print('Hey, SLASH here! A twitter bot.')

CONSUMER_KEY='o80JZbavTzoRllgI0VH4KHtNk'
CONSUMER_SECRET='xmgdggDVg6Y97P2DBZrBVapdVUmXsuiWYugZ0rR17YjyrTI9NI'
ACCESS_KEY='1317182765385699328-0GzU0Un9xhjrPNkYTVaoy5CCsNFwAC'
ACCESS_SECRET='ggdpyLo23rAgzyZQqhbIcUBjiHs7Jqe3WkWHnknqb6coS'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


image='bot.jpg'
''' ---------------------------------------------Backup Code for Status Update-------------------------------------------
def postStatus(update):
    try:
        api.update_status(update)
    except tweepy.TweepError as error:
        if error.api_code == 187:
            # Do something special
            print('Duplicate Message')

postStatus("Hello ,ChatBotSDL is Online Now")
'''
def loadRandomWord():
    dictionary = PyDictionary()
    rw=RandomWords()

    word=rw.random_word()
    definitions = dictionary.meaning(word)

    try:
        part_of_speech = random.choice(list(definitions.keys()))
        definition=random.choice(definitions[part_of_speech])
    except:
        return "NULL DEFINITION"

    return {
        "word":word,
        "definition":definition,
        "part_of_speech":part_of_speech
    }

def tweetDaily():
    while(True):
            word_of_the_day = loadRandomWord()

            while(word_of_the_day == "NULL_DEFINITION"):
                word_of_the_day=loadRandomWord()

            wotd_tweet = word_of_the_day["word"]
            api.update_status(wotd_tweet +'--Word Of The Day , Bot Status - Online')
            break

def tweetOffline():
    while(True):
            word_of_the_day = loadRandomWord()

            while(word_of_the_day == "NULL_DEFINITION"):
                word_of_the_day=loadRandomWord()

            wotd_tweet = word_of_the_day["word"]
            api.update_status(wotd_tweet +'--Word Of The Day , Bot Status - Offline ')
            break

def tweetMorning():
    while(True):
            word_of_the_day = loadRandomWord()

            while(word_of_the_day == "NULL_DEFINITION"):
                word_of_the_day=loadRandomWord()

            wotd_tweet = word_of_the_day["word"]
            api.update_status(wotd_tweet +'Good Morning ! ')
            break


file_name = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return





def reply_to_tweets():
    FOLLOW= True
    message='Hello Sir , Feel Free to Drop your feedbacks to this DM'
    print('retrieving and replying to tweets...', flush=True)
    # NOTE: use 1060651988453654528 for testing.
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(retrieve_last_seen_id(file_name), tweet_mode='extended')
    for mention in reversed(mentions):

        #store_last_seen_id(last_seen_id, file_name)
        if '#hellobot' in mention.full_text.lower() :
            print(str(mention.id) + ' - ' + mention.full_text, flush=True)
            try:
                if '#like' not in mention.full_text.lower() and '#retweet' not in mention.full_text.lower() :
                    print(str(mention.id)+ ' - '+mention.full_text)
                    api.update_status('@' + mention.user.screen_name + '#hellobot Back To You, Auto-Reply Works !', mention.id)
            except tweepy.TweepError as error:
                if error.api_code == 187:
                    # Do something special
                    print('Duplicate Message')
                else:
                    raise error
            try:
                if '#like' in mention.full_text.lower() and '#retweet' not in mention.full_text.lower():
                    try:
                        print(str(mention.id)+ ' - '+mention.full_text)
                        api.update_status('@' + mention.user.screen_name + '#hellobot Back To You, Auto-Reply And Auto-Like Works !', mention.id)
                    except tweepy.TweepError as error:
                        if error.api_code == 187:
                            # Do something special
                            print('Duplicate Message')
                        else:
                            raise error
                    if not mention.favorited:
                        api.create_favorite(mention.id)
                if '#retweet' in mention.full_text.lower() and '#like' not in mention.full_text.lower() :
                    try:
                        print(str(mention.id)+ ' - '+mention.full_text)
                        api.update_status('@' + mention.user.screen_name + '#hellobot Back To You, Auto-Reply And Auto-Retweet Works !', mention.id)
                    except tweepy.TweepError as error:
                        if error.api_code == 187:
                            # Do something special
                            print('Duplicate Message')
                        else:
                            raise error
                    if not mention.retweeted:
                        api.retweet(mention.id)
                if '#retweet' in mention.full_text.lower() and '#like' in mention.full_text.lower() :
                    try:
                        print(str(mention.id)+ ' - '+mention.full_text)
                        api.update_status('@' + mention.user.screen_name + '#hellobot Back To You, Auto-Reply ,Auto-Like And Auto-Retweet Works !', mention.id)
                    except tweepy.TweepError as error:
                        if error.api_code == 187:
                            # Do something special
                            print('Duplicate Message')
                        else:
                            raise error
                    if not mention.retweeted:
                        api.retweet(mention.id)
                    if not mention.favorited:
                        api.create_favorite(mention.id)
                if FOLLOW:
                    if not mention.user.following:
                        mention.user.follow()
                        print('Followed the user')


            except tweepy.TweepError as error:
                if error.api_code == 139:
                        print('Already Liked and Retweeted')
                else:
                    raise error
            try:
                recipient_id=mention.user.id
                direct_message=api.send_direct_message(recipient_id,message)
                print(direct_message.message_create['message_data']['text'])

            except tweepy.TweepError as error:
                        if error.api_code == 349:
                            # Do something special
                            print('User Has Denied Permission')
            store_last_seen_id(mention.id, file_name)


tweetDaily()



while True:
    reply_to_tweets()
    '''
    try:
        sys.exit( tweetOffline() )
        {
            print("Exiting")
        }
    except SystemExit:
        print ('--------------------------------------')
    '''
    time.sleep(15)





































































'''
import tweepy
import time
print('Hey, SLASH here! A twitter bot.')

CONSUMER_KEY='o80JZbavTzoRllgI0VH4KHtNk'
CONSUMER_SECRET='xmgdggDVg6Y97P2DBZrBVapdVUmXsuiWYugZ0rR17YjyrTI9NI'
ACCESS_KEY='1317182765385699328-sbNXraeTxAV8SzHJgRLPGCXJibAUNb'
ACCESS_SECRET='DLmhIqbE5Sh4Y61VNsaq9cmxScDvMydYhntpLOONS61ZO'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

tweets=api.mentions_timeline()
'''
'''
for tweet in tweets:
    if '#hellobot' in tweet.text.lower():
        print(str(tweet.id) + ' - ' + tweet.text)
'''

'''
cd
# NOTE: I put my keys in the keys.py to separate them
# from this main file.
# Please refer to keys_format.py to see the format.
from keys import *

# NOTE: flush=True is just for running this script
# with PythonAnywhere's always-on task.
# More info: https://help.pythonanywhere.com/pages/AlwaysOnTasks/
print('this is my twitter bot', flush=True)
'''
'''
file_name = 'G:\\TE\\twitterbot\\last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return
'''
'''
last_seen_id = retrieve_last_seen_id (FILE_NAME)
mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
for mention in reversed(mentions):
    print(str(mention.id) + ' - ' + mention.full_text)
    last_seen_id = mention.id
    store_last_seen_id( last_seen_id, FILE_NAME)
    if '#hellobot' in mention.text.lower():
            print('found #hellobot!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name + '#hellobot back to you!', mention.id)
'''
'''
def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    # DEV NOTE: use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(file_name)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, file_name)
        if '#hellobot' in mention.full_text.lower():
            print('found #hellobot!', flush=True)
            print('responding back...', flush=True)
            try:
            api.update_status('@' + mention.user.screen_name +
                    '#hellobot Back To You , Auto-Like ,Auto -Retweet and Auto-Reply Works !', mention.id)
            except tweepy.TweepError as error:
            if error.api_code == 187:
                # Do something special
                print('duplicate message')
            else:
                raise error
            api.create_favorite(mention.id)
            api.retweet(mention.id)

#while True:
reply_to_tweets()
    #time.sleep(15)
    
    '''
    
    


    