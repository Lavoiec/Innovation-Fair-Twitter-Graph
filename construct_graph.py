from search_tweets import search_and_store
from random import randint
import json

"""
Designing a JSON file to largely fit the mould of the Force Directed Graph Demo from the D3 Gallery.
Found here: https://bl.ocks.org/mbostock/4062045
Current Schema:

Nodes {
    id: Tweet id
    text: Tweet text
    size: Weighted Average of Favourites, Retweets and Quotes
}

Links: {
    Source: Tweet id
    Target: id of Tweet that it retweeted
}

"""
# Alter 
def import_tweets(reload=False):
    """
    Function to import tweets, either from a json file or from CyberSpace

    reload: Boolean indicator of whether we reload the data (from CyberSpace) or import from JSON 
    """
    if not reload:
        with open('tweets.json', 'r') as f:
            tweets = json.load(f)

        return tweets
    
    return search_and_store()


class TwitterGraph():
    """
    Creating an object that will contain the network graph the be generated.
    Takes on a list of JSON objects as its data attribute.
    """

    def __init__(self, tweet_list):
        self.data = tweet_list


    def get_nodes(self):
        """
        Creates an object for each unique tweet, and adds them into one list.

        No real parameters since we are just using the data stored in the init
        """
        node_data = []
        tweet_list = self.data

        for tweet in tweet_list:
            # Constructs the object
            node_object = {
                'id': tweet['id'],
                'text': tweet['text'],
                'size':tweet['retweet_count']
                  }
            # If tweet is unique
            if node_object not in node_data:
                node_data.append(node_object)

        self.nodes = node_data


        node_list = []
        for node in self.nodes:
            node_list.append(node['id'])

        self.node_list = node_list


    def get_links(self, method):

        """
        method: Either "reply" or "retweet". Determines how the tweets will link with each other.
        """
        
        tweet_list = self.data
        link_data = []
        for tweet in tweet_list:
            
            try:
                if method == "retweet":
                    # Retweeted_status gives the original tweet
                    # that the tweet is retweeting as its original object
                    # Therefore we dig a level deeper to get the id of the
                    # retweeted tweet
                    if tweet['retweeted_status']['id'] in self.node_list:

                        link_object = {
                            'source': tweet['id'],
                            'target': tweet['retweeted_status']['id'],
                            'value': 1
                            }

                        link_data.append(link_object)

                elif method == "reply":
                    # The id of the tweet it replies to is stored as a parameter
                    # Easy to fetch.
                    if tweet['in_reply_to_status_id'] in self.node_list:

                        link_object = {
                            'source': tweet['id'],
                            'target': tweet['in_reply_to_status_id'],
                            'value': 1
                        }

                        link_data.append(link_object)

            except KeyError:
                pass

        self.links = link_data

    
    def export_to_json(self):
        """
        Exports the nodes and links parameters as a JSON object to mirror the
        "miserables.json" dataset used in the example.
        """

        json_object = {
            "nodes": self.nodes,
            "links": self.links
        }

        with open('twitter_graph.json', 'w') as f:
            json.dump(json_object, f, indent=4, separators=(',',':'))


        



        

tweets = import_tweets()

graph = TwitterGraph(tweets)

graph.get_nodes()

graph.get_links(method="retweet")

graph.export_to_json()
