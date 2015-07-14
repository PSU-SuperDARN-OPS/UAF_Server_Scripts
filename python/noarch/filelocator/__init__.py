#fitpath=os.environ['SD_FITROPEN_PATH'].strip().split(":")
#rawpath=os.environ['SD_RAWROPEN_PATH'].strip().split(":")
#datpath=os.environ['SD_RAWROPEN_PATH'].strip().split(":")
#fitext=['.fitacf','.fitacf.gz']
#rawext=['.rawacf','.rawacf.gz']
#datext=['.dat','.dat.gz']
import os,datetime

def locate_files(starttime,endtime=None,pathlist=["."],extlist=['.fitacf','.fitacf.gz'],radarcode='kod',
                 walk=False,verbose=True):
  from string import join
  from dmap import timespan, dt2ts
  stid=radarcode.split('.')[0]
  try:
    channel=radarcode.split('.')[1]
  except:
    channel=''
  print "<%s> <%s> %d" % (stid, channel,len(channel))
  pathlist.reverse()
  extlist.reverse()
  prevtime=starttime-datetime.timedelta(days=1)
  if endtime is None: endtime=starttime+datetime.timedelta(days=1)
  goodfiles={}
  for path in pathlist:
    if not walk:
      dt=endtime-prevtime
      for i in range(dt.days+1):
        activedate=starttime+datetime.timedelta(i)
        ystr=activedate.strftime("%Y")
        mstr=activedate.strftime("%m")
        dstr=activedate.strftime("%d")
        activedir=path+"/%s/%s.%s/" % (ystr,mstr,dstr) 
        if verbose: print "Active Directory:", activedir
        if os.path.exists(activedir):
          for f in os.listdir(activedir):
            base=os.path.basename(f).split('.')
            if len(base) > 3:
              if base[3].lower()==stid.lower():
                if ((channel is None) or (len(channel)==0)) or ((len(channel) != 0) and (base[4].lower()==channel.lower())): 
                    filedate=datetime.datetime(int(base[0][0:4]),int(base[0][4:6]),int(base[0][6:8]),
                      int(base[1][0:2]),int(base[1][2:4]),int(base[2]),tzinfo=None) 
                    if filedate>prevtime and filedate<endtime:
                      for ext in extlist:
                        ext_segs=len(ext.split('.'))-1 
                        tmpfile=activedir+'/'+join(base[0:-ext_segs],'.')+ext 
                        if os.path.exists(tmpfile): 
                          goodfiles[filedate]=tmpfile
                        del tmpfile
                    del filedate
            del base
    else:  
        if verbose: print "Active Path:", path
        for (p, dirs, files) in os.walk(path):
          for f in files:
#            print f
            base=os.path.basename(f).split('.')
            if len(base) > 3:
              if base[3].lower()==stid.lower():
                if ((channel is None) or (len(channel)==0)) or ((len(channel) != 0) and (base[4].lower()==channel.lower())): 
                    filedate=datetime.datetime(int(base[0][0:4]),int(base[0][4:6]),int(base[0][6:8]),
                      int(base[1][0:2]),int(base[1][2:4]),int(base[2])) 
                    if filedate>prevtime and filedate<endtime:
                      for ext in extlist:
                        ext_segs=len(ext.split('.'))-1 
                        tmpfile=p+'/'+join(base[0:-ext_segs],'.')+ext 
                        if os.path.exists(tmpfile): 
                          goodfiles[filedate]=tmpfile
                        del tmpfile
                    del filedate
            del base

  finallist=[]
  for filedate,f in goodfiles.items():  
#    print filedate,f
    start,end=timespan(f,'d')
    if (start<endtime) and (end >starttime):
      finallist.append(f)
  return finallist

def main():
  hmm=locate_files(datetime.datetime(2013,3,1,2),datetime.datetime(2013,3,1,3),
    pathlist=['/raid/SuperDARN/data/fit/'],
#    pathlist=['/tmp/','/home/jspaleta/Data/SuperDARN/data/fit/'],
#    walk=True,
    verbose=True,radarcode='kod.c'
       )
  print hmm
if __name__ == '__main__':
    main()

