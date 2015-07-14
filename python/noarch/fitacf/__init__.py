import os,datetime

class FitACF:
  def __del__(self):
#    for f in self.fileobjects:
#      f.close()
    pass
  def __init__(self,startdate=datetime.datetime(2007, 04, 26,0,0,0)
    ,enddate=None,filelist=None,directory=None,pathlist=None,verbose=False,walk=False,radarcode='kod',timeformat='f'):
    from filelocator import locate_files
    from dmap import DMapFile
    self._verbose=verbose
    self._ext=['.fitacf','.fitacf.gz']
    if radarcode is None: self.radarcode='kod'
    else: self._radarcode=radarcode
    self._variables={
      'scalars': [
        'atten', 'bmazm', 'bmnum', 'channel', 'combf', 'cp', 'ercod', 'fitacf.revision.major',
        'fitacf.revision.minor', 'frang', 'intt.sc', 'intt.us', 'lagfr', 'lvmax', 'mpinc', 'mplgs',
        'mppul', 'mxpwr', 'nave', 'noise.lag0', 'noise.mean', 'noise.search', 'noise.sky', 'noise.vel', 
        'nrang','offset', 'origin.code', 'origin.command', 'origin.time', 'radar.revision.major',
        'radar.revision.minor','rsep', 'rxrise', 'scan', 'smsep', 'stat.agc', 'stat.lopwr', 'stid', 'tfreq',
        'time.dy','time.hr', 'time.mo', 'time.mt', 'time.sc', 'time.us', 'time.yr', 'txpl', 'txpow', 'xcf']
      ,'pulse_arrays': [
        'ptab','ltab']
      ,'variable_range_arrays': [
        'elv','nlag','elv_high', 'elv_low', 'gflg', 'p_l', 'p_l_e', 'p_s', 'p_s_e', 'phi0', 
        'phi0_e', 'qflg', 'sd_l', 'sd_phi', 'sd_s', 'v', 'v_e', 'w_l', 'w_l_e', 'w_s', 
        'w_s_e', 'x_gflg', 'x_p_l','x_p_l_e', 'x_p_s', 'x_p_s_e', 'x_qflg', 'x_sd_l', 'x_sd_phi', 'x_sd_s', 'x_v',
        'x_v_e', 'x_w_l', 'x_w_l_e','x_w_s', 'x_w_s_e']
      ,'index_range_array': ['slist']
      ,'full_range_arrays': ['pwr0']
      }
    self._required=['nrang']
    self._rangevar='slist'
    if timeformat is None: self._format='d'
    else: self._format=timeformat
    self.startdate=startdate
    if enddate is None : self.enddate=startdate+datetime.timedelta(days=1)
    else : self.enddate=enddate
    try:
      if pathlist is None: self._pathlist=[]
      else: self._pathlist=pathlist
    except:
      self._pathlist=[]
      pass
    if directory is not None: self._pathlist.append(directory)
    if len(self._pathlist) == 0:
      self._pathlist.append(os.environ['SD_FITROPEN_PATH'].strip().split(":")[0])
    if filelist is None: 
      self.files=locate_files(self.startdate,self.enddate,self._pathlist,self._ext,self._radarcode,walk=walk,verbose=verbose)
    else:
      if type(filelist)==type([]): self.files=filelist
      else: self.files=[filelist]
    self.data=DMapFile(files=self.files,required=self._required
      ,starttime=self.startdate,endtime=self.enddate
      ,rangevar=self._rangevar,rangearrs=self._variables['variable_range_arrays']
      ,format=self._format)
    self.cache={}
  def purge_cache(self,varname=None):
    if varname==None:
      return self.data.purge_cache()
    else:
      return self.data.purge_cache(varname)


def main():
    print "Opening FitACF Object"
    testfit=FitACF(radarcode='kod.c',startdate=datetime.datetime(2011,7,20,0),enddate=datetime.datetime(2011,7,20,8),verbose=True)
    print "Testing Length of object lists"
    print len(testfit.files), len(testfit.data.times)
    if True:
#    try: 
      print min(testfit.data.times),max(testfit.data.times)
      print "Testing Data retrieval from open files"
      print sorted(testfit.data[min(testfit.data.times)].keys())
      print sorted(testfit.data[max(testfit.data.times)].keys())
      T0=testfit.data.times[0]
      data0=testfit.data[T0]
      print "T0:",T0
      print "Data[T0][v]:",data0["v"]
      print "Data[T0][slist]:",data0["slist"]
      vel=testfit.data['v']
      print "Vel[T0]:",vel[T0]
      #for key,item in testfit.data['v'].items():
      #  print key,item
#    except: pass
if __name__ == '__main__':
    main()

