import tweepy

consumer_key = "X8HkSttEllWxiAdeuHy4Nbmjp"
consumer_secret = "OXanF1kiDyfdrzDJ4r3GqiSVHkGOEGI3SJWBVgpwoXHdYWr7dD"
access_token = "4635341481-ViSyRYLrfB5HZTBLjTuNsL9reACXsbvD31aXMPB"
access_secret = "cvFkC4eTxuO706oznshIwmPpvPJOHfIWYOAhZW7igbp3Y"

auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

tweets = api.search(q='@OdeCarvalho')

for t in tweets:
    print t.created_at, t.text, "\n"