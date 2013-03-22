# Copyright (c) 2013, Luke Maurits <luke@maurits.id.au>
# Published under the terms of the BSD 3-Clause License
# (see LICENSE file or http://opensource.org/licenses/BSD-3-Clause)

__version__ = 1.2

import feedparser

import codecs
import os
import socket
import time

feedparser.USER_AGENT = "Gopherfeed +https://github.com/lmaurits/gopherfeed"
_TIME_FORMAT = "%Y-%m-%d %H:%M"

def _build_mapline(entry, timestamp=False, feed_object=None):
    """Return one line of a Gophermap, built from one feed entry bject."""
    filetype = "h"
    descr = entry.title.replace("\t","   ")
    if feed_object:
        descr = "%s: %s" % (feed_object.get("title", "Untitled feed"), descr)
    if timestamp:
        if "published_parsed" in entry:
            epoch = time.mktime(entry.published_parsed)
        elif "updated_parsed" in entry:
            epoch = time.mktime(entry.updated_parsed)
        timestamp = time.localtime(epoch)
        timestring = time.strftime(_TIME_FORMAT, timestamp)
        descr = "[%s] %s" % (timestring, descr)
    mapline = "%s%s\tURL:%s" % (filetype, descr, entry.link)
    return mapline

def gopherize_feed_object(feed_obj, timestamp=False, plug=True):
    """Return a gophermap string for a feed object produced by feedparser."""
    feed, entries = feed_obj.feed, feed_obj.entries
    if not entries:
        raise Exception("Problem either fetching or parsing feed")

    maplines = []
    feed_title = feed.get("title", feed.get("link", "Untitled feed"))
    feed_title = feed_title.replace("\t","    ")
    maplines.append(feed_title)
    if feed.get("description", None):
        maplines.append(feed.description.replace("\t","    "))
    maplines.append("")
    
    timestamped_maplines = []
    for entry in entries:
        mapline = _build_mapline(entry, timestamp)
        timestamped_maplines.append((entry.updated_parsed, mapline))

    # Entries are not guaranteed to appear in feed in chronological order,
    # so let's sort them
    timestamped_maplines.sort()
    timestamped_maplines.reverse()
    for updated, mapline in timestamped_maplines:
        maplines.append(mapline)

    if plug:
        if feed_obj.version.startswith("rss"):
            feed_type = "RSS feed"
        elif feed_obj.version.startswith("atom"):
            feed_type = "Atom feed"
        else:
            feed_type = "Unknown feed type"
        maplines.append("_"*70)
        plug_line = "Converted from %s by Gopherfeed %s" % (feed_type, __version__)
        maplines.append(plug_line.rjust(70))

    return "\n".join(maplines)

def gopherize_feed(feed_url, timestamp=False, plug=True):
    """Return a gophermap string for the feed at feed_url."""
    return gopherize_feed_object(feedparser.parse(feed_url), timestamp, plug)

def _slugify(feed):
    """Make a simple string from feed title, to use as a directory name."""
    slug = feed.title
    slug = slug.encode("ASCII", "ignore")
    for kill in """.,:;-"'\`\/""":
        slug = slug.replace(kill,"_")
        slug = slug.replace(" ","_")
        slug = slug.lower()
    return slug

def build_feed_index(feed_objects, directory, header=None, hostname=None,
        port=70, sort=None, plug=True):
    """
    Build a gophermap file in the specified directory, which presents an index
    for all the feeds in feed_objects.
    """
    if not hostname:
        hostname = socket.getfqdn()
    decorated_maplines = []
    for index, feed_obj in enumerate(feed_objects):
        feed, entries = feed_obj.feed, feed_obj.entries
        feed_slug = _slugify(feed)
        feed_dir = os.path.join(directory, feed_slug)
        feed_title = feed.get("title", feed.get("link", "Untitled feed"))
        feed_title = feed_title.replace("\t","    ")
        mre = max([entry.updated_parsed for entry in entries])
        mapline = "1%s\t%s\t%s\t%d" % (feed_title, feed_dir, hostname, port)
        if sort == "alpha":
            decorated_maplines.append((feed_title.lower(), mapline))
        elif sort == "time":
            decorated_maplines.append((mre, mapline))
        else:
            decorated_maplines.append((index, mapline))
    decorated_maplines.sort()
    if sort == "time":
        decorated_maplines.reverse()
    maplines = []
    if header:
        maplines.append(header)
        maplines.append("")
    for decoration, mapline in decorated_maplines:
        maplines.append(mapline)
    if plug:
        maplines.append("_"*70)
        plug_line = "Converted from RSS/Atom feeds by Gopherfeed %s" % __version__
        maplines.append(plug_line.rjust(70))

    return "\n".join(maplines)

def combine_feed_objects(feed_objs, max_entries=20, timestamp=False, plug=True):
    """
    Build a single gophermap string, combining the entries from all
    provided feed objects.
    """
    print("Final func got n: %d" % max_entries)
    timestamped_maplines = []
    for feed_obj in feed_objs:
        feed, entries = feed_obj.feed, feed_obj.entries
        for entry in entries:
            if "published_parsed" in entry:
                mapline = _build_mapline(entry, timestamp, feed)
                timestamped_maplines.append((time.mktime(entry.published_parsed), mapline))
            elif "updated_parsed" in entry:
                mapline = _build_mapline(entry, timestamp, feed)
                timestamped_maplines.append((time.mktime(entry.updated_parsed), mapline))
   
    timestamped_maplines.sort()
    timestamped_maplines.reverse()
    maplines = []
    for updated, mapline in timestamped_maplines[:max_entries]:
        maplines.append(mapline)

    if plug:
        maplines.append("_"*70)
        plug_line = "Converted from RSS/Atom feeds by Gopherfeed %s" % __version__
        maplines.append(plug_line.rjust(70))
    
    return "\n".join(maplines)
