#!/bin/sh
for i in *spikecount.txt; do
	name=$(basename $i _spikecount.txt)
	time="_timespent.txt"
	spike="_spikecount.txt"
	if [ -f "spike_analysis/"$name"_spike_analysis.txt" ]; then
		continue
	fi
	python "C:\Users\jbroussard5\Desktop\scripts\python\info_revision.py" "$name$time" "$name$spike"
done
