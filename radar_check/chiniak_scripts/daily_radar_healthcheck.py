import datetime, pickle
from emaillib import *
from radar_ping import *
from radar_streamcheck import *
from radar_hdcheck import *
from remote_command import adak_ddscheck, timechecks, qnx_roschecks, twohourchecks, fitacftimes

SUBJECT = 'SuperDARN Status Update: '
EMAIL_TARGET = 'jtklein@alaska.edu'
EMAIL_CC = ''
TIMEOUT = 10#4 * 60

comments = []

try:
	print 'ros process check...'
	roscheck = qnx_roschecks()

except:
	roscheck = ['could not complete ros process check, probably network related']
	print roscheck

try:
	print 'two hour check...'
	twohour = twohourchecks()
	print twohour
except:
	twohour = ['could not complete two hour check, probably network related']
	print twohour

try:
	print 'fitacf write time check...'
	fittime = fitacftimes ()
	print fittime 
except:
	twohour = ['could not complete fitacf write time check, probably network related']
	print fittime 

try:
	print 'dds low power check...'
	adakdds = adak_ddscheck()
except:
	adakdds = ['could not complete adak dds check, probably network related']
	print adakdds
try:
	print 'radar clock check...'
	radar_times = timechecks()
except:
	radar_times = ['could not complete kodiak time skew check, probably network related']
	print radar_times
try:
	print 'data quality check...'
	lagchecks = check_site_slists()
except:
	lagchecks = ['could not complete nlag/slist ratio check, probably network related']
	print lagchecks
try:
	print 'rawacf number check...'
	acfchecks = check_site_rawacf()
except:
	acfchecks = ['could not count remote rawacfs, probably network related']
	print acfchecks
try:
	print 'hard disk check...'
	diskchecks = check_site_hd()
except:
	diskchecks = ['could not complete disk checks, probably network related']
	print diskchecks

try:
	print 'radar stream check...'
	downstreams = check_radar_streams()
except:
	downstreams = ['could not complete radar realtime stream check']
	print downstreams

try:
	print 'radar ping check...'
	downpings = check_sites()
except:
	downpings = ['could not complete ping check..']
	print downpings

try:
	print 'south pole number of scans check...'
	scancount = check_site_nscans()
except:
	scancount = ['could not complete south pole scan check']
	print scancount
try:
	print 'checking for local rawacfs'
	localrawacf = check_local_rawacfs()
except:
	localrawacf = ['could not complete local nfs rawacf check, this is bad..']
	print localrawacf

# send alert if anyone other than south pole is down
send_email = False

# send email if anyone other than south pole isn't streaming data
if len(downpings) + len(downstreams) > 0 and sum([not s.startswith('sp') for s in downstreams]) :
    print "sending email - stream down" 
    send_email = True

# send email if you can't ping a computer that isn't south pole 
if len(downpings) - sum([s.startswith('sp') for s in downpings]):
    print "sending email - can't ping computer" 
    send_email = True

# send email if a computer has a full hard drive
if len(diskchecks) > 0: 
    print 'sending email - full hard drive'
    send_email = True

# send email if a computer no new rawacfs 
if len(acfchecks):#- (sum([s.startswith('sp') for s in downpings]) > 0):
    print 'sending email - no new rawacfs'
    send_email = True

# send email if rawacfs haven't made it back 
if len(localrawacf):
    print 'sending email - missing local rawacfs '
    send_email = True

if len(lagchecks):
    print 'sending email - possible bad data..'
    send_email = True

if len(scancount):
    print 'sending email - south pole with crazy with scans again...'
    send_email = True

if sum([s.startswith('sp') for s in downpings]) == 1:
    comments.append('SPS trouble, can only reach one of sps-lnx or sps-qnx..')
    print 'sending email, only one of sps-lnx or sps-qnx is down'
    send_email = True

# send email if you can ping south pole computers, but the data stream is down
if sum([s.startswith('sp') for s in downstreams]) and not sum([s.startswith('sp') for s in downpings]):
    comments.append('SPS trouble, I can reach the computers but the stream is down...')
    print "sending email - can't ping computer" 
    send_email = True

if send_email:
    body = 'SuperDARN Network Status, ' + str(datetime.datetime.now()) + '\n\n'
    body += '\n'.join(comments) + '\n\n'
    if downstreams:
        body += 'The following real-time data streams are probably down:\n'
        body += '\n'.join(downstreams) + '\n\n'

    if downpings:
        body += 'The following computers are inaccessible:\n'
        body += '\n'.join(downpings) + '\n\n'

    if diskchecks:
        body += 'The following computers may have nearly full disks:\n'
        body += '\n'.join(diskchecks) + '\n\n'

    if acfchecks:
        body += 'The following computers wrote less than 12 rawacf files in the past 26 hours:\n'
        body += '\n'.join(acfchecks) + '\n\n'

    if lagchecks:
        body += 'The following computers did not have many quality fits in the past day:\n'
        body += '\n'.join(lagchecks) + '\n\n'

    if scancount:
        body += 'The following computers had too many scans running..:\n'
        body += '\n'.join(scancount) + '\n\n'

    if adakdds:
        body += 'The following adak dds checks failed:\n'
	body += '\n'.join(adakdds) + '\n\n'

    if radar_times:
        body += 'The following radars have skewed clocks:\n'
	body += '\n'.join(radar_times) + '\n\n'

    if roscheck:
        body += 'The following radars failed ros process checks:\n'
	body += '\n'.join(roscheck) + '\n\n'

    if twohour:
        body += 'The following radars failed two hour check of slist/nlag ratio..:\n'
	body += '\n'.join(twohour) + '\n\n'
	
    if fittime:
        body += 'The following radars have not written fitacfs recently..:\n'
	body += '\n'.join(fittime) + '\n\n'

    if localrawacf:
        body += 'The following radars have not had rawacfs pulled recently..:\n'
	body += '\n'.join(localrawacf) + '\n\n'





    body += '\n\n\n-chiniak'
    subject = SUBJECT + ' ' + ' '.join(downstreams) + ' Down'

    email_notice(subject, body, EMAIL_TARGET, EMAIL_CC)

