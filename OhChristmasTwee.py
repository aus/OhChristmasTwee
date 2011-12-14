#! /usr/bin/env python

import datetime
import serial
import re
import time
import random
import urllib2
import tweetstream 
import tweepy 

# Path to Serial
SERIAL_PORT = '/dev/tty.usb'

# Twitter Sream
TW_USERNAME  = 'XXXXXX'
TW_PASSWORD  = 'XXXXXX'

# Twitter Bot
ENABLE_TWITTER_BOT  = 1 
CONSUMER_KEY        = 'XXXXXX'
CONSUMER_SECRET     = 'XXXXXX'
ACCESS_KEY          = 'XXXXXX'
ACCESS_SECRET       = 'XXXXXX'
TWEET_URL           = 'http://google.com'
TWEETS              = ['Hey @%s! Jingle bell time is a swell time to be %s. %s',
                       '@%s changed my color. Holiday cheer also comes in %s. %s',
                       "Hey @%s! What color is Christmas Spirit? It's %s. %s",
                       'Buddy, the Elf. Whats your favorite color? @%s says %s. %s',
                       '@%s sings, "Oh Christmas Twee. Oh Christmas Twee. Your branches %s delight us! %s',
                       '@%s reads, "Twas the night before Christmas. Lights %s, shining a bright! %s',
                       'On the 1st day of Christmas, my true love @%s gave to me, %s in my Christmas Tree. %s',
                       '@%s sings, "Rudolph the %s nosed, Reindeer." %s',
                       '@%s makes my color %s. Pa rum pum pum pum. %s',
                       '@%s is dreaming of a %s Christmas. %s',
		       'Grandma and @%s got ran over by %s reindeer. %s',
                       'Oh Holy Night, @%s! The stars are brightly %s. %s',
		       '@%s decked the halls with boughs of %s. Fa la la la la, la la la la. %s']

# NOTE: Modifying these values can get you out of sync of the cheer light network.         
# if(modified): CHRISTMAS_SPIRIT = 0                 

HASHTAGS = ['cheerlights']
TRANSITION_DELAY = 1                # Seconds between multiple colors. Still needs to be standardized?
COLOR_SET = set(['red', 
                 'green', 
                 'blue', 
                 'white', 
                 'black', 
                 'cyan', 
                 'magenta', 
                 'yellow', 
                 'purple', 
                 'warmwhite', 
                 'orange'])

# DO NOT MODIFY AFTER THIS LINE.
# WARNING: CRAPPY UNDOCUMENTED CODE AHEAD. PROCEED AT YOUR OWN RISK!

def send_cmds(serial_out):
    print '*** Sending commands to serial...'
    for item in serial_out:
        try:
            ser.write(str(item))
            print '*** Serial: ' + item
            time.sleep(TRANSITION_DELAY)
        except:
            print '*** Error sending serial command!'
    return

def format_colors(color_list):
    color_list = list(set(color_list)) # remove duplicate colors
    color_string = ''
    if (len(color_list) > 4):
        return 'M-M-MMULTI COLOR!!'
    else:
        for item in color_list:
            if (item != color_list[-1]):
	        color_string += item
                color_string += ', '
	    else:
	        if (len(color_list) > 1):
	            color_string += 'and ' + item
	        else:
	            color_string = item
    return color_string

def tweet_it(colors, user):
    msg  = random.choice(TWEETS) %(user, format_colors(colors), TWEET_URL)
    try:
        print "*** Tweeting... \n" 
        api.update_status(msg)
        print "-----" * 4
        print TW_USERNAME + " tweeeted: \n"
        print msg
        print "-----" * 4
    except:
        print '*** Error sending tweet!'
    return

try:
    print '*** Initializing serial...'
    ser = serial.Serial(SERIAL_PORT, 9600)
    print '*** Serial connected!'
    print '*** Serial testing...'
    time.sleep(2)
    send_cmds(['red','green','blue'])
except:
    print '*** Error initializing serial to ' + SERIAL_PORT + '! Check SERIAL_PORT'

print '*** Getting last color from ThingSpeak...'
send_cmds([urllib2.urlopen("http://api.thingspeak.com/channels/1417/field/1/last.txt").read()])

if(ENABLE_TWITTER_BOT):
    try:
        print '*** Authenticating Twitter bot...'
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)
        print '*** Authorized!'
    except:
        print '*** Error authenticating Twitter bot. Check OAuth settings!'

try:
    print '*** Connecting to Twitter stream...' 
    stream = tweetstream.FilterStream(TW_USERNAME, TW_PASSWORD, track=HASHTAGS)
    print '*** Connected!'
    print '*** Waiting for tweets matching hashtags...'
except:
    print '*** Twitter stream failed. :('

try:
    for tweet in stream:
        print "-----" * 4
	print datetime.datetime.now()
        print "New tweet from: " + tweet['user']['screen_name'] + "\n"
        print tweet['text']
        print "-----" * 4
        words = re.findall(r'\w+', tweet['text'].lower())
        cmds = [word for word in words if word in COLOR_SET]
        if (cmds):
            print '*** New color command(s) found!'
            send_cmds(cmds)
            if (ENABLE_TWITTER_BOT):
            	if(tweet['user']['screen_name'] != TW_USERNAME):   # Do not @reply self
                    tweet_it(cmds, tweet['user']['screen_name'])
        else:
            print '*** No color commands found.'
except KeyboardInterrupt:
    print '\n *** Goodbye!'

