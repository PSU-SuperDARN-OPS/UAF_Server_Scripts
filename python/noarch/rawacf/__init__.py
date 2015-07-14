from libfitacf import get_badlags as get_lagstate
import scipy.linalg.basic as basic
import lomb
import os,datetime
import numpy as N
import sys
try: import numpy.core.ma as MA
except: import numpy.ma as MA

class RawACF:
  def __del__(self):
#    for f in self.fileobjects:
#      f.close()
    pass
  def __init__(self,startdate=datetime.datetime(2011, 10, 01,0,0,0)
    ,enddate=None,filelist=None,directory=None,pathlist=None,verbose=False,radarcode='mcm',timeformat='f'):
    from filelocator import locate_files
    from dmap import DMapFile
    self._verbose=verbose
    if pathlist is None: self._pathlist=fitpath=os.environ['SD_RAWROPEN_PATH'].strip().split(":")
    else: self._pathlist=pathlist
    self._ext=['.rawacf','.rawacf.gz']
    if radarcode is None: self.radarcode='mcm'
    else: self._radarcode=radarcode
    self._variables={
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
    self._required=['slist']
    self._rangevar='slist'
    if timeformat is None: self._format='d'
    else: self._format=timeformat
    self.startdate=startdate
    if enddate is None : self.enddate=startdate+datetime.timedelta(days=1)
    else : self.enddate=enddate
    if directory is not None: self._pathlist.append(directory)
    if filelist is None: 
      self.files=locate_files(self.startdate,self.enddate,self._pathlist,self._ext,self._radarcode,verbose=verbose)
    else:
      if type(filelist)==type([]): self.files=filelist
      else: self.files=[filelist]
#    print self._pathlist
#    print self.files
    self.data=DMapFile(files=self.files,required=self._required
      ,starttime=self.startdate,endtime=self.enddate
      ,rangevar=self._rangevar,rangearrs=self._variables['variable_range_arrays']
      ,format=self._format)
    self.cache={}
    self.lomb_phi_data={}
    self.current_time=None
  def purge_cache(self,varname=None):
    if varname==None:
      return self.data.purge_cache()
    else:
      return self.data.purge_cache(varname)

  def set_current_time(self,key):
   self.current_block=self.data[key]
   self.current_time=key

  def clear_current_time(self,key):
   self.current_block={}
   self.current_time=None

  def acf_real(self,key,item):
     if key is not None:
       if key != self.current_time:
         self.set_current_time(key)

     if self.current_time is not None: 
#       item=self.current_block['slist'].index(bin)
       numlags=self.current_block['mplgs']
       lenlist=len(self.current_block['slist'])
       lenacf=lenlist*numlags*2
       numofpoints=numlags*2
       if lenacf == len(self.current_block['acfd']) and lenlist != 0:
         real_acf=self.current_block['acfd'][item*numofpoints:(item+1)*numofpoints:2]
         if len(real_acf)!=numlags:
           print "Re acf has wrong length",len(real_acf), numlags
         return real_acf
       else: 
         print "Error parsing Re acf",lenlist,numlags,lenlist*numlags*2,len(self.current_block['acfd'])
         return None

  def acf_imag(self,key,item):
     if key is not None:
       if key != self.current_time:
         self.set_current_time(key)

     if self.current_time is not None: 
#       item=self.current_block['slist'].index(bin)
       numlags=self.current_block['mplgs']
       lenlist=len(self.current_block['slist'])
       lenacf=lenlist*numlags*2
       numofpoints=numlags*2
       if lenacf == len(self.current_block['acfd']) and lenlist != 0:
         im_acf=self.current_block['acfd'][item*numofpoints+1:(item+1)*numofpoints+1:2]
         return im_acf
       else: 
         print "Error parsing Im acf",lenlist,numlags,lenlist*numlags*2,len(self.current_block['acfd'])
         return None

  def acf_pwr(self,key,bin):
     if key is not None:
       if key != self.current_time:
         self.set_current_time(key)

     if self.current_time is not None: 
       slistindex=self.current_block['slist'].index(bin)
       numlags=self.current_block['mplgs']
       lenlist=len(self.current_block['slist'])
       lenacf=lenlist*numlags*2
       numofpoints=numlags*2
       if lenacf == len(self.current_block['acfd']) and lenlist != 0:
         real_acf=self.current_block['acfd'][slistindex*numofpoints:(slistindex+1)*numofpoints:2]
         im_acf=self.current_block['acfd'][slistindex*numofpoints+1:(slistindex+1)*numofpoints+1:2]
         return map(lambda x,y: ((x**2+y**2)**0.5)*0.5, 
                    self.acf_real(key,slistindex),self.acf_imag(key,slistindex))
       else: 
         print "Error parsing Re acf",lenlist,numlags,lenlist*numlags*2,len(self.current_block['acfd'])
         return None

  def lagstate(self,key,bin,include_pwr=False):
     if key is not None:
       if key != self.current_time:
         self.set_current_time(key)

     if self.current_time is not None: 
       lagstate=get_lagstate(self.current_block,bin,include_pwr)
       return lagstate

  def badlags(self,key,bin):
     if key is not None:
       if key != self.current_time:
         self.set_current_time(key)
     if self.current_time is not None: 
       lagstate=get_lagstate(self.current_block,bin)
       bad_mask=MA.getmask(MA.masked_equal(MA.array(lagstate),0)) 
       badlags=MA.array(map(lambda x : abs(x[1]-x[0]),self.current_block['ltab'])[0:self.current_block['mplgs']],
           mask=bad_mask)
       return badlags

  def goodlags(self,key,bin):
     if key is not None:
       if key != self.current_time:
         self.set_current_time(key)
     if self.current_time is not None: 
       lagstate=get_lagstate(self.current_block,bin)
       good_mask=MA.getmask(MA.masked_equal(MA.array(lagstate),1)) 
       goodlags=MA.array(map(lambda x : abs(x[1]-x[0]),self.current_block['ltab'])[0:self.current_block['mplgs']],
           mask=good_mask)
       return goodlags

  def acf_lomb(self,key,item,w=None,mpinc=None,tfreq=None,gaussian=False,lagstate=None,dupzero=False,realtime=False,
          thresh=3.0,lo_f=None, hi_f=None, num_f=100,lombdata=None):
        if w is None : return None
        if key != self.current_time:
          self.set_current_time(key)
        if mpinc is None : mpinc = self.current_block['mpinc']
        if tfreq is None : tfreq = self.current_block['tfreq']
        rangebin=self.current_block['slist'][item]
        print "Entering acf_lomb:",key,item,rangebin
	iacf=N.array(self.acf_imag(key,item))
	racf=N.array(self.acf_real(key,item))
	signal=[]
	lags=[]
	badlags=[]
	if lagstate is None: lagstate=self.lagstate(key,rangebin)
        print "lagstate:",lagstate
	if badlags is None: badlags=self.badlags(key,rangebin)
        print "badlags:", badlags
        print self.current_block['mplgs']
	for index in xrange(self.current_block['mplgs']):
          lag=self.current_block['ltab'][index]
          print index,lag
	  if realtime==True: clag=abs(lag[1]-lag[0])*self.data['mpinc'][key]
	  else: clag=abs(lag[1]-lag[0])
	  lags.append(clag)
	  if (racf is None)  or (iacf is None) : 
                   print "Warning: acf is None!!!"
          else: signal.append(racf[index]+1J*iacf[index]) 
        print lags
        if lombdata is None: lombdata=lomb.acf_lomb(ltable=lags,mpinc=mpinc)
#		pwr=self.get_pwr(key,item)
          

        lombtup=lombdata.calculate(signal,lagstate,pthresh=1E-1,factor=.5,scale=10)
#	if gaussian: 
#          lombtup=lombdata.calculate(test_record['tfreq'],0.0,signal,lagstate,thresh=3.0)
#          #lombdata.calculate(tfreq=10000.,w=0,A=None,lagstate=None,normalize=True,thresh=3.0,sigmas=False)
#	else:
#          lombtup=lombdata.calculate(test_record['tfreq'],0.0,signal,lagstate,thresh=3.0)

        return lombdata,lombtup

  def signal(self,key,bin):
        if key != self.current_time:
          self.set_current_time(key)
#        bin=self.current_block['slist'][item]
        item=self.current_block['slist'].index(bin)
	racf=N.array(self.acf_real(key,item))
	iacf=N.array(self.acf_imag(key,item))
        signal=MA.zeros(self.current_block['mplgs'],dtype='complex128')
	for index in xrange(self.current_block['mplgs']):
	  if (racf is None)  or (iacf is None) : 
                   print "Warning: acf is None!!!"
          else: signal[index]=racf[index]+1J*iacf[index] 
        return signal

  def pwr_fit(self,key,bin,power=1,dupzero=False,realtime=False,force=True):
     if key is not None:
       if key != self.current_time:
         self.set_current_time(key)
     if self.current_time is not None: 
       pwr=self.acf_pwr(key,bin)
       xdata=[]
       ydata=[]
       matrix = []
       lags=[]
       lagstate=self.lagstate(key,bin)
       if True:	
#       try :
         for index in xrange(self.current_block['mplgs']):
           vector= []
           if not lagstate[index]:
             lag=self.current_block['ltab'][index]
             if realtime==True: clag=abs(lag[1]-lag[0])*self.current_block['mpinc']*1E-6 # seconds
             else: clag=abs(lag[1]-lag[0])
             xdata.append(clag) 
             ydata.append(N.log(pwr[index])) 
             vector.append(1.0)
             vector.append(-pow(clag,power))
             matrix.append(vector)
         xdata=N.array(xdata)
         ydata=N.array(ydata)
         coeffs = basic.lstsq(matrix, ydata)[0]
         if force and  (coeffs[1] < 0.0) : 
           coeffs[1]= 0.0
           coeffs[0]=N.mean(ydata)
         ycalc = coeffs[0]-coeffs[1]*pow(xdata,power) 
         error = ycalc-ydata
         n=len(error)
         x_mean2=pow(N.mean(xdata),2)
         S_xx=sum(pow(xdata,2))-n*x_mean2
#         print "x_mean2",x_mean2
#         print "S_xx",S_xx
         s=pow(sum(pow(error,2))/(n-2),0.5)
#         print "S", s
#         print "scipy.linalg.basic.lstsq curve fitting example"
         # Calculate standard error of a
         std_err_a=s*pow(1/n+x_mean2/S_xx,0.5)
         std_err_b=s/pow(S_xx,0.5)
         coeffs_err=[std_err_a,std_err_b]
#         print "fitting data to the equation y = a - b *pow(x,%d)" % (power,)
#         print "coeffs:     a ,b:",coeffs[0],coeffs[1]
#         print "coeffs err: a ,b:",std_err_a,std_err_b
#         print "yields:  x data     y data    calc value   error"
 #        for i in range(len(xdata)):
 #          print "         % .3f    % .3f      % .3f    % .3f" % (xdata[i], ydata[i], ycalc[i], error[i])
         return_tup=(coeffs,coeffs_err,xdata,ydata,ycalc,error)
#       except :
#         return_tup=None
       return return_tup

if __name__ == '__main__':
    import fitacf,datetime,os
    import pylab as p
    import numpy as N
    print "Opening RawACF Object"
    testraw=RawACF(startdate=datetime.datetime(2011,10,1,0),enddate=datetime.datetime(2011,10,1,2),radarcode='mcm')
    print "rawacf.revision.major",testraw.data[testraw.data.times[0]]["rawacf.revision.major"]
    print "rawacf.revision.minor",testraw.data[testraw.data.times[0]]["rawacf.revision.minor"]
    print "radar.revision.major",testraw.data[testraw.data.times[0]]["radar.revision.major"]
    print "radar.revision.minor",testraw.data[testraw.data.times[0]]["radar.revision.minor"]
    print "times:",testraw.data.times
    print testraw.data.datetimes
    print "Deleting RawACF Object"
#    del testraw
#    for i in range(100):
#      print "Opening RawACF Object",i
#      testraw=RawACF(startdate=datetime.datetime(2008,9,1,17),enddate=datetime.datetime(2008,9,1,18))
#      print "Deleting RawACF Object"
#      del testraw
    testfit=fitacf.FitACF(startdate=datetime.datetime(2011,10,1,0),enddate=datetime.datetime(2011,10,1,2),radarcode='mcm')
#    long_numbadlags=[] 
#    norm_numbadlags=[] 
    testraw.set_current_time(testraw.data.times[130])
    print testfit.data[testraw.current_time]["slist"]
    print testfit.data[testraw.current_time]["ltab"]
    print len(testfit.data[testraw.current_time]["ltab"])
    for nr in testfit.data[testraw.current_time]["slist"]:
      print "lagstate:",testraw.lagstate(testraw.current_time,nr)
    
    sys.exit(0)
    item=0  
    rangebin=testfit.data[testraw.current_time]["slist"][item]
    rangebin=30
    print "Rangbin:",rangebin
    lombtup=testraw.acf_lomb(testraw.current_time,item,w=0.0,num_f=500,lo_f=-500,hi_f=500,
      lagstate=None,gaussian=False,dupzero=False,realtime=False,thresh=3.0)
    hmm=testraw.pwr_fit(testraw.current_time,rangebin,power=2)
    good_mask=p.ma.getmask(p.ma.masked_equal(p.ma.array(testraw.lagstate(testraw.current_time,rangebin)),1)) 
    bad_mask=p.ma.getmask(p.ma.masked_equal(p.ma.array(testraw.lagstate(testraw.current_time,rangebin)),0)) 
    goodlags=p.ma.array(map(lambda x : abs(x[1]-x[0]),testraw.current_block['ltab'])[0:testraw.current_block['mplgs']],
           mask=good_mask)
    badlags=p.ma.array(map(lambda x : abs(x[1]-x[0]),testraw.current_block['ltab'])[0:testraw.current_block['mplgs']],
           mask=bad_mask)
    fitted_lags=N.linspace(N.min(goodlags),N.max(goodlags),100)
    print goodlags
    print fitted_lags
    print hmm
    fitted_pwr=N.exp(hmm[0][0])*N.exp(-1*hmm[0][1]*fitted_lags**2)
 
    try: p.plot(fitted_lags,fitted_pwr,color="black")
    except: pass
    try: p.scatter(goodlags,testraw.acf_pwr(testraw.current_time,rangebin))
    except: pass
#    try: p.scatter(badlags,testraw.acf_pwr(testraw.current_time,rangebin),color='red')
#    except: pass
#    if False:
##    for index,time in enumerate(testraw.data.times):
#      testraw.set_current_time(time)
#      print "time",index,time
#      for i,rangebin in enumerate(testraw.current_block['slist']):
#        bad_mask=p.ma.getmask(p.ma.masked_equal(p.ma.array(testraw.lagstate(testraw.current_time,i)),0)) 
#        good_mask=p.ma.getmask(p.ma.masked_equal(p.ma.array(testraw.lagstate(testraw.current_time,i)),1)) 
#        badlags=p.ma.array(map(lambda x : abs(x[1]-x[0]),testraw.current_block['ltab'])[0:testraw.current_block['mplgs']],
#           mask=bad_mask)
#        goodlags=p.ma.array(map(lambda x : abs(x[1]-x[0]),testraw.current_block['ltab'])[0:testraw.current_block['mplgs']],
#           mask=good_mask)
#        re=testraw.acf_real(testraw.current_time,rangebin)
#        im=testraw.acf_imag(testraw.current_time,rangebin)
#        pwr=testraw.acf_pwr(testraw.current_time,rangebin)
#        if index % 2 == 0 : long_numbadlags.append(len(badlags.compressed())/float(testraw.current_block['mplgs'])) 
#        else :norm_numbadlags.append(len(badlags.compressed())/float(testraw.current_block['mplgs']))
##    p.subplot(211)
##    p.title("Distribution of badlag number for long sequence")
##    p.hist(long_numbadlags,100,fc='b')
##    p.subplot(212)
##    p.title("Distribution of badlag number for normal sequence")
##    p.hist(norm_numbadlags,100,fc='r')
    p.show()

#    del testraw,testfit
#
#    print "Opening RawACF Object"
#    testraw=RawACF(startdate=datetime.datetime(2008,9,1,17),enddate=datetime.datetime(2008,9,1,18),verbose=True)
#    print "Testing Length of object lists"
#    print len(testraw.files), len(testraw.data.times)
#    print min(testraw.data.times),max(testraw.data.times)
#    print "Testing Data retrieval from open files"
#    print sorted(testraw.data[min(testraw.data.times)].keys())
#    print sorted(testraw.data[max(testraw.data.times)].keys())
#    elv=testraw.data['bmnum']
#    for key,item in testraw.data['bmnum'].items():
#      print key,item

