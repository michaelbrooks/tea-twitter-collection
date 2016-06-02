
import tweepy
import json
from datetime import datetime, timedelta
import time
import traceback
import sys
import os
import io

import first_last

def log(s):
    print >> sys.stderr, "%s > %s" % (datetime.now().isoformat(), s)

def limit_handled(cursor):

    def rate_limit_sleep():
        log("Rate limit reached. Sleeping for 5 minutes.")
        time.sleep(5 * 60)
        log("Continuing...")

    def unknown_sleep(e):
        log(e)
        traceback.print_exc()
        log("Unexpected error. Sleeping for 1 minute.")
        time.sleep(60)
        log("Continuing...")

    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            rate_limit_sleep()
        except tweepy.TweepError, e:
            if e.response.status_code == 429:
                rate_limit_sleep()
            else:
                log("Unknown TweepError: %s" % e.response.text)
                unknown_sleep(e)
        except StopIteration:
            log('No more tweets matching query')
            raise StopIteration
        except Exception, e:
            unknown_sleep(e)

def connect():
    import twitter_keys

    auth = tweepy.OAuthHandler(twitter_keys.CONSUMER_KEY, twitter_keys.CONSUMER_SECRET)
    auth.set_access_token(twitter_keys.ACCESS_KEY, twitter_keys.ACCESS_TOKEN)

    return tweepy.API(auth)

def get_cursor(api, query_file):

    query = dict(
        count=100,
        result_type='recent'
    )

    log("Reading query params from %s" % query_file)
    with open(query_file, 'r') as fp:
        query.update(json.loads(fp.read()))

    log("Query params: %s" % json.dumps(query, indent=3))
    return tweepy.Cursor(api.search, **query)

def get_output_file(query_file):
    query_file = os.path.splitext(query_file)[0]
    return "%s.raw.json" % query_file

def print_progress(total, tweet):
    try:
        log("Total: %d \tLast ID: %s \tLast Date: %s \tText: '%s'" % (received, tweet.id, tweet.created_at, tweet.text))
    except UnicodeEncodeError:
        pass

query_file = sys.argv[1]
output_filename = get_output_file(query_file)
log("Writing to %s" % output_filename)

api = connect()
cursor = get_cursor(api, query_file)
try:
    with io.open(output_filename, 'w', encoding='utf-8') as outfile:
        received = 0
        for tweet in limit_handled(cursor.items()):
            received += 1
            if received % 1000 == 0:
                print_progress(received, tweet)

            outfile.write(unicode(json.dumps(tweet._json)))
            outfile.write(u'\n')
            outfile.flush()
finally:
    print_progress(received, tweet)

    log("Word count:")
    from subprocess import check_output
    log(check_output(['wc', output_filename]))

    log("First/last tweets:")
    first_last.summary(output_filename, sys.stderr)
