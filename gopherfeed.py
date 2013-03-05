# Copyright (c) 2013, Luke Maurits <luke@maurits.id.au>
# Published under the terms of the BSD 3-Clause License
# (see LICENSE file or http://opensource.org/licenses/BSD-3-Clause)

import feedparser

import codecs
import os
import sys

def _gopherize_feed_object(feed):
    maplines = []
    if "title" not in feed.feed:
        return ""
    maplines.append("%s" % feed.feed.title.replace("\t","    "))
    if "description" in feed.feed:
        maplines.append(feed.feed.description.replace("\t","    "))
    for entry in feed.entries:
        filetype = "h"
        maplines.append("%s%s\tURL:%s" % (filetype, entry.title.replace("\t","   "), entry.link))
    gophermap = "\n".join(maplines)
    return gophermap

def gopherize_feed(feed_url):
    return _gopherize_feed_object(feedparser.parse(feed_url))

def _slugify(feed):
    slug = feed.title
    slug = slug.encode("ASCII", "ignore")
    for kill in """.,:;-"'\`\/""":
        slug = slug.replace(kill,"_")
        slug = slug.replace(" ","_")
        slug = slug.lower()
    return slug

def _read_feed_urls(filename):
    feeds = []
    fp = codecs.open(filename, "r", "UTF-8")
    for line in fp:
        if line and not line.startswith("#"):
            feeds.append(line)
    fp.close()
    return feeds

def gopherize_feed_file(feedfile, directory, hostname, port=70):
    feeds = _read_feed_urls(feedfile)
    fp = codecs.open(directory+"/"+"gophermap", "w", "UTF-8")
    for feed_url in feeds:
	feed = feedparser.parse(feed_url)
	if "title" not in feed.feed:
    	    continue
	feed_slug = _slugify(feed.feed)
	dir = directory + "/" + feed_slug
	gophermap = dir + "/" + "gophermap"
	if not os.path.exists(dir):
    	    os.mkdir(dir)
	fp.write("1%s\t%s\t%s\t%d\n" % (feed.feed.title, dir, hostname, port))
        fp2 = codecs.open(gophermap, "a", "UTF-8")
	fp2.write(_gopherize_feed_object(feed))
        fp2.close()
    fp.close()
