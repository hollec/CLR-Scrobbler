#!/usr/bin/env python

# CLR Scrobbler -- Command-line Rhapsody Scrobbler
# Copyright (c) 2012 hollec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import calendar
import datetime

from dateutil.parser import parse

import feedparser
import pylast

# Prerequisites (Ubuntu packages): python-dateutil, python-feedparser
# Prerequisites (Manual installs): http://code.google.com/p/pylast/


# Rhapsody Settings
# Get your RSS Feed URL from: http://www.rhapsody.com/myrhapsody/feeds.html
# Set your profile to Public and copy the Recently Played Tracks URL
RHAPSODY_FEED_URL = 'http://feeds.rhapsody.com/member/xxxxxxxxxxxxxxxxxxxxxxxxxxxxx/track-history.rss'

# Last.fm Settings
# Sign up for an API Account from: http://www.last.fm/api/account
LASTFM_API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
LASTFM_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
LASTFM_USERNAME = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
LASTFM_PASSWORD = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Required variables
tracks = []
session_key = None

# Sign in to Last.fm
network = pylast.LastFMNetwork(LASTFM_API_KEY, LASTFM_SECRET, session_key, LASTFM_USERNAME, pylast.md5(LASTFM_PASSWORD))

# Download the latest Rhapsody RSS Feed
rhap_rss = feedparser.parse(RHAPSODY_FEED_URL)

# Extract the relevant track information
for entry in rhap_rss.entries:
    print entry.rhap_artist         # Current artist
    artist = entry.rhap_artist
    print '\t',entry.rhap_track     # Current track
    title = entry.rhap_track
    print '\t',entry.rhap_album     # Current album
    album = entry.rhap_album
    print '\t',entry.updated        # Time scrobbled

    # convert the time scrobbled to a UNIX timestamp (UTC time zone)
    dt = parse(entry.updated)
    timestamp = calendar.timegm(dt.timetuple())

    tracks.append({"artist": artist, "title": title, "album": album, "timestamp": timestamp})

# Reverse the order of the tracks so the first heard song is submitted
# first.  This cleans up the last.fm user page, which displays items
# in the order they were submitted.  The actual main tracks page does
# display the tracks in the correct order no matter what.
tracks.reverse()

# Submit the track information to Last.fm
print "Submitting track information ..."
network.scrobble_many(tracks)

print "Submitted", len(tracks), "songs to last.fm"
