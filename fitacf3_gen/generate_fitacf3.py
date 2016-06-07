#!/usr/bin/python2.6
# python script to trawl rawacfs on kodiak and generate fitacf3s
# hardcoded to run on kodiak.gi.alaska.edu
# mit license

import datetime
import glob
import os 
import pdb

OVERWRITE_FITACF3 = False 

RAWACF_PATH_BASE = '/raid/SuperDARN/data/rawacf/'
FITACF3_PATH_BASE = '/raid/SuperDARN/data/fit3/'
RADAR = '*' # flag to narrow down radars

# (Y, M, D) start and end dates to convert
START_DATE = datetime.date(2016, 1, 1)
END_DATE = datetime.date(2016, 5, 1)

MAKE_FIT = '/home/fitacf_test/repos/fitacf.3.0/bin/make_fit'
FITACF3_EXT = 'fitacf'

current_date = START_DATE 

while current_date < END_DATE:
	day_path = '/{0}/{1}.{2}/'.format(current_date.year,str(current_date.month).zfill(2),str(current_date.day).zfill(2))

	rawacfs = glob.glob(RAWACF_PATH_BASE + day_path + RADAR)
	

	if not os.path.exists(FITACF3_PATH_BASE + day_path):
		os.makedirs(FITACF3_PATH_BASE + day_path)

	for rawacf in rawacfs:
		fitacf3_filename = rawacf.split('/')[-1]
		cat_command = 'cat'

		if 'bz2' in fitacf3_filename:
			fitacf3_filename = fitacf3_filename[:-4]
			cat_command = 'bzcat'

		if 'gz' in fitacf3_filename:
			fitacf3_filename = fitacf3_filename[:-3]
			cat_command = 'zcat'
			
		fitacf3_filename = fitacf3_filename[:-6] + FITACF3_EXT
		fitacf3_filename = FITACF3_PATH_BASE + day_path + fitacf3_filename
		if OVERWRITE_FITACF3 or (not os.path.isfile(fitacf3_filename)):			
			print('generating ' + fitacf3_filename)
			cat_cmd = ' '.join([cat_command, rawacf])
			fit_cmd = ' '.join([MAKE_FIT, '-new', '>' + fitacf3_filename])
			cmd = '{0} | {1}'.format(cat_cmd, fit_cmd)

			print cmd
			os.system(cmd)
		else:
			print(fitacf3_filename + ' exists, skipping (overwrite by setting OVERWRITE_FITACF3 to True)')

	current_date += datetime.timedelta(days=1)	
