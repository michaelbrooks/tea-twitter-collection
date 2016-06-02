
import sys
import json
from tweepy.utils import parse_datetime

def pf(msg, outfile=sys.stdout):
    print >> outfile, msg

def print_tweet(t, outfile=sys.stdout):
    pf("id_str:\t\t%s" % t['id_str'], outfile)
    pf("created_at:\t%s" % t['created_at'], outfile)
    pf("text:\t\t%s" % t['text'], outfile)
    #pf("text:\t\t%s" % t['text'].encode('utf-8'), outfile)
    
    return parse_datetime(t['created_at'])

def summary(inputfile, outfile=sys.stdout):
    with open(inputfile, "rb") as f:
        first = f.readline()      # Read the first line.
        f.seek(-2, 2)             # Jump to the second last byte.
        while f.read(1) != b"\n": # Until EOL is found...
            f.seek(-2, 1)         # ...jump back the read byte plus one more.
        last = f.readline()       # Read last line.

    first = json.loads(first)
    last = json.loads(last)

    pf("First tweet:", outfile)
    first = print_tweet(first, outfile)

    pf("Last tweet:", outfile)
    last = print_tweet(last, outfile)

    pf("Duration: %s" % (first - last), outfile)


if __name__ == '__main__':
    summary(sys.argv[1])
