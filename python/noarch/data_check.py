def uniq_list(seq, idfun=None): 
  # order preserving
  if idfun is None:
       def idfun(x): return x
  seen = {}
  result = []
  for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
  return result

def check_for_updates(stid,channel,plot_directory=None,date=None,year=None,prev_days=90,data_directory=None,force=False):
  import os
  import datetime
  date_list=[]
  prev_date=datetime.datetime.utcnow()-datetime.timedelta(days=prev_days)
  if plot_directory is None: plot_dirstub="/tmp/daily_plots"
  else : plot_dirstub=plot_directory
  if data_directory is None: dirtree_to_check="/raid/SuperDARN/data/fit"
  else : dirtree_to_check=data_directory
  if date is None:
    if year is not None: 
      dirtree_to_check+="/%04d" % year
  else: dirtree_to_check+="/%04d/%02d.%02d" % (date.year,date.month,date.day)
  print dirtree_to_check
  for (p, dirs, files) in os.walk(dirtree_to_check):
    for f in files:
      filedate=None
      base=os.path.basename(f).split('.')
      if len(base) > 3:
        if base[3].lower()==stid.lower():
          if ((channel is None) or (len(channel)==0)) or ((len(channel) != 0) and (base[4].lower()==channel.lower())): 
            filedate=datetime.datetime(int(base[0][0:4]),int(base[0][4:6]),int(base[0][6:8]),tzinfo=None) 
            #print base, filedate
            path=os.path.join(p,f)
            if os.path.isfile(path):
              datafile_mtime=datetime.datetime.utcfromtimestamp(os.path.getmtime(path))
              if datafile_mtime > prev_date:
                if force: date_list.append(filedate.date()) 
                else:
                  plotdir=os.path.join(plot_dirstub,"%04d" % filedate.year,"%02d.%02d" % (filedate.month,filedate.day))
                  if not os.path.isdir(plotdir):
                    plotdir=os.path.join(plot_dirstub,"%02d.%02d" % (filedate.month,filedate.day))
                  if os.path.isdir(plotdir):
                    plotdir_mtime=datetime.datetime.utcfromtimestamp(os.path.getmtime(plotdir))
                  else: plotdir_mtime=datafile_mtime
                  if datafile_mtime >= plotdir_mtime:
                    date_list.append(filedate.date()) 
                  else : 
                    print "Existing plot directory is newer:",plotdir,path,datafile_mtime,plotdir_mtime
                    if force: date_list.append(filedate.date()) 
                    pass
                pass
      pass
      del filedate,base
  date_list.sort()
  return uniq_list(date_list)


if __name__== "__main__":
  import datetime
  date=datetime.datetime(2012,3,1)
  print len(check_for_updates("kod","d",date=date,plot_directory="/tmp/daily_plots",year=2012,prev_days=10,force=True))

