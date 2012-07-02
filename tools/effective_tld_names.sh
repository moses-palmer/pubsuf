#/bin/sh

# The URL of the database file
BASEURL="http://mxr.mozilla.org/mozilla-central/source/netwerk/dns/"
FILE="effective_tld_names.dat"
FLAGS="?raw=1"
URL="$BASEURL$FILE$FLAGS"

# The local file name written by wget
OUT="$FILE$FLAGS"
TARGET="tools/$FILE"

# Download it!
if wget \
		--timestamping \
		"$URL"; then
	mv "$OUT" "$TARGET"
fi
