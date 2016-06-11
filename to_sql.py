import sys
import os
import pandas as pd
from sqlalchemy import create_engine
import datetime as dt

host_name = '162.243.130.6'
username = 'root'
password = 'teatime82'
dbname = 'twitter'
port = 5432

csv_file = sys.argv[1]
table_name = os.path.splitext(os.path.basename(csv_file))[0].replace('.', '')
engine = create_engine('postgresql://%s:%s@%s:%d/%s' % (username, password, host_name, port, dbname))

print "Importing %s to %s.%s on %s" % (csv_file, dbname, table_name, host_name)

start = dt.datetime.now()
chunksize = 20000
for df in pd.read_csv(csv_file, chunksize=chunksize, iterator=True, encoding='utf-8'):

    print '{} seconds: completed {} rows'.format((dt.datetime.now() - start).seconds, j*chunksize)

df = pd.read_csv(csv_file, nrows=50)
#df.to_sql(table_name, engine)
