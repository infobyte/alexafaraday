"""Netsec API connector"""
import feedparser

URL = "http://www.reddit.com/r/netsec/.rss"

def topstories():
    """Return last news"""
    news = feedparser.parse(URL)
    return news
