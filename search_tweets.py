import tweepy
import code
import json
# The actual authentication
from oauth_handler import auth

N_TWEETS = 1000

def setup_search_query(auth=auth):
    """
    Using auth to setup a search object.
    Needs to be placed within the Cursor to be used later

    auth: authentication of Tweepy. default imported from oauth_handler
    """
    return tweepy.API(auth).search

def search_twitter(search_object, q, n_items=N_TWEETS, **kwargs):
    """
    Returns an actual search in a list of the json object in every tweet
    search_object: API search object


    q: String query
    n_items: Number of items returned. Integer
    kwargs: Additional arguments to be sent into the API.search() method.
    """

    search = tweepy.Cursor(search_object, q, **kwargs)
    # Returns the json object inside each search term
    return [item._json for item in search.items(N_TWEETS)]


def extract_tweet_parameter(tweet_list, parameter):
    """
    Extracts certain objects from the list of tweets generated from search_twitter
    Keeps id of tweet to have unique identification

    tweet_list: List of json objects from search_twitter(). List
    parameter: Parameter from each json object to be extracted. String
    """

    return [{'id': tweet['id'], parameter:tweet[parameter]} for tweet in tweet_list]


def get_parent_of_replies(tweet_list, append=True, auth=auth):
    """
    Fetches the parent tweet if the original is a reply to something.
    Has the option to append to the existing list of tweets if relevant
    tweet_list: List of tweets.
    append: Boolean. Determines if returns a separate list or appends to an existing list
    auth: Authenticated Tweepy object
    """
    twitter_search = tweepy.API(auth)
    reply_list = []
    for tweet in tweet_list:

        try:
            reply_id = tweet['in_reply_to_status_id']

            try:
                reply_object = twitter_search.get_status(reply_id)._json
                reply_list.append(reply_object)
            except tweepy.error.TweepError:
                pass

        except KeyError:
            pass

    if append:
        tweet_list += reply_list
        return tweet_list
    else:
        return reply_list







def search_and_store():
    api_search = setup_search_query()
    tweets = search_twitter(api_search, "#GC2020")

    return tweets
    

if __name__ == "__main__":

    tweets = search_and_store()
    # Dumping to a json object
    with open('tweets.json', 'w') as f:
        json.dump(tweets, f, indent=4, separators=(',',':'))
