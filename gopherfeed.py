# Copyright (c) 2013, Luke Maurits <luke@maurits.id.au>
# Published under the terms of the BSD 3-Clause License
# (see LICENSE file or http://opensource.org/licenses/BSD-3-Clause)

import feedparser

import codecs
import os
import socket
import time

feedparser.USER_AGENT = "Gopherfeed +https://github.com/lmaurits/gopherfeed"
_TIME_FORMAT = "%Y-%m-%d %H:%M"

def _gopherize_feed_object(feed_obj, timestamp=False):
    """Return a gophermap string for a feed object produced by feedparser."""
    feed, entries = feed_obj.feed, feed_obj.entries
    if not entries:
        return ""

    maplines = []
    feed_title = feed.get("title", feed.get("link", "Untitled feed"))
    feed_title = feed_title.replace("\t","    ")
    maplines.append(feed_title)
    if "description" in feed:
        maplines.append(feed.description.replace("\t","    "))
    
    timestamped_maplines = []
    for entry in entries:
        filetype = "h"
        descr = entry.title.replace("\t","   ")
        if timestamp:
            timestring = time.strftime(_TIME_FORMAT, entry.updated_parsed)
            descr = "[%s] %s" % (timestring, descr)
        mapline = "%s%s\tURL:%s" % (filetype, descr, entry.link)
        timestamped_maplines.append((entry.updated_parsed, mapline))

    # Entries are not guaranteed to appear in feed in chronological order,
    # so let's sort them
    timestamped_maplines.sort()
    timestamped_maplines.reverse()
    for updated, mapline in timestamped_maplines:
        maplines.append(mapline)
    return "\n".join(maplines)

def gopherize_feed(feed_url, timestamp=False):
    """Return a gophermap string for the feed at feed_url."""
    return _gopherize_feed_object(feedparser.parse(feed_url), timestamp)

def _slugify(feed):
    """Make a simple string from feed title, to use as a directory name."""
    slug = feed.title
    slug = slug.encode("ASCII", "ignore")
    for kill in """.,:;-"'\`\/""":
        slug = slug.replace(kill,"_")
        slug = slug.replace(" ","_")
        slug = slug.lower()
    return slug

def _read_feed_urls(filename):
    """Return a list of URLs read from a file, one per line."""
    feeds = []
    fp = codecs.open(filename, "r", "UTF-8")
    for line in fp:
        # Ignore blank and commented lines
        if line and not line.startswith("#"):
            feeds.append(line)
    fp.close()
    return feeds

def gopherize_feed_file(feedfile, directory, hostname=None, port=70,
        sort=None, timestamp=False):
    """
    Read a file of URLs and generate a directory structure of gophermaps.

    This method will read URLs from a file and then create a directory
    structure, in which each feed gets its own directory.  Goperhmap files
    will be created for each feed (in that feed's directory), along with one
    master gophermap file at the root of the directory structure which acts
    as an index to the others (using each feed's title as the descriptor).
    """
    if not hostname:
        hostname = socket.getfqdn()
    feeds = _read_feed_urls(feedfile)
    decorated_maplines = []
    for index, feed_url in enumerate(feeds):
        feed = feedparser.parse(feed_url)
        if "title" not in feed.feed:
            continue
        feed_slug = _slugify(feed.feed)
        feed_dir = os.path.join(directory, feed_slug)
        gophermap = os.path.join(feed_dir, "gophermap")
        if not os.path.exists(feed_dir):
            os.mkdir(feed_dir)
        descr = feed.feed.title.replace("\t", "    ")
        mre = max([entry.updated_parsed for entry in feed.entries])
#        if timestamp:
#            timestring = time.strftime(_TIME_FORMAT, mre)
#            descr = "[%s] %s" % (timestring, descr)
        mapline = "1%s\t%s\t%s\t%d\n" % (descr, feed_dir, hostname, port)
        if sort == "alpha":
            decorated_maplines.append((feed.feed.title.lower(), mapline))
        elif sort == "time":
            decorated_maplines.append((mre, mapline))
        else:
            decorated_maplines.append((index, mapline))
        fp2 = codecs.open(gophermap, "w", "UTF-8")
        fp2.write(_gopherize_feed_object(feed, timestamp))
        fp2.close()
    decorated_maplines.sort()
    if sort == "time":
        decorated_maplines.reverse()

    if not os.path.exists(directory):
        os.mkdir(directory)
    fp = codecs.open(os.path.join(directory, "gophermap"), "w", "UTF-8")
    for decoration, mapline in decorated_maplines:
        fp.write(mapline)
    fp.close()
