#Bash Script: get_rem_lnx

Calling convention: get_rem_lnx \<remote-host\>

Used to pull data from remote radar sites via ssh key.
Relies on pre-populate ssh key on remote radar sites for data user.
No password information encoded in script or in resource file

Reads radar specific resource file for radar site specific environment variables
Uses PID based file lock to prevent concurrent runs for a given radar.

Resource filenaming convention: $HOME/.\<remote-host\>.config

Calling Examples:
get_rem_lnx kod-lnx > /tmp/kod_pull.log
get_rem_lnx mcm-lnx > /tmp/mcm_pull.log
get_rem_lnx ksr-lnx > /tmp/ksr_pull.log
get_rem_lnx_new adak-lnx > /tmp/adak_pull.log
get_rem_lnx sps-lnx > /tmp/sps_pull.log


Remote hosts ip addressed defined in /etc/hosts usually.

#Bash Script: get_vt_data

Calling convention: get_vt_data

Used to pull other SuperDARN radar data from vt data archive.
Runs as ak_data user. Relies on pre-seeded ssh key to vt.

 
