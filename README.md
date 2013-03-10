gopherfeed
==========

Convert RSS or Atom feeds to gophermap files.

-----------

Usage: gopherfeed FEED_URL [GOPHERMAP] [OPTIONS]
Convert RSS/Atom feed at FEED_URL to Gophermap file and save to GOPHERMAP if
specified, otherwise print to stdout

Or: gopherfeed -f FEED_FILE -d GOPHER_DIR [OPTIONS]
Read RSS/Atom feed URLs from FEED_FILE (one URL per line) and create a
directory structure of Gophermaps, including a central index, under GOPHER_DIR

Options for feed file (2nd usage pattern):

    -h HOSTNAME         Specify hostname to use in central index Gophermap
                            (defaults to FQDN of current machine)
    -i INDEX_HEADER     Specify a header to print at the top of the central
                            index Gophermap
    -p PORT             Specify port to use in central index Gophermap
                            (defaults to 70)
    -s SORT             Specify order in which feeds are listed in central
                            index.  Options are:
                                ALPHA - sort alphabetically by title
                                TIME - sort by time of most recent entry

Common options (1st and 2nd usage patterns):

    -t                  Timestamp feed entries in gophermap file
    -x                  Exclude Gopherfeed version footer

Note that in the 2nd pattern, gopherfeed should be run from within the
Goper server's root directory, as GOPHER_DIR will be created (if necessary) in
the current working directory.  Paths in the central index Gophermap will
begin with GOPHER_DIR, so if GOPHER_DIR is not in the Gopher root then the
server will not be able to find the individual feed directories.

Feed files should contain one URL, including scheme (e.g. http://), per line.
Blank lines and lines beginning with # will be ignored.

By invoking usage pattern 2 from an hourly cron job, you can use your Gopher
client as a basic feed aggregator.  This works best if you use a client which
also has seamless HTTP/HTML support (e.g. lynx).

Please report bugs to <luke@maurits.id.au> or at
<https://github.com/lmaurits/gopherfeed/issues>
