# datapypes -  Pythonic abstractions for data pipelines

**datapypes** provides the building blocks to enable the following:

```python
# Retrieve news from GoogleNews, store in MongoDB
News(query='Japan').latest(GoogleNews()).save(MongoDB())
```

```python
# Create a post, send to Twitter & Tumblr
Post(text='I did something interesting').save(
  Twitter(username='tweet_user', password='tweet_pass'),
  Tumblr(username='tumblr_user', password='tumblr_pass'))
```

```python
# Get SoundCloud, YouTube links for a track, post to Twitter, save to MongoDB
Track(artist="Meshuggah", title="New Millenium Cyanide Christ").get(
  SoundCloud(), Youtube()).save(
    Twitter(username='tweet_user', password='tweet_pass'),
    MongoDB(host='127.0.0.1'))
```

See examples.py for implementation details.

## Classes

Build your pipeline by subclassing these classes:

* **Attribute** - A typed model attribute, i.e. title, author, date
* **Model** - A data model, i.e. Article, Video
* **Set** - A set of data models, i.e. News, Videos
* **Source** - A data source, i.e. Google News, Twitter
* **Store** - A data source & store, i.e. MongoDB, Twitter
* **SourcePype** - Defines integration logic for Set & Source
* **StorePype** - Defines integration logic for Set & Store

## Actions

A **Source** defines these action methods:

* **one()** - Returns a single data point
* **latest()** - Returns a list of the most recent data
* **search()** - Returns a list of data matching a query
* **stream()** - Builds a list of data from a stream
* **all()** - Returns a list of all available source data

A **Store** defines these action methods:

* **save()** - Creates or updates data in a Store
* **update()** - Updates data in a Store
* **delete()** - Deletes data in a Store

## Pype methods

A **SourcePype** defines these methods:

* **one()** - Loads raw source data into a Model
* **latest()** - Loads recent source data into a Set
* **search()** - Loads found source data into a Set
* **stream()** - Loads raw stream data into a Set
* **all()** - Loads all source data into a Set

A **StorePype** defines these methods:

* **save_model()** - Saves a single Model to a Store
* **save_set()** - Saves an entire Set to a Store
* **update_model()** - Updates a single Model in a Store
* **update_set()** - Updates entire Set in a Store
* **delete_model()** - Deletes a single Model from a Store
* **delete_set()** - Deletes an entire Set from a Store

## Authors

Mike Smathers &lt;mikesmathers at gmail dot com&gt;

## License

All code is released under the MIT license. Please read the LICENSE.txt file for more details.