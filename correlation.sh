#!/bin/sh
IFS=$'\n'
set -f
cd "/home/aperez6/dashlab/share/Broussard"
for i in $(awk '{print $0}' /home/aperez6/box_positions2); do 
	basename=$(echo $i | awk '{print $1}')
	echo $basename
	corr="_correlations.txt"
	analysis="$basename$corr"
	if [ -f "/home/aperez6/dashlab/share/Broussard/correlations_nofilter/$analysis" ]; then
		continue
	fi
	declare -i sx
	declare -i sy
	declare -i ex
	declare -i ey
	sx1=$(echo $i | awk '{print $2}')
	sy1=$(echo $i | awk '{print $3}')
	ex1=$(echo $i | awk '{print $4}')
	ey1=$(echo $i | awk '{print $5}')
	sx2=$(echo $i | awk '{print $6}')
	sy2=$(echo $i | awk '{print $7}')
	ex2=$(echo $i | awk '{print $8}')
	ey2=$(echo $i | awk '{print $9}')
	correlation.py $basename $sx1 $sy1 $ex1 $ey1 $sx2 $sy2 $ex2 $ey2
	mv $analysis correlations_nofilter
done
