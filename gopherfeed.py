# Copyright (c) 2013, Luke Maurits <luke@maurits.id.au>
# Published under the terms of the BSD 3-Clause License
# (see LICENSE file or http://opensource.org/licenses/BSD-3-Clause)

import feedparser

import codecs
import os

def _gopherize_feed_object(feed):
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
        maplines.append("%s%s\tURL:%s" % (filetype, descr, entry.link))
    gophermap = "\n".join(maplines)
    return gophermap

def gopherize_feed(feed_url):
    """Return a gophermap string for the feed at feed_url."""
    return _gopherize_feed_object(feedparser.parse(feed_url))

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

def gopherize_feed_file(feedfile, directory, hostname, port=70):
    """
    Read a file of URLs and generate a directory structure of gophermaps.

    This method will read URLs from a file and then create a directory
    structure, in which each feed gets its own directory.  Goperhmap files
    will be created for each feed (in that feed's directory), along with one
    master gophermap file at the root of the directory structure which acts
    as an index to the others (using each feed's title as the descriptor).
    """
    feeds = _read_feed_urls(feedfile)
    fp = codecs.open(directory+"/"+"gophermap", "w", "UTF-8")
    for feed_url in feeds:
        feed = feedparser.parse(feed_url)
        if "title" not in feed.feed:
            continue
        feed_slug = _slugify(feed.feed)
        directory = directory + "/" + feed_slug
        gophermap = directory + "/" + "gophermap"
        if not os.path.exists(directory):
            os.mkdir(directory)
        fp.write("1%s\t%s\t%s\t%d\n" % (feed.feed.title, directory, hostname, port))
        fp2 = codecs.open(gophermap, "w", "UTF-8")
        fp2.write(_gopherize_feed_object(feed))
        fp2.close()
    fp.close()
