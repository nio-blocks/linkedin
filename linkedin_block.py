from requests_oauthlib import OAuth1
from datetime import datetime
from nio.common.discovery import Discoverable, DiscoverableType
from .http_blocks.rest.rest_block import RESTPolling
from nio.metadata.properties.object import ObjectProperty
from nio.metadata.properties.string import StringProperty
from nio.metadata.properties.timedelta import TimeDeltaProperty
from nio.metadata.properties.int import IntProperty
from nio.metadata.properties.holder import PropertyHolder
from nio.common.signal.base import Signal


class LinkedInSignal(Signal):
    def __init__(self, data):
        for k in data:
            setattr(self, k, data[k])


class OAuthCreds(PropertyHolder):
    consumer_key = StringProperty()
    app_secret = StringProperty()
    oauth_token = StringProperty()
    oauth_secret = StringProperty()


@Discoverable(DiscoverableType.block)
class LinkedIn(RESTPolling):
    URL_FORMAT = ("https://api.linkedin.com/v1/groups/{0}/"
                  "posts:(id,creator,title,summary,creation-timestamp,"
                  "site-group-post-url)?category=discussion&order=recency&"
                  "modified-since={1}&count={2}")

    creds = ObjectProperty(OAuthCreds)
    lookback = TimeDeltaProperty()
    limit = IntProperty(default=10)

    def __init__(self):
        super().__init__()
        self._paging_field = 'dunno'
        self._created_field = 'creationTimestamp'

    def configure(self, context):
        super().configure(context)
        lb = self._unix_time(datetime.utcnow() - self.lookback) * 1000
        self._freshest = [lb] * self._n_queries

    def _authenticate(self):
        if self.creds.consumer_key is None or self.creds.app_secret is None:
            self._logger.error("You need a consumer key and app secret, yo")
        else:
            self._auth = OAuth1(self.creds.consumer_key, self.creds.app_secret,
                                self.creds.oauth_token, self.creds.oauth_secret)

    def _process_response(self, resp):
        signals = []
        resp = resp.json()
        fresh_posts = posts = resp.get('values') or []
        paging = resp.get(self._paging_field) is not None
        self._logger.debug("LinkedIn response contains %d posts" % len(posts))

        if len(posts) > 0:
            self.update_freshness(posts)
            fresh_posts = self.find_fresh_posts(posts)
            paging = len(fresh_posts) == self.limit

            if len(fresh_posts) > 0:
                self.prev_stalest = self.created_epoch(fresh_posts[-1])
        
        signals = [LinkedInSignal(p) for p in fresh_posts]
        self._logger.debug("Found %d fresh posts" % len(signals))

        return signals, paging

    def _prepare_url(self, paging=False):
        headers = {
            "x-li-format": "json",
            "Content-Type": "application/json"
        }
        fmt = self.URL_FORMAT

        if not paging:
            self.paging_url = None
            self.url = fmt.format(self.current_query,
                                  self.freshest - 2,
                                  self.limit)
        return headers

    def created_epoch(self, post):
        return post.get(self._created_field)
