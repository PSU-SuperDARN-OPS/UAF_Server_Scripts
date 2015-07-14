import os

dir='/raid/hold/'
datadir="/raid/SuperDARN/data/"
exts=["rawacf","fitacf"]
old_exts=['fit','inx']
missing=[]
unknown=[]
for root, dirs, files in os.walk(dir):
  for name in files:
    #print root, name
    seen=False
    for ext in exts:
      if not seen:
        rawdir=os.path.join(datadir,ext)
        #print rawdir 
        if ext in name:
          seen=True
          segments=name.split('.')
          yr=int(segments[0][0:4])
          mo=int(segments[0][4:6])
          dy=int(segments[0][6:8])
          path=rawdir+"/%04d/%02d.%02d/" % (yr,mo,dy)
          fname=os.path.join(path,name)
          #print root, name, fname 
          if os.path.isfile(fname):
          #print name+" exists!"
            pass
          else: 
            #print name+" does not exist ",fname
            if segments[-1] in ["bz2","gz"]:
              bname=".".join(segments[0:-1])
              fname=os.path.join(path,bname)
              #print "Trying "+bname+" "+fname 
              if os.path.isfile(fname):
                pass
              else:  
                print name+ " does not exist!"
                missing.append(os.path.join(root,name))
            else:
              print name+ " does not exist!"
              missing.append(os.path.join(root,name))
    for ext in old_exts:
      if not seen:
        fext=ext
        if ext=="inx": fext='fit'
        rawdir=os.path.join(datadir,fext)
        #print rawdir 
        if ext in name:
          seen=True
          segments=name.split('.')
          yr=int(segments[0][0:4])
          mo=int(segments[0][4:6])
          dy=int(segments[0][6:8])
          path=rawdir+"/%04d/%02d.%02d/" % (yr,mo,dy)
          fname=os.path.join(path,name)
          if os.path.isfile(fname):
            pass
          else: 
            if segments[-1] in ["bz2","gz"]:
              bname=".".join(segments[0:-1])
              fname=os.path.join(path,bname)
              #print "Trying "+bname+" "+fname 
              if os.path.isfile(fname):
                pass
              else:  
                print name+ " does not exist!"
                missing.append(os.path.join(root,name))
            else: 
              print name+ " does not exist! ",fname
              missing.append(os.path.join(root,name))
    if not seen: 
      print "File: %s unknown data type" % name
      unknown.append(os.path.join(root,name))
      
print "\nMissing Files:"
for file in missing:
  print file 
print "\nUnknown Files:"
for file in unknown:
  print file 
