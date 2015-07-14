from pydmap import DMapFile, timespan, dt2ts, ts2dt

def main():
  import os,datetime 
  print "Test of Dmap"
  print dir(DMapFile)
  print "Opening a dmap filelist"
# Open any number of files.
  dfile=DMapFile(files=["/home/jspaleta/data/fitacf/2012/03.01/20120301.2001.00.mcm.a.fitacf",
    "/home/jspaleta/data/fitacf/2012/03.01/20120301.2201.00.mcm.a.fitacf",]) 
  print "Dmap Files processed"
# Times are in datetime format 
  print dfile.times[0],type( dfile.times[0])
# Time used as record key
  print "Combf from time0 record:", dfile[dfile.times[0]]['combf']
# time used as parameter key
  print "Combf at time0 from parameter time history:",dfile['combf'][dfile.times[0]]
# Setting cache is optional.
  dfile.cache_limit=10
  print "Cache limit",dfile.cache_limit

  print "Comparing record dictionary to variable dictionary"
  times=dfile.times
  print dfile.get_scalars(times[0])
  for t in times:
# Using time as dictionary key to access data record,
    record=dfile[t] 
    print t,record.keys()
  exit(0)
  dfile.purge_cache()
  print "Cache full?",dfile.is_cache_full()
  print "Cache length",len(dfile.cache)
#  h=dfile['tfreq']
#  g=dfile['tfreq']

  del dfile

## More advanced test which for file locator and for handling specific record format verification
## Used in my fitacf and rawacf modules. 
#from filelocator import locate_files
#  variables={
#      'scalars': [
#        'radar.revision.major', 'radar.revision.minor', 'origin.code', 'origin.time', 'origin.command', 'cp', 'stid',  
#        'time.yr', 'time.mo', 'time.dy', 'time.hr', 'time.mt', 'time.sc', 'time.us', 'txpow', 'nave', 'atten', 'lagfr', 
#        'smsep', 'ercod', 'stat.agc', 'stat.lopwr', 'noise.search', 'noise.mean', 'channel', 'bmnum', 'bmazm', 'scan', 
#        'offset', 'rxrise', 'intt.sc', 'intt.us', 'txpl', 'mpinc', 'mppul', 'mplgs', 'nrang', 'frang', 'rsep', 'xcf', 
#        'tfreq', 'mxpwr', 'lvmax', 'rawacf.revision.major', 'rawacf.revision.minor', 'combf', 'thr'
#        ]
#      ,'pulse_arrays': [
#        'ptab','ltab']
#      ,'variable_range_arrays': []
#      ,'index_range_array': ['slist']
#      ,'full_range_arrays': ['pwr0']
#      ,'raw_data_arrays': ['acfd']
#  }
#  required=['slist']
#  rangevar='slist'
#  format='d'
#  pathlist=fitpath=os.environ['SD_RAW_PATH'].strip().split(":")  
#  print pathlist
#  startdate=datetime.datetime(2008,9,1,17)
#  enddate=datetime.datetime(2008,9,1,18)
#  ext=['.rawacf','.rawacf.gz']
#  radarcode='kod'
#  files=locate_files(startdate,enddate,pathlist,ext,radarcode,verbose=True)
#  print files
   
#  dfile=DMapFile(files=files,required=required
#      ,starttime=startdate,endtime=enddate
#      ,rangevar=rangevar,rangearrs=variables['variable_range_arrays']
#      ,format=format)


if __name__ == '__main__':
    main()

