#!/usr/bin/bash
YR=2015

nfiles=$(rsync -i -n -a --no-perms -O \
	-f"+ ${YR}/" \
	-f"+ ${YR}/*/" \
	-f"+ *ade*rawacf*" \
	-f"+ *adw*rawacf*" \
	-f"+ *kod*raw*" \
	-f"+ *koa*raw*" \
	-f"+ *koc*raw*" \
	-f"+ *kob*raw*" \
	-f"+ *ksr*raw*" \
	-f"+ *mcm*raw*" \
	-f"+ *sps*raw*" \
	-f"- *" -e "ssh" \
	--rsync-path="/usr/bin/rsync" \
	jtklein@chiniak.gi.alaska.edu:/raid0/SuperDARN/data/rawacf/ \
	/sam-qfs/SUPERDARN/ak_radar_data/rawacf/ | wc -l)
echo "Number of files to archive: $nfiles"
rsync -i -a --no-perms -O \
	-f"+ ${YR}/" \
	-f"+ ${YR}/*/" \
	-f"+ *ade*rawacf*" \
	-f"+ *adw*rawacf*" \
	-f"+ *kod*raw*" \
	-f"+ *koa*raw*" \
	-f"+ *koc*raw*" \
	-f"+ *kob*raw*" \
	-f"+ *ksr*raw*" \
	-f"+ *mcm*raw*" \
	-f"+ *sps*raw*" \
	-f"- *" -e "ssh" \
	--rsync-path="/usr/bin/rsync" \
	jtklein@chiniak.gi.alaska.edu:/raid0/SuperDARN/data/rawacf/ \
	/sam-qfs/SUPERDARN/ak_radar_data/rawacf/
echo "Changing permissions.."
chmod -R g+rwx  /sam-qfs/SUPERDARN/ak_radar_data/rawacf/$YR
echo "Number of files archived: $nfiles"
