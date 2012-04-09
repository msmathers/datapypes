from datapypes import (
  Attribute,
  Model,
  Set,
  Source,
  Store,
  SourcePype,
  StorePype,
  register_pypes
)

from datetime import datetime

class String(Attribute):
    def _validate(self, val):
        return val is None or isinstance(val, str)

class Datetime(Attribute):
    def _validate(self, val):
        return val is None or isinstance(val, datetime)

class NewsItem(Model):
    title = String()
    snippet = String()
    query = String()
    date = Datetime()

class News(Set):
    model = NewsItem

class GoogleNews(Source):
    def one(self, query):
        print "Querying google one: %s" % query
        # Google API hooks
        return {
          'title': 'Single News Item 1',
          'snippet': 'The single news item 1',
          'date': datetime(2012,4,13)
        }

    def latest(self, query):
        print "Querying google for: %s" % query
        # Google API hooks
        return [{
          'title': 'NewsItem 1',
          'snippet': 'The news item 1',
          'date': datetime(2012,4,13),
        },{
          'title': 'NewsItem 2',
          'snippet': 'The news item 2',
          'date': datetime(2012,4,14)
        }]

class GoogleNewsPype(SourcePype):
    set = News
    source = GoogleNews

    def one(self, query_model):
        query = {'query': query_model.query}
        return self.retrieve_model(self._source.one(query=query))

    def latest(self, query_model):
        query = {'query': query_model.query}
        return self.retrieve_set(self._source.latest(query=query))

class MongoDB(Store):
    def __init__(self, host='localhost', port=27017):
        self._host = host
        self._port = port

    def save(self, collection, doc):
        print "Saving data to mongo collection: %s" % collection
        print doc
        # pymongo hooks

class MongoNewsPype(StorePype):
    set = News
    store = MongoDB

    def save_model(self, data_model):
        collection = data_model.__class__.__name__
        self._store.save(collection, data_model._data)

    def save_set(self, data_set):
      for obj in data_set:
          self.save_model(obj)

register_pypes(MongoNewsPype, GoogleNewsPype)

print '''
NewsItem(query='stuff').get(GoogleNews()).save(MongoDB())
'''

NewsItem(query='stuff').get(GoogleNews()).save(MongoDB())

print '''
News(query='stuff').latest(GoogleNews()).save(MongoDB())
'''
News(query='stuff').latest(GoogleNews()).save(MongoDB())

print '''
News(query='stuff').latest(GoogleNews()).filter(
  lambda x: '1' in x.title
).save(MongoDB())
'''
News(query='stuff').latest(GoogleNews()).filter(
  lambda x: '1' in x.title
).save(MongoDB())e


class Post(Model):
    title = String()
    text = String()
    date = Datetime()

class Posts(Set):
    model = Post

class Twitter(Store):
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def save(self, text):
        print "Posting to twitter: %s" % text
        # Twitter API hooks

class TwitterPostPype(StorePype):
    set = Posts
    store = Twitter

    def save_model(self, data_model):
        self._store.save(data_model.text)

class Tumblr(Store):
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def save(self, text):
        print "Posting to tumblr: %s" % text
        # Tumblr API hooks

class TumblrPostPype(StorePype):
    set = Posts
    store = Tumblr

    def save_model(self, data_model):
        self._store.save(data_model.text)

register_pypes(TwitterPostPype, TumblrPostPype)

print '''
Post(text='This is post').save(
  Twitter(username='',password=''),
  Tumblr(username='',password=''))
'''

Post(text='This is post').save(
  Twitter(username='',password=''),
  Tumblr(username='',password=''))


class URL(Attribute):
    def _validate(self, val):
        return val is None or val.startswith("http")

class Track(Model):
    artist = String()
    title = String()
    track_url = URL()
    video_url = URL()

class Tracks(Set):
    model = Track

class SoundCloud(Source):
    def one(self, query):
        print "Searching soundcloud for: %s" % query
        return {'track_url': 'http://soundcloud/'}

class Youtube(Source):
    def one(self, query):
        print "Searching youtube for: %s" % query
        return {
          'video_url': 'http://youtube/',
          'track_url': 'http://youtube/'
        }

class SoundCloudTrackPype(SourcePype):
    set = Tracks
    source = SoundCloud

    def one(self, query_model):
        query = {'query': "%s %s" % (query_model.artist, query_model.title)}
        return self.retrieve_model(self._source.one(**query))

class YoutubeTrackPype(SourcePype):
    set = Tracks
    source = Youtube

    def one(self, query_model):
        query = {'query': "%s %s" % (query_model.artist, query_model.title)}
        return self.retrieve_model(self._source.one(**query))

class TwitterTrackPype(StorePype):
    set = Tracks
    store = Twitter

    def save_model(self, data_model):
        tweet = "'%s' by '%s'" % (data_model.title, data_model.artist)
        if data_model.track_url:
            tweet += ". Track: %s" % data_model.track_url
        if data_model.video_url:
            tweet += ". Video: %s" % data_model.video_url
        self._store.save(tweet)

class MongoDBTrackPype(StorePype):
    set = Tracks
    store = MongoDB

    def save_model(self, data_model):
        coll = data_model.__class__.__name__
        self._store.save(coll, data_model._data)

register_pypes(
  SoundCloudTrackPype,
  YoutubeTrackPype,
  TwitterTrackPype,
  MongoDBTrackPype
)

#register(*globals().values())

print '''
Track(artist="Meshuggah", title="New Millenium").get(
  SoundCloud(), Youtube()).save(
    Twitter(username='', password=''),
    MongoDB(host='127.0.0.1')
'''

Track(artist="Meshuggah", title="New Millenium").get(
  SoundCloud(), Youtube()).save(
    Twitter(username='', password=''),
    MongoDB(host='127.0.0.1'))
