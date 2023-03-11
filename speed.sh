#!/bin/sh
for filename in *.txt; do
	name=$(basename $filename .txt)
	extension="_timestamps.txt"
	mkdir -p "timestamps"
	output="$name$extension"
	if [ -f "timestamps"/$output ]; then
		continue
	fi
	python "C:\Users\jbroussard5\Desktop\scripts\python\speed.py" $filename "timestamps"/$output
done
