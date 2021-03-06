# -*- coding: utf-8 -*-
"""Sentiment_Analysis_for_twitter_.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G0dmhOYe7LL_XA9XNEuBSRPlVMDoBYim
"""

import csv
import re
import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt


def remove_special_character(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())


def calculate_per(n, m):
    x = 100 * float(n) / float(m)
    return format(x, '.4f')

consumerKey = 'aSafntYhEHz5dIUmDPpgLsocU'
consumerSecret = 'YH35fdPUXokY1kTKGTxXn7l1kReFFEhcyzWRiNg9saGCuEgdy8'
accessToken = '877054901511221249-hMDVxVskAr4hhBRwKcq8FVamiccDm7O'
accessTokenSecret = 'uTSLF5yvY3ITpHVjy4xOMOhc68vYB2zbkM25a2mza76Gn'
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)
tweets = []
tweetText = []
searchTerm = input("Enter Keyword/Tag to search about: ")
NoOfTerms = int(input("Enter how many tweets to search: "))
tweets = tweepy.Cursor(api.search, q=searchTerm, lang="en").items(NoOfTerms)
csvFile = open('result.csv', 'a')
csvWriter = csv.writer(csvFile)
polarity = 0
positive = 0
wpositive = 0
spositive = 0
negative = 0
wnegative = 0
snegative = 0
neutral = 0
for tweet in tweets:
    # Append to temp so that we can store in csv later. I use encode UTF-8
    tweetText.append(remove_special_character(tweet.text).encode('utf-8'))
    # print (tweet.text.translate(non_bmp_map))    #print tweet's text
    analysis = TextBlob(tweet.text)
    # print(analysis.sentiment)  # print tweet's polarity
    polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

    if analysis.sentiment.polarity == 0:  # adding reaction of how people are reacting to find average later
        neutral += 1
    elif 0 < analysis.sentiment.polarity <= 0.3:
        wpositive += 1
    elif 0.3 < analysis.sentiment.polarity <= 0.6:
        positive += 1
    elif 0.6 < analysis.sentiment.polarity <= 1:
        spositive += 1
    elif -0.3 < analysis.sentiment.polarity <= 0:
        wnegative += 1
    elif -0.6 < analysis.sentiment.polarity <= -0.3:
        negative += 1
    elif -1 < analysis.sentiment.polarity <= -0.6:
        snegative += 1

# Write to csv and close csv file
csvWriter.writerow(tweetText)
csvFile.close()

# finding average of how people are reacting
positive = calculate_per(positive, NoOfTerms)
wpositive = calculate_per(wpositive, NoOfTerms)
spositive = calculate_per(spositive, NoOfTerms)
negative = calculate_per(negative, NoOfTerms)
wnegative = calculate_per(wnegative, NoOfTerms)
snegative = calculate_per(snegative, NoOfTerms)
neutral = calculate_per(neutral, NoOfTerms)

# finding average reaction
polarity = polarity / NoOfTerms

# printing out data
print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
print()
print("General Report: ")

if polarity == 0:
    print("Neutral")
elif 0 < polarity <= 0.3:
    print("Weakly Positive")
elif 0.3 < polarity <= 0.6:
    print("Positive")
elif 0.6 < polarity <= 1:
    print("Strongly Positive")
elif -0.3 < polarity <= 0:
    print("Weakly Negative")
elif -0.6 < polarity <= -0.3:
    print("Negative")
elif -1 < polarity <= -0.6:
    print("Strongly Negative")

print()
print("Detailed Report: ")
print(str(positive) + "% people thought it was positive")
print(str(wpositive) + "% people thought it was weakly positive")
print(str(spositive) + "% people thought it was strongly positive")
print(str(negative) + "% people thought it was negative")
print(str(wnegative) + "% people thought it was weakly negative")
print(str(snegative) + "% people thought it was strongly negative")
print(str(neutral) + "% people thought it was neutral")