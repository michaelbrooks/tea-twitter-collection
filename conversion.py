import io
import sys
import json
import csv
from collections import OrderedDict
from datetime import datetime
from tweepy.utils import parse_datetime

from dateutil import tz
utc = tz.tzutc()

def log(s):
    print >> sys.stderr, "%s > %s" % (datetime.now().isoformat(), s)

# Do not expand these keys - simply record whether they exist
excluded_keys = set([u'retweeted_status', u'quoted_status',
    u'hashtags', u'symbols', u'urls', u'entities', u'user_mentions',
    u'bounding_box', u'contained_within', u'geo',
    u'scopes', u'withheld_in_countries'])
def flatten(d):
    result = OrderedDict()
    for key in sorted(d.keys()):
        # Skip ids where we have a str version
        if key.endswith('status_id') or key.endswith('user_id') or key == 'id':
            continue

        value = d[key]

        ## parse and reformat times
        if key == 'created_at':
            value = parse_datetime(value).replace(tzinfo=utc).isoformat()

        if key == 'text':
            value = value.replace('\n', ' ').replace('\r', '')

        if isinstance(value, dict):
            if key in excluded_keys:
                result[key] = bool(value)
            elif key == u'coordinates':
                result['%s_lon' % key] = value['coordinates'][0]
                result['%s_lat' % key] = value['coordinates'][1]
            else:
                try:
                    flattened = flatten(value)
                    for k in flattened:
                        result['%s_%s' % (key, k)] = flattened[k]
                except ValueError,e:
                    log("Error flattening dict: %s" % key)
                    raise e

        elif isinstance(value, list):
            if key in excluded_keys:
                result[key] = bool(value)
            else:
                log("Unknown list key: %s" % key)
                raise ValueError(key)
        elif isinstance(value, unicode):
            result[key] = value.encode('utf-8')
        else:
            result[key] = value
    return result


# Read the first 1000 lines of input and print out the list of fields detected
def find_header():
    lineno = 0
    keys = OrderedDict()
    for line in sys.stdin:
        lineno += 1

        try:
            raw = json.loads(line)
        except ValueError:
            log("Parse error on line %d" % lineno)
            continue

        f = flatten(raw)
        for k in f.keys():
            keys[k] = 1

        if lineno > 1000:
            break
    print keys.keys()

def convert_to_csv(input_filename):
    header = [
        '_source_file_',
        u'contributors',
        u'coordinates',
        u'created_at',
        u'entities',
        u'favorite_count',
        u'favorited',
        u'geo',
        u'id_str',
        u'in_reply_to_screen_name',
        u'in_reply_to_status_id_str',
        u'in_reply_to_user_id_str',
        u'is_quote_status',
        u'lang',
        u'metadata_iso_language_code',
        u'metadata_result_type',
        u'place',
        u'possibly_sensitive',
        u'retweet_count',
        u'retweeted',
        u'retweeted_status',
        u'source',
        u'text',
        u'truncated',
        u'user_created_at',
        u'user_description',
        u'user_followers_count',
        u'user_friends_count',
        u'user_id_str',
        u'user_location',
        u'user_name',
        u'user_screen_name',
        u'user_statuses_count',
        u'user_time_zone',
        u'user_utc_offset',
        u'place_bounding_box',
        u'place_contained_within',
        u'place_country',
        u'place_country_code',
        u'place_full_name',
        u'place_name',
        u'place_place_type',
        u'place_url',
        u'quoted_status_id_str',
        u'quoted_status',
        u'coordinates_lon',
        u'coordinates_lat'
    ]

    writer = csv.DictWriter(sys.stdout, header, restval='', extrasaction='ignore')
    writer.writeheader()
    lineno = 0

    with io.open(input_filename, encoding='utf-8') as inputfile:
        for line in inputfile:
            lineno += 1

            try:
                raw = json.loads(line)
            except ValueError:
                log("Parse error on line %d" % lineno)
                continue

            f = flatten(raw)
            f['_source_file_'] = input_filename

            try:
                writer.writerow(f)
            except:
                print f
                break
if __name__ == '__main__':
    #find_header()
    input_filename = sys.argv[1]
    convert_to_csv(input_filename)
