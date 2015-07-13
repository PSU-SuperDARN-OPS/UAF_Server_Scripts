#!/usr/bin/bash

SD_DATA="/sam-qfs/SUPERDARN/mirror/sddata/rawacf/*/"

function usage()
{
	echo "Script that stages all rawacf hash files onto disk"
	echo "The search directory is $SD_DATA"
}
	
if [ ! -z $1 ]; then
	usage
	exit
fi

sfind $SD_DATA -name "*.hashes" -offline | batch_stage -i

exit
