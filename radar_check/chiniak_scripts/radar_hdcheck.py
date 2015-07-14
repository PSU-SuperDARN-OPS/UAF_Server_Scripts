import subprocess, pdb, datetime, glob
import signal

TIMEOUT = 40

class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Exception("command timed out")

signal.signal(signal.SIGALRM, alarm_handler)

WARN_THRESHOLD = 95 # warn on 96%+ disk usage

# TODO: warn if no new acfs written
FITACF_TIME = 3 # warn if no new fitacfs written in past 3 hours 
RAWACF_TIME = 3 # warn if no new rawacfs written in past 3 hours

# checks for free disk space

# returns the highest % usage of a hard drive
#HDCHECK = 'df -P | awk {'print $5'} | tail -n +2 | sed 's/.$//' | sort -r -n | head -n 1'
HDCHECKCMD = 'hdcheck' # loaded hdcheck scipt into path on all radars.. 

adak = 'radar@adak-lnx'
kodiak = 'radar@kodiak-lnx'
kingsalmon = 'radar@ks-rst' 
mcmurdo = 'radar@mcm-lnx'
southpole = 'radar@sps-lnx'
chiniak = 'jtklein@chiniak'

def check_hdspace(radar):
    port = 22
    if 'adak' in radar:
        port = 7022

    print 'checking ' + radar + ' disk usage'
    full = []
    signal.alarm(TIMEOUT)
    try:
        s = subprocess.Popen(["ssh", "-p", str(port), radar, '"hdcheck"'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)      
        out, err = s.communicate()

        print radar + 'highest disk usage is ' + out
        if int(out[:-1]) > WARN_THRESHOLD:
            full.append(radar + ' max usage is ' + out) 
    except:
        print radar + ' df error'
        full.append('could not complete ' + radar + ' disk space check, probably network related')
    print full
    signal.alarm(0)
    return full

def check_rawacfs(radar):
    port = 22
    if 'adak' in radar:
        port = 7022

    print 'checking ' + radar + ' rawacf files'
    full = []
    signal.alarm(TIMEOUT)
    try:
        s = subprocess.Popen(["ssh", "-p", str(port), radar, '"rawacf_check"'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)      
        out, err = s.communicate()
        print radar + ' rawacfs: ' + out
        if int(out[:-1]) < 12:
            print 'only ' + out + ' rawacf files written in past 26 hours'
            full.append(radar + ' has only written ' + out[:-1] + ' rawacf files in past 26 hours') 
    except:
        print radar + ' rawacf check error'
        full.append(radar + ' rawacf check error')
    print full

    signal.alarm(0)
    return full

def check_time(radar):
    port = 22
    if radar[0] == 'a':
        port = 7022

    print 'checking ' + radar + ' rawacf files'
    full = []
    signal.alarm(TIMEOUT)
    try:
        s = subprocess.Popen(["ssh", "-p", str(port), radar, '"rawacf_check"'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)      
        out, err = s.communicate()
        print radar + ' rawacfs: ' + out
        if int(out[:-1]) < 12:
            print 'only ' + out + ' rawacf files written in past 26 hours'
            full.append(radar + ' has only written ' + out[:-1] + ' rawacf files in past 26 hours') 
    except:
        print radar + ' rawacf check error'
        full.append(radar + ' rawacf check error')
    print full

    signal.alarm(0)
    return full


def check_slists(radar, ratio = 10):
    port = 22
    if 'adak' in radar:
        port = 7022
    print 'checking ' + radar + ' ratio of good data using port ' + str(port)
    full = []
    signal.alarm(TIMEOUT)
    try:
        s = subprocess.Popen(["ssh", "-p", str(port), radar, '"lagcheck"'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)      
        out, err = s.communicate()
        print radar + ' bad to good lag ratio: ' + out
        if int(out[:-1]) > ratio:
            print 'only one in ' + out + ' lags had quality data in the past day!'
            full.append(radar + ' had only one in ' + out[:-1] + ' lags with quality data in the past day!') 
    except:
        pass
    print full

    signal.alarm(0)
    return full

def check_nscans(radar):
    signal.alarm(TIMEOUT)
    print 'checking ' + radar + ' number of scans running'
    full = []
    try:
        s = subprocess.Popen(["ssh", radar, '"scancheck"'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)      
        out, err = s.communicate()
        print radar + ' number of scans (include grep scan and scancheck..): ' + out
        if int(out[:-1]) > 3:
            print 'too many scans running on ' + radar 
            full.append(radar + ' has too many scans running!')
    except:
	full.append("scan count check failed")
    print full

    signal.alarm(0)
    return full

def check_local_rawacf(radar, hours = 50):
    down = []
    now = datetime.datetime.utcnow()
    checkday = now - datetime.timedelta(hours = hours)
    checkpath = checkday.strftime("/raid0/SuperDARN/data/rawacf/%Y/%m.%d/") + '*' + radar + '*'
    rawacfs = glob.glob(checkpath)
    msg = radar + ' has ' + str(len(rawacfs)) + ' rawacfs in ' + checkpath
    print msg
    if len(rawacfs) == 0:
        print 'failing ' + radar
        down.append(msg)
    return down
    
def check_local_rawacfs():
    down = []
    down += check_local_rawacf('kod', hours = 50)
    down += check_local_rawacf('ade', hours = 38)
    down += check_local_rawacf('adw', hours = 38)
    down += check_local_rawacf('sps', hours = 50)
    down += check_local_rawacf('mcm', hours = 38)
    down += check_local_rawacf('ksr', hours = 38)
    return down


def check_site_hd():
    down = []
    #down += check_hdspace(southpole)
    down += check_hdspace(adak)
    down += check_hdspace(kodiak)
    down += check_hdspace(kingsalmon)
    down += check_hdspace(chiniak)
    down += check_hdspace(mcmurdo)
    return down

def check_sitetime():
    down = []
    #down += check_time(southpole)
    down += check_time(adak)
    down += check_time(kodiak)
    down += check_time(mcmurdo)
    return down


def check_site_rawacf():
    down = []
    #down += check_rawacfs(southpole)
    down += check_rawacfs(adak)
    down += check_rawacfs(kodiak)
    down += check_rawacfs(kingsalmon)
    down += check_rawacfs(mcmurdo)
    return down

def check_site_slists():
    down = []
    #down += check_slists(southpole)
    down += check_slists(adak)
    down += check_slists(kodiak)
    down += check_slists(mcmurdo)
    return down

def check_site_nscans():
    down = []
    #down += check_nscans(southpole)
    return down

if __name__ == '__main__':
    down = check_local_rawacfs()
    print  down

