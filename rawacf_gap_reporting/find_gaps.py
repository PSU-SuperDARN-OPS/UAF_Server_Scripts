# python script to compare data gaps for SuperDARN rawacfs 
# jon klein, jtklein@alaska.edu
# 03/2014

# requires dmapdump and write permissions to /tmp

# assumes saskatoon data gap files are in the format [radar].txt
# for example, ade.a.txt
# gap file contents are in the following format:
#20120318.14.rkn  --  20120318.22.rkn 
#20120319.00.rkn  --  20120319.14.rkn 
#20120321.16.rkn  -- 
#Means that there are no rawacf data files during the time period March 18th, at 14:00 UTC to March 19th at 14:00 UTC. 
#Then there are data files for March 19th 16:00 UTC until March 21st at 14:00 UTC. And the data file for March 21st at 1600 is missing. 

# modify main() to taste to change radars and the date range covered by the gap reports

# step zero, pass in date ranges, data path, and gap reports
# step one, read in gap information from saskatoon gap reports
# step two, read gaps from rawacf archives
# step three, compare and generate report...

import glob
import datetime
import subprocess, os, shutil
import pdb

GAP_TOLERANCE = datetime.timedelta(hours = 3)

SD_DATA_PATH = '/raid0/SuperDARN/data/fit/' # root directory for FitACF files
SAK_GAP_DIR = './cangaps/' # folder with gap reports for usask
TMP_DIR = '/tmp/gaptmp' # temporary directory for storing decompressed files (because jef gets mad when we decompress in place)

# looks through a saskatoon gap report, creates a dictionary with gaps
def read_gap_report(filename):
    gapfile = open(filename, 'r')

    gaps = {}

    radar = filename.split('/')[-1][:-4]
    for line in gapfile:
        gap = line[:-1].split('  --  ')
        if not gap[0]:
            continue
        # if the gap only exists for one time, set the end time as the start time
        # eg, for the case 20120321.16.rkn  -- 
        if not gap[-1]:
            gap[-1] = gap[0]
        gaps[_fname_to_time(gap[0], radar)] = _fname_to_time(gap[-1], radar)
         
    return radar, gaps

# merge gaps smaller than threshold
def _merge_gaps(gaps, threshold = GAP_TOLERANCE):
    merged_gaps = {}
    sgaps = sorted(gaps.keys())

    gapstart = ''
    for (i, sgap) in enumerate(sgaps):
        if not gapstart:
            gapstart = sgap

        gapend = gaps[sgap]
        if i+1 < len(sgaps) and sgaps[i+1] - gapend < threshold:
            continue

        merged_gaps[gapstart] = gapend
        gapstart = ''
    return merged_gaps

def _round_gaps(gaps):
    rounded_gaps = {}
    for gap in gaps.keys():
        rounded_gaps[_round_to_hour(gap)] = _round_to_hour(gaps[gap])
    return rounded_gaps

def _fname_to_time(name, radar):
    return datetime.datetime.strptime(name, '%Y%m%d.%H.' + radar)

# gap reports provided rounded to the nearest hour..
def _round_to_hour(dt):
    if dt.minute > 29:
        dt += datetime.timedelta(hours = 1)
    return datetime.datetime(year = dt.year, month = dt.month, day = dt.day, hour = dt.hour)

# looks through FitACF files and creates a gap dictionary
# given radar name (ade.a) starting and ending datetimes t0 and t1
def create_gap_report(radar, t0, t1 = datetime.date.today(), gapthresh = datetime.timedelta(minutes = 20)):
    records = []
    recordlens = []
    gaps = {}
    # create iterator glob across input date range, track record tmes and record lengths
    # no obivous way of expanding python iglobs over multi-digit ranges... manually run over each year
    years = range(t0.year, t1.year+1, 1)
    for y in years:
        pathexpr = '{path}/{y}/*/*{radar}*'.format(path=SD_DATA_PATH, y = y, sm = t0.month, em = t1.month, sd = t0.day, ed = t0.day, radar = radar)
	print 'looking in ' + pathexpr
        itr = glob.iglob(pathexpr)
        i = 0
        for record in itr:
            rname = record.split('/')[-1].split('.' + radar)[0]
            rdate = datetime.datetime.strptime(rname,'%Y%m%d.%H%M.%S')
            if rdate >= t0 and rdate <= t1:
                i += 1
                records.append(rdate)
                recordlens.append(record_len(record))
    
    # sort record lengths (because the iterator hops through time..)
    recordlens = [x for y, x in sorted(zip(records, recordlens))]
    records.sort()
   
    # compute missing data times, create gap dictionary for gaps longer than threshold (default 10 minutes) 
    rdeltas = [records[i+1] - (records[i] + recordlens[i]) for i in range(len(records)-1)]
    for (i, delta) in enumerate(rdeltas):
        if (delta) > gapthresh:
            gaps[records[i] + recordlens[i]] = records[i+1] # create gap from end of record to start of next record
    
    return gaps

def compare_gaps(sask_gaps, gaps):
    zerosec = datetime.timedelta(seconds = 0)

    # merge and round gaps
    sask_gaps = _merge_gaps(sask_gaps)
    gaps = _merge_gaps(gaps)
    gaps = _round_gaps(gaps)

    gap_start = sorted(gaps.keys())
    gap_sask_start = sorted(sask_gaps.keys())
    
    # print gaps in sask report not found in report searching our data
    for sgap in gap_sask_start:
        gapdiff = [abs(sgap - g) for g in gap_start]
        neighborgap = gap_start[gapdiff.index(min(gapdiff))]
        neighborgapend = gaps[neighborgap]
        if ((abs(sgap - neighborgap) < zerosec) or (min(gapdiff) < GAP_TOLERANCE)) and ((abs(sask_gaps[sgap] - neighborgapend) < GAP_TOLERANCE) or ((neighborgapend - sgap) > zerosec)):
            print 'gap ' + str(sgap) + ' matched to gap ' + str(neighborgap)
            continue
        else:
            print 'unknown gap detected at ' + str(sgap) + ' (closest match was: ' + str(neighborgap) + ' ) '

    #print 'gaps:'
    #for gap in gap_start:
        #print str(gap) + ' to ' + str(gaps[gap])

    return 0

# uses dmapdump to find the last record time in a file
# assumes that records are stored sequentially (this is a bad idea) 
# this is terrible, but pydmap was acting wonky on chiniak/odiak..
def record_len(recordfile):
    # if the file is compressed... decompress to temp dir
    tmpfile = False

    if recordfile[-7:] != '.fitacf':
#       print recordfile
        tmpfile = True
        filename = recordfile.split('/')[-1]
       	recordfile_tmp = TMP_DIR + '/' + os.path.splitext(filename)[0]
	#pdb.set_trace()
        if os.path.isfile(recordfile_tmp):
	        pass

        else:
                try: 
                    os.makedirs(TMP_DIR)
                except OSError:
                    if not os.path.isdir(TMP_DIR):
                        raise
		print 'copying ' + recordfile + ' to ' + TMP_DIR

                shutil.copy(recordfile, TMP_DIR)
                if '.bz2' in filename:
                    decomp = subprocess.call(['bunzip2', TMP_DIR + '/' + filename], stdout=subprocess.PIPE)
                elif '.gz' in filename:
                    decomp = subprocess.call(['gunzip', TMP_DIR + '/' + filename], stdout=subprocess.PIPE)
                else:
                    raise NotImplementedError('Unsupported compresstion type for file ' + str(recordfile))
    else:
        recordfile_tmp = recordfile 
    pdmap = subprocess.Popen(['dmapdump', recordfile_tmp], stdout=subprocess.PIPE)
    pgrep = subprocess.Popen(['grep', 'time'], stdin = pdmap.stdout, stdout=subprocess.PIPE)
    pdmap.stdout.close()
    ret = pgrep.communicate()
    lines = ret[0].split('\n')
    
    # ignore small files 
    if len(lines) > 100:
        # I feel horrible about this..  parse dmapdump output for times
        # can't use origin.time, because ade (and everybody but mcm, sps, kod, ksr?) doesn't change for every integration time
        # assumes dmap file time is monotonically increasing, this should approximately be true 
        tstart = tuple([int(l.split(' = ')[-1]) for l in lines[1:7]])
        tend = tuple([int(l.split(' = ')[-1]) for l in lines[-8:-2]])
        
        #if tmpfile:
        #    os.remove(recordfile)
        try:
            tdiff = datetime.datetime(*tend) - datetime.datetime(*tstart)
        except:
            pdb.set_trace()
    else:
        tdiff = datetime.timedelta(seconds = 0)
    return tdiff 

if __name__ == '__main__':
    radars = ['mcm.a', 'mcm.b', 'ade.a', 'adw.a', 'kod.c', 'kod.d', 'sps.a']

    t0 = datetime.datetime(year=2015,month=1,day=1,hour=0) 
    t1 = datetime.datetime(year=2015,month=9,day=1,hour=0)
    
    for r in radars:
        print 'checking radar: ' + r
        radar, cangaps = read_gap_report('./cangaps/' + r + '.txt')
        gaps = create_gap_report(r, t0, t1)
        compare_gaps(cangaps, gaps)

        # remove decompressed acfs
        #files = glob.glob(TMP_DIR + '/*')
        #for f in files:
        #    os.remove(f)
