#!/bin/bash

inputdir=$1
outputdir=$2
permadir=$3

for i in `ls ${inputdir}`; do
    echo ${inputdir}/${i}

    inohtml=`echo ${i} | sed 's/.html//g'`
    jekylldir=`echo ${inputdir} | sed 's?../../dsa-puddles/_includes/??g'`

    echo "---" > ${outputdir}/${i}
    echo "permalink: ${permadir}/${inohtml}" >> ${outputdir}/${i}
    echo "---" >> ${outputdir}/${i}
    echo "" >> ${outputdir}/${i}
    echo '<div style="text-align: left;">' >> ${outputdir}/${i}
    echo "{% include ${jekylldir}/${i} %}" >> ${outputdir}/${i}
    echo '</div>' >> ${outputdir}/${i}

done
