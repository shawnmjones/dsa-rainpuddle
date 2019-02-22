#!/bin/bash

export USER_AGENT="MementoEmbed/0.2018.09.07.000916"
export VIEWPORT_WIDTH=1024
export VIEWPORT_HEIGHT=768
export URIM=$1
export THUMBNAIL_OUTPUTFILE=$2

echo "executing node"

node ../MementoEmbed/mementoembed/static/js/create_screenshot.js

echo "done with execution"
