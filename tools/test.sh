#!/bin/sh

# The URL of the test file
BASEURL="http://publicsuffix.org/list/"
FILE="test.txt"
URL="$BASEURL$FILE"

# The local file name written by wget
OUT="$FILE"
TARGET="tools/$FILE"

# Download it!
if wget \
		--timestamping \
		"$URL"; then
	mv "$OUT" "$TARGET"
fi
