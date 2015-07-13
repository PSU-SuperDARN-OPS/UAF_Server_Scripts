#!/usr/bin/bash

function usage()
{
	echo "USAGE:"
	echo "./stage_rawacfs.bash YYYY MM DD"
	echo "Options:"
	echo "YYYY -- the year for which data files are requested"
	echo "MM -- the month for which data files are requested"
#	echo "DD -- the day for which data files are requested (optional)"
}

function check_online()
{
	local nfiles=`ls $1 | wc -l`
	local noffline=`/opt/SUNWsamfs/bin/sfind $1 -offline | wc -l`
	if [ $noffline == 0 ]; then
		echo 0 #All files are online
	elif [ $nfiles == $noffline ]; then
		echo 1 #All files are offline
	else
		echo 2 #Some but not all files are online
	fi
}

function get_num_offline()
{
	local noffline=$(/opt/SUNWsamfs/bin/sls $1/$2/$3 -D | grep "offline" | wc -l)
	echo $noffline
}


SD_DATA="/sam-qfs/SUPERDARN/mirror/sddata/rawacf"
YR=$1
MO=$2
DY=$3
if [ "$#" -lt 2 ]; then
	usage
	exit
fi

DIR=$SD_DATA/$YR/$MO/$YR$MO$DY
if [ -z $DY ]; then
	DIR=$SD_DATA/$YR/$MO
fi
echo $DIR

result=$(check_online $DIR*)
if [ $result == 0 ]; then
	echo "All files online"
elif [ $result == 1 ]; then
	echo "Fetching all files in the search path."
	echo "This may take some time.."
	noffline=$(get_num_offline $SD_DATA $YR $MO)
	echo "Number of offline files: $noffline"

	#exit

	/usr/local/bin/batch_stage $DIR
elif [ $result == 2 ]; then
	echo "Fetching all offline files."
	echo "This may take some time.."
	noffline=$(get_num_offline $SD_DATA $YR $MO)
	echo "Number of offline files: $noffline"

	#exit

	/opt/SUNWsamfs/bin/sfind $DIR* -offline | /usr/local/bin/batch_stage -i

	echo "All files online for $YR/$MO"
fi

exit
