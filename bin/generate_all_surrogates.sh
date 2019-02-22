#!/bin/bash

inputfile=$1
outputdir=$2
storyid=$3
metadatafile=$4


python ./generate_summary_page -i ${inputfile} -o ${outputdir}/${storyid}-socialcards.html -s socialcard
python ./generate_summary_page -i ${inputfile} -o ${outputdir}/${storyid}-thumbnails-simple.html -s thumbnail
python ./rearrange_thumbnails.py ${outputdir}/${storyid}-thumbnails-simple.html ${outputdir}/${storyid}-thumbnails.html
python ./generate_summary_page -i ${inputfile} -o ${outputdir}/${storyid}-socialcard_thumbnail.html -s socialcard+thumbnail
python ./generate_summary_page -i ${inputfile} -o ${outputdir}/${storyid}-socialcardwiththumbonhover.html -s socialcard+hoverthumb
python ./generate_summary_page -i ${inputfile} -o ${outputdir}/${storyid}-socialcardwiththumbasimg.html -s thumbnailcard
python ./make_archiveit_interface.py ${outputdir}/${storyid}-socialcards.html ${metadatafile} ${outputdir}/${storyid}-archiveitlike.html
