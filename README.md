# Tea Twitter Collection

Get set up:
```bash
conda create -n twitter python=2.7 sqlalchemy pandas psycopg2
source activate twitter
pip install -r requirements.txt
```

Create `twitter_keys.py`:

```python
CONSUMER_KEY='blah'
CONSUMER_SECRET='blahblahblah'

ACCESS_KEY='blah-blahblah'
ACCESS_TOKEN='blahblahblah'
```

Create a `query.json` file:

```json
{
  "q": "tea -\"tea party\"",
  "lang": "en"
}
```

Collect tweets:

```bash
python collection.py query.json 2> query.err
```

Get info about the first and last tweets in a raw json file:

```bash
python first_last.py query.raw.json
```

Sample lines in a file:

```bash
python sample.py 0.10 < query.raw.json > query.sampled.json
```

Convert tweets to csv:

```bash
python conversion.py query.raw.json > query.raw.csv
```

Convert a bunch of tweet json files to csv:

```bash
for f in *.raw.json; do
  python conversion.py $f > $( basename $f .json).csv;
done
```

Combine a bunch of CSV files together:

```
# Get the header from one csv file
head -n 1 first_csv.raw.csv > combined.csv
# Get the body of all of the rest (watch out you aren't reading from the output file though)
gtail -q -n +2 *.raw.csv >> combined.csv
```
