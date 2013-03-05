gopherfeed
==========

Convert RSS or Atom feeds to gophermap files.

Usage pattern 1: gopherfeed FEED_URL [GOPHERMAP_FILENAME]
This will turn the feed at FEED_URL into a gophermp and save it to
GOPHER_FILENAME if specified, or print it stdout if not.
    
Usage pattern 2: gopherfeed -f FEED_FILE -d GOPHER_DIR -h HOSTNAME
This will read feed URLs from FEED_FILE (one URL per line) and turn them all
into gophermap files.  Each feed's gophermap will end up in its own directory
under the directory GOPHER_DIR.  A master goperhmap pointing to each of the
feeds will also be created under GOPHER_DIR, using the hostname HOSTNAME.

By invoking usage pattern 2 from an hourly cron job, you can use your Gopher
client as a basic feed aggregator.  This works best if you use a client which
also has seamless HTTP/HTML support (e.g. lynx).

Note that in usage pattern 2, gopherfeed should be called from the root
directory of your Gopher server.

Note that gopherfeed is presently fairly fragile and may not fail gracefully
or explicitly if you, e.g. leave the http:// off a feed URL or do not have
appropriate filesystem permissions to do what you ask it to do.  Tread
carefully!
