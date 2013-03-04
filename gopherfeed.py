# Copyright (c) 2013, Luke Maurits <luke@maurits.id.au>
# Published under the terms of the BSD 3-Clause License
# (see LICENSE file or http://opensource.org/licenses/BSD-3-Clause)

import feedparser

import sys

def gopherize_feed(feed_url):
    maplines = []
    f = feedparser.parse(feed_url)
    if "title" not in f.feed:
        return ""
    maplines.append("%s" % f.feed.title.replace("\t","    "))
    if "description" in f.feed:
        maplines.append(f.feed.description.replace("\t","    "))
    for entry in f.entries:
        filetype = "h"
        maplines.append("%s%s\tURL:%s" % (filetype, entry.title.replace("\t","   "), entry.link))
    gophermap = "\n".join(maplines)
    return gophermap
