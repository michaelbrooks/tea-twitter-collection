import sys
import json
import csv
from collections import OrderedDict
from datetime import datetime

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
        if isinstance(value, dict):
            if key in excluded_keys:
                result[key] = '[obj]'
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
                result[key] = '[list]'
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

def convert_to_csv():
    header = [u'contributors', u'coordinates', u'created_at', u'entities', u'favorite_count',
                u'favorited', u'geo', u'id_str', u'in_reply_to_screen_name',
                u'in_reply_to_status_id_str', u'in_reply_to_user_id_str', u'is_quote_status',
                u'lang', u'metadata_iso_language_code', u'metadata_result_type', u'place',
                u'possibly_sensitive', u'retweet_count', u'retweeted', u'retweeted_status',
                u'source', u'text', u'truncated', u'user_contributors_enabled',
                u'user_created_at', u'user_default_profile', u'user_default_profile_image',
                u'user_description', u'user_entities', u'user_favourites_count',
                u'user_follow_request_sent', u'user_followers_count', u'user_following',
                u'user_friends_count', u'user_geo_enabled', u'user_has_extended_profile',
                u'user_id_str', u'user_is_translation_enabled', u'user_is_translator',
                u'user_lang', u'user_listed_count', u'user_location', u'user_name',
                u'user_notifications', u'user_profile_background_color',
                u'user_profile_background_image_url',
                u'user_profile_background_image_url_https', u'user_profile_background_tile',
                u'user_profile_banner_url', u'user_profile_image_url',
                u'user_profile_image_url_https', u'user_profile_link_color',
                u'user_profile_sidebar_border_color', u'user_profile_sidebar_fill_color',
                u'user_profile_text_color', u'user_profile_use_background_image',
                u'user_protected', u'user_screen_name', u'user_statuses_count',
                u'user_time_zone', u'user_url', u'user_utc_offset', u'user_verified',
                u'place_bounding_box', u'place_contained_within', u'place_country',
                u'place_country_code', u'place_full_name', u'place_name', u'place_place_type',
                u'place_url', u'quoted_status_id_str', u'quoted_status', u'coordinates_lon',
                u'coordinates_lat']

    writer = csv.DictWriter(sys.stdout, header, restval='', extrasaction='ignore')
    writer.writeheader()
    lineno = 0
    for line in sys.stdin:
        lineno += 1

        try:
            raw = json.loads(line)
        except ValueError:
            log("Parse error on line %d" % lineno)
            continue

        f = flatten(raw)

        try:
            writer.writerow(f)
        except:
            print f
            break
if __name__ == '__main__':
    #find_header()
    convert_to_csv()
