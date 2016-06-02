# Tea Twitter Collection

Get set up:
```bash
conda create -n twitter python=2.7
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

Convert tweets to csv:

```bash
python conversion.py < query.raw.json > query.raw.csv
```

Get info about the first and last tweets in a raw json file:

```bash
python first_last.py query.raw.json
```
