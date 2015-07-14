from pydmap import DMapFile, timespan, dt2ts, ts2dt
from filelocator import locate_files
import os,datetime 
def main():
  import pydmap
  print "Test of Dmap"
  print dir(DMapFile)
  print "Opening a dmap filelist"
  poop=DMapFile(files=[\
    "/home/jspaleta/Desktop/20110108.0602.00.mcm.fitacf",]) 
  print "Dmap Files processed"
  print poop.times[0]
  poop.cache_limit=10
  print "Cache limit",poop.cache_limit
  for var in poop.get_scalars(poop.times[0]):
    h=poop[var]
    g=poop[var]
    for t in h:
      if h[t]!=g[t]: 
        print "%s Problem at time:" % (var),t
        print h[t],g[t]
  poop.purge_cache()
  print "Cache full?",poop.is_cache_full()
  print "Cache length",len(poop.cache)
  h=poop['tfreq']
  g=poop['tfreq']
  print poop['combf'][poop.times[0]]

  del poop
#  poop=DMapFile(files=[
#    "/home/jspaleta/Data/SuperDARN/data/fit/2008/08.12/20080812.1720.11.kod.fitacf",
#    ])
#
#  del poop

  variables={
      'scalars': [
        'radar.revision.major', 'radar.revision.minor', 'origin.code', 'origin.time', 'origin.command', 'cp', 'stid',  
        'time.yr', 'time.mo', 'time.dy', 'time.hr', 'time.mt', 'time.sc', 'time.us', 'txpow', 'nave', 'atten', 'lagfr', 
        'smsep', 'ercod', 'stat.agc', 'stat.lopwr', 'noise.search', 'noise.mean', 'channel', 'bmnum', 'bmazm', 'scan', 
        'offset', 'rxrise', 'intt.sc', 'intt.us', 'txpl', 'mpinc', 'mppul', 'mplgs', 'nrang', 'frang', 'rsep', 'xcf', 
        'tfreq', 'mxpwr', 'lvmax', 'rawacf.revision.major', 'rawacf.revision.minor', 'combf', 'thr'
        ]
      ,'pulse_arrays': [
        'ptab','ltab']
      ,'variable_range_arrays': []
      ,'index_range_array': ['slist']
      ,'full_range_arrays': ['pwr0']
      ,'raw_data_arrays': ['acfd']
  }
  required=['slist']
  rangevar='slist'
  format='d'
  pathlist=fitpath=os.environ['SD_RAW_PATH'].strip().split(":")  
  print pathlist
  startdate=datetime.datetime(2008,9,1,17)
  enddate=datetime.datetime(2008,9,1,18)
  ext=['.rawacf','.rawacf.gz']
  radarcode='kod'
  files=locate_files(startdate,enddate,pathlist,ext,radarcode,verbose=True)
#  print files
   
#  poop=DMapFile(files=files,required=required
#      ,starttime=startdate,endtime=enddate
#      ,rangevar=rangevar,rangearrs=variables['variable_range_arrays']
#      ,format=format)


if __name__ == '__main__':
    main()

