#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 25 19:25:59 2018

Modifications by thebooort

@author: Mik
"""
import csv 
import time 

import tweepy

# Copy the api key, the api secret, the access token and the access token secret from the relevant page on your Twitter app 

api_key = '--'
api_secret = '--'
access_token = '--'
access_token_secret = '--'

# You don't need to make any changes below here # This bit authorises you to ask for information from Twitter 
auth = tweepy.OAuthHandler(api_key, api_secret) 
auth.set_access_token(access_token, access_token_secret) 
# The api object gives you access to all of the http calls that Twitter accepts 
api = tweepy.API(auth) 

#User we want to use as initial node 
user='sevaseviene'


#This creates a csv file and defines that each new entry will be in a new line 
csvfile=open(user+'_twitter_network.csv', 'w') 
spamwriter = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL) 

#This is the function that takes a node (user) and looks for all its followers #and print them into a CSV file... and look for the followers of each follower... 
def fib(n,user,spamwriter):
    if n>0:
        #There is a limit to the traffic you can have with the API, so you need to wait 
        #a few seconds per call or after a few calls it will restrict your traffic 
        #for 15 minutes. This parameter can be tweeked 
        time.sleep(40) 
        
        #This is for private users whose followers we won't be able to see
        try:
            users=tweepy.Cursor(api.followers, screen_name = user, wait_on_rate_limit = True).items()
            for follower in users:
                print(follower.screen_name)
                spamwriter.writerow([user+';'+follower.screen_name]) 
                fib(n-1,follower.screen_name,spamwriter) 
                #n defines the level of autorecurrence

        except tweepy.TweepError:
                print("Failed to run the command on that user, Skipping...")
                
            

n=2
fib(n,user,spamwriter)
