#!/bin/sh
for filename in *.txt; do
	name=$(basename $filename .txt)
	extension="_ripple.txt"
	mkdir -p "Ripple"
	output="$name$extension"
	if [ -f "Ripple"/$output ]; then
		continue
	fi
	python ~/packages/scripts/python/ripple.py $filename "Ripple"/$output
done
