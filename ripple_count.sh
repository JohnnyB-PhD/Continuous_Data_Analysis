#!/bin/sh
for filename in *.txt; do
	name=$(basename $filename .txt)
	mkdir -p "Ripple Count"
	ripple="_ripple.txt"
	extension="_ripple_count.txt"
	output="$name$extension"
	if [ -f "Ripple Count"/$output ]; then
		continue
	fi
	ripplefile="$name$ripple"
	python /home/aperez6/packages/scripts/python/ripple_counts.py "Ripple"/$ripplefile "Ripple Count"/$output
done
