import sys
import os
import pandas as pd
from sqlalchemy import create_engine
import datetime as dt

#host_name = '162.243.130.6'
host_name = 'localhost'
username = 'root'
password = 'teatime82'
dbname = 'twitter'
port = 5432

csv_file = sys.argv[1]
table_name = os.path.splitext(os.path.basename(csv_file))[0].replace('.', '')
engine = create_engine('postgresql://%s:%s@%s:%d/%s' % (username, password, host_name, port, dbname))

print "Importing %s to %s.%s on %s" % (csv_file, dbname, table_name, host_name)

dtypes = {
    '_source_file_': pd.np.object,
    'contributors': pd.np.float64,
    'coordinates': pd.np.float64,
    'created_at': pd.np.object,
    'entities': pd.np.bool,
    'favorite_count': pd.np.int64,
    'favorited': pd.np.bool,
    'geo': pd.np.float64,
    'id_str': pd.np.int64,
    'in_reply_to_screen_name': pd.np.object,
    'in_reply_to_status_id_str': pd.np.float64,
    'in_reply_to_user_id_str': pd.np.float64,
    'is_quote_status': pd.np.bool,
    'lang': pd.np.object,
    'metadata_iso_language_code': pd.np.object,
    'metadata_result_type': pd.np.object,
    'place': pd.np.float64,
    'possibly_sensitive': pd.np.object,
    'retweet_count': pd.np.int64,
    'retweeted': pd.np.bool,
    'retweeted_status': pd.np.object,
    'source': pd.np.object,
    'text': pd.np.object,
    'truncated': pd.np.bool,
    'user_created_at': pd.np.object,
    'user_description': pd.np.object,
    'user_followers_count': pd.np.int64,
    'user_friends_count': pd.np.int64,
    'user_id_str': pd.np.int64,
    'user_location': pd.np.object,
    'user_name': pd.np.object,
    'user_screen_name': pd.np.object,
    'user_statuses_count': pd.np.int64,
    'user_time_zone': pd.np.object,
    'user_utc_offset': pd.np.float64,
    'place_bounding_box': pd.np.object,
    'place_contained_within': pd.np.object,
    'place_country': pd.np.object,
    'place_country_code': pd.np.object,
    'place_full_name': pd.np.object,
    'place_name': pd.np.object,
    'place_place_type': pd.np.object,
    'place_url': pd.np.object,
    'quoted_status_id_str': pd.np.float64,
    'quoted_status': pd.np.object,
    'coordinates_lon': pd.np.float64,
    'coordinates_lat': pd.np.float64,
}


start = dt.datetime.now()
chunksize = 20000
rows_read = 0
if_exists = 'replace'
for df in pd.read_csv(csv_file, chunksize=chunksize, iterator=True, encoding='utf-8', dtype=dtypes):
    rows_read += len(df)
    print '{} seconds: completed {} rows'.format((dt.datetime.now() - start).seconds, rows_read)
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)
    if_exists = 'append'

print 'Completed all rows.'
