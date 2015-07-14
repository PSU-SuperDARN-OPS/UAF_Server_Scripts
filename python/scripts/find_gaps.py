# python script to compare data gaps
# jon klein, jtklein@alaska.edu

# assumes saskatoon data gap files are in the format [radar].txt
# for example, ade.a.txt
# gap file contents are in the following format:
#20120318.14.rkn  --  20120318.22.rkn 
#20120319.00.rkn  --  20120319.14.rkn 
#20120321.16.rkn  -- 
#Means that there are no rawacf data files during the time period March 18th, at 14:00 UTC to March 19th at 14:00 UTC. 
#Then there are data files for March 19th 16:00 UTC until March 21st at 14:00 UTC. And the data file for March 21st at 1600 is missing. 


# step zero, pass in date ranges, data path, and gap reports
# step one, read in gap information from saskatoon gap reports
# step two, read gaps from fitacf archives
# step three, compare and generate..
import glob
import datetime
import subprocess
from pydarn.dmap import DMapFile

SD_DATA_PATH = '/raid0/SuperDARN/data/fit'

# looks through a saskatoon gap report, creates a dictionary with gaps
def read_gap_report(filename):
    gapfile = open(filename, 'r')

    gaps = {}

    radar = filename[:-4]
     
    for line in gapfile:
        gap = line[:-1].split('  --  ')
        # if the gap only exists for one time, set the end time as the start time
        # eg, for the case 20120321.16.rkn  -- 
        if not gaps[-1]:
            gaps[-1] = gaps[0]

        gaps[gap[0]] = gap[-1] 
    
    return radar, gaps

# looks through FitACF files and creates a gap dictionary
# given radar name (ade.a) starting date t0 and end date t1
def create_gap_report(radar, t0, t1 = datetime.date.today(), gapthresh = datetime.timedelta(hours = 2, minutes = 5)):
    records = []
    recordlens = []
    # create iterator glob across input date range
    # no obivous way of expanding python iglobs over multi-digit ranges... manually run over each year
    years = range(t0.year, t1.year+1, 1)
    for y in years:
        pathexpr = '{path}/{y}/*/*{radar}*'.format(path=SD_DATA_PATH, y = y, sm = t0.month, em = t1.month, sd = t0.day, ed = t0.day, radar = radar)
        itr = glob.iglob(pathexpr)
        
        for record in itr:
            rname = record.split('/')[-1].split('.' + radar)[0]
            rdate = datetime.datetime.strptime(rname,'%Y%m%d.%H%M.%S')
            if rdate >= t0 and rdate <= t1:
                records.append(rdate)
                pdb.set_trace()
                

    records.sort()
    
    rdeltas = [records[i+1] - records[i] for i in range(len(records)-1)]

    for (i, delta) in enumerate(rdeltas):
        if delta > gapthresh:
            print str(records[i]) + ' gap ' + str(delta)

    pdb.set_trace() 

    return gaps

def compare_gaps(gaps1, gaps2):
    return 0

# uses dmapdump to find the last record time in a file
# assumes that records are stored sequentially (this is a bad idea) 
def record_len(recordfile):
    dfile = DMapFile(files=[recordfile])
    times = dfile.times.sort()
    return times[-1] - times[0]

if __name__ == '__main__':
    t1 = datetime.datetime.today() 
    t0 = t1 - datetime.timedelta(days = 365)

    create_gap_report('ade.a', t0, t1)

