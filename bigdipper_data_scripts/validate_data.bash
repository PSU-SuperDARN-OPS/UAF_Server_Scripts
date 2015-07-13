#!/usr/bin/bash

SD_DATA="/sam-qfs/SUPERDARN/mirror/sddata/rawacf"
#SD_DATA="$HOME/SUPERDARN/mirror/sddata/rawacf" # Used for testing
EMAIL_ADDRESS="alexmorrisak@gmail.com,jdspaleta@alaska.edu" #Assign address to get notifications of data mismatch(es)
EMAIL_ADDRESS="alexmorrisak@gmail.com" #Assign address to get notifications of data mismatch(es)
ERROR_FILE=error_file.txt
MAIL_BODY=/tmp/sd_mail.txt

YR=$1

function usage()
{
	echo "Script that checks to see if local archived files are different from the remote files."
	echo "Perhaps files were corrupted at the remote end, or revised, or something.."
}
	
if [ -z $1 ]; then #If no arguments are provided, then print out the usage() message
	usage
	exit
fi

#flist=$(rsync --existing --out-format='%f' -n --size-only -e "ssh" --rsync-path="/usr/bin/rsync" ak_data@superdarn-cssdp.usask.ca:/sddata/raw/$YR/ $SD_DATA/$YR)

rsync --existing --delete --out-format="%i :: %n" --size-only -n -r -e "ssh" --rsync-path="/usr/bin/rsync" ak_data@superdarn-cssdp.usask.ca:/sddata/raw/$YR/ $SD_DATA/$YR > $ERROR_FILE

nfiles=$(cat "$ERROR_FILE" | wc -l) 
echo "$nfiles files disagree"

SUB="SD Data Validation Error!"
if [ -s "$ERROR_FILE" ]; then
	echo "Subject: $SUB" > $MAIL_BODY
	echo "This is an automated message generated by the ARSC BigDipper server." >> $MAIL_BODY
	echo "A mismatch has been detected in $nfiles file(s) between the remote mirror and the local file archive." >> $MAIL_BODY
	echo "Files on either the remote mirror or local archive were possibly updated or corrupted."  >> $MAIL_BODY
	echo "Immediate attention to this issue is recommended."  >> $MAIL_BODY
	echo "DETAILED REPORT:" >> $MAIL_BODY
	#echo $flist > $ERROR_FILE
	cat $ERROR_FILE >> $MAIL_BODY
	cat $MAIL_BODY
	#cat $MAIL_BODY | mail $EMAIL_ADDRESS
fi

exit