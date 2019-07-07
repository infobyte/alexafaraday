"""Hackernews API connector"""
import feedparser

URL = "https://news.ycombinator.com/rss"

def topstories():
    """Return last news"""
    news = feedparser.parse(URL)
    return news
