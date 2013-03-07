# Copyright (c) 2013, Luke Maurits <luke@maurits.id.au>
# Published under the terms of the BSD 3-Clause License
# (see LICENSE file or http://opensource.org/licenses/BSD-3-Clause)

import feedparser

import codecs
import os
import socket
import time

_TIME_FORMAT = "%Y-%m-%d %H:%M"

def _gopherize_feed_object(feed, timestamp=False):
    """Return a gophermap string for a feed object produced by feedparser."""
    maplines = []
    if "title" not in feed.feed:
        return ""
    maplines.append("%s" % feed.feed.title.replace("\t","    "))
    if "description" in feed.feed:
        maplines.append(feed.feed.description.replace("\t","    "))
    for entry in feed.entries:
        filetype = "h"
        descr = entry.title.replace("\t","   ")
        if timestamp:
            timestring = time.strftime(_TIME_FORMAT, entry.updated_parsed)
            descr = "[%s] %s" % (timestring, descr)
        maplines.append("%s%s\tURL:%s" % (filetype, descr, entry.link))
    gophermap = "\n".join(maplines)
    return gophermap

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
    fp = codecs.open(directory+"/"+"gophermap", "w", "UTF-8")
    for index, feed_url in enumerate(feeds):
        feed = feedparser.parse(feed_url)
        if "title" not in feed.feed:
            continue
        feed_slug = _slugify(feed.feed)
        directory = directory + "/" + feed_slug
        gophermap = directory + "/" + "gophermap"
        if not os.path.exists(directory):
            os.mkdir(directory)
        mapline = "1%s\t%s\t%s\t%d\n" % (feed.feed.title, directory, hostname, port)
        if sort == "alpha":
            decorated_maplines.append((feed.feed.title.lower(), mapline))
        else:
            decorated_maplines.append((index, mapline))
        fp2 = codecs.open(gophermap, "w", "UTF-8")
        fp2.write(_gopherize_feed_object(feed, timestamp))
        fp2.close()
    decorated_maplines.sort()
    for decoration, mapline in decorated_maplines:
        fp.write(mapline)
    fp.close()
