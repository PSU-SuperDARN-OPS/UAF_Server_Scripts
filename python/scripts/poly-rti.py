# This is a somewhat complicate script that I use to RTI-plots of
#
#

# Importing of several python modules for this script
from matplotlib.collections import PolyCollection
import sdcolormaps
from data_check import check_for_updates
from optparse import OptionParser
from datetime import *
import os,sys,matplotlib,fitacf
import numpy as N
import tempfile
from time import clock
from string import lower,upper
from shutil import rmtree
try:
  import numpy.ma as MA
except:
  import numpy.core.ma as MA
import pylab as p
from matplotlib.dates import HourLocator,MinuteLocator
from matplotlib.ticker import MaxNLocator
import greatcircle
import math
import aacgm
import rpos
home=os.environ['HOME']
#from mpl_toolkits.basemap.pyproj import Geod
today=datetime.utcnow()-timedelta(days=1)
parser = OptionParser()
parser.add_option( "-f", "--force", dest="force",action="store_true",default=False,
                  help="Force creation of plot even if plot already exists",)
parser.add_option("-r", "--radar", dest="radar",default="kod",
                  help="3 letter radarcode",)
parser.add_option("-c", "--channel", dest="channel",default="",
                  help="Radar Channel",)
parser.add_option("-b", "--beam", action="append",type="int",dest="beamlist",default=[],
                  help="Add additional beam for plotting")
parser.add_option("--maxskip", dest="max_skip_secs",type="float",default=60*2,
                  help="maximum pixel time extent",)
parser.add_option("--minskip", dest="min_skip_secs",type="float",default=0.5,
                  help="minimum pixel time extent",)
parser.add_option("-Y", "--year", dest="year",type="int",default=today.year,
                  help="Year",)
parser.add_option("-M", "--month", dest="month",type="int",default=today.month,
                  help="Month",)
parser.add_option("-D", "--day", dest="day",type="int",default=today.day,
                  help="Day",)
parser.add_option("--hour", dest="hour",type="int",default=0,
                  help="Hour",)
parser.add_option("--minute", dest="minute",type="int",default=0,
                  help="Minute",)
parser.add_option("--plotminutes", dest="plotminutes",type="int",default=60*24,
                  help="Time extent of plot in minutes",)
parser.add_option( "--days", dest="days",type="int",default=1,
                  help="Days prior to process",)
parser.add_option( "--plotvar1", dest="plotvar1",default="p_l",
                  help="Variable to Plot",)
parser.add_option( "--plotvar1_label", dest="plotvar1_label",default="[dB]",
                  help="Unit Label for plot variable",)
parser.add_option( "--plotvar2", dest="plotvar2",default="v",
                  help="Variable to Plot",)
parser.add_option( "--plotvar2_label", dest="plotvar2_label",default="[m/s]",
                  help="Unit Label for plot variable",)
parser.add_option( "--plotvar1_min", dest="plotvar1_min",type="int",default=0,
                  help="Minimum value for plot variable",)
parser.add_option( "--plotvar1_max", dest="plotvar1_max",type="int",default=40,
                  help="Maximum value for plot variable",)
parser.add_option( "--plotvar2_min", dest="plotvar2_min",type="int",default=-500,
                  help="Minimum value for plot variable",)
parser.add_option( "--plotvar2_max", dest="plotvar2_max",type="int",default=500,
                  help="Maximum value for plot variable",)
parser.add_option( "--directory", dest="directory",default="%s/tmp/data_to_plot/" %(home),
                  help="Working directory for data files to process",)
parser.add_option( "--plottree", dest="plottree",default="/raid/SuperDARN/daily_plots/",
                  help="Directory tree for rendered plots",)
parser.add_option( "--nowalk", dest="walk",action="store_false",default=True,
                  help="Don't Walk the directory of interest",)
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")
parser.add_option( "--geodist",
                  action="store_true", dest="geodist", default=False,
                  help="Use Geodesic Latitude for Range")
parser.add_option( "--magdist",
                  action="store_true", dest="magdist", default=False,
                  help="Use Geomag Latitude for Range")
parser.add_option( "--rangedist",
                  action="store_true", dest="rangedist", default=False,
                  help="Use Ground Range")

(options, args) = parser.parse_args()
if len(options.beamlist) == 0 : options.beamlist.append(9)
print options.year,options.month,options.day
# Some global script control variables
plot=True  #display the plots as well as save them
show=False
savefile=True
range_distance=options.rangedist
lat_distance=options.geodist
geomag_distance=options.magdist
show_gflag=True # Shade ground flag
target_range=False   # plot haarp_range location

plotdict={}
plotdict["radar"]=upper(options.radar)  #the radar code
plotdict["channel"]=upper(options.channel)
plotdict["plotvar1"]=options.plotvar1  #variable to plot
plotdict["plotvar2"]=options.plotvar2  #variable to plot
plotdict["directory"]=os.path.join(options.directory,plotdict["radar"],plotdict["channel"])  
plotdict["plot_dir"]=os.path.join(options.plottree,plotdict["radar"],plotdict["channel"])
plotdict["plotvar1_label"]=options.plotvar1_label #label for colorbar
plotdict["plotvar2_label"]=options.plotvar2_label #label for colorbar
plotdict["plot_title_text"]="SuperDARN RTI Plot"
plotdict["days_per_plot"]=p.floor(options.plotminutes/(60.0*24.0))
plotdict["seconds_per_plot"]=60*(options.plotminutes-(plotdict["days_per_plot"]*60*24))
plotdict["max_days_to_plot"]=options.days
plotdict["min_skip_secs"]=options.min_skip_secs
plotdict["max_skip_secs"]=options.max_skip_secs
plotdict["num_tick_divisions"]=6
plotdict["year"]=options.year
plotdict["month"]=options.month
plotdict["day"]=options.day
plotdict["hour"]=options.hour
plotdict["plot1_min"]=options.plotvar1_min   #minimum for colorbar
plotdict["plot1_max"]=options.plotvar1_max #maximum for colorbar
plotdict["plot2_min"]=options.plotvar2_min   #minimum for colorbar
plotdict["plot2_max"]=options.plotvar2_max #maximum for colorbar
plotdict["max_slant_rang"]=1500 #maximum range
plotdict["min_slant_rang"]=0 #minimum range
plotdict["max_rang"]=None #maximum range
plotdict["min_rang"]=None #minimum range
plotdict["beamlist"]=options.beamlist  #which beams to plot  16 means all beams
print plotdict
enddate=datetime(plotdict["year"],plotdict["month"],plotdict["day"],plotdict["hour"],0)   #end date and time
startdate= enddate-timedelta(days=plotdict["max_days_to_plot"])    # start date and time
enddate= enddate+timedelta(days=1)    # end date and time
skiptime=timedelta(days=plotdict["days_per_plot"],seconds=plotdict["seconds_per_plot"])
total_seconds=60*60*24*plotdict["days_per_plot"]+plotdict["seconds_per_plot"]
startday= enddate-timedelta(days=1)    # end date and time
endday=  startday+skiptime    # end date and time
print plotdict["days_per_plot"],plotdict["seconds_per_plot"]
print startdate,startday,endday,enddate


#beamlist=[9]  # Each beam gets its own plot
max_plot_numsecs=min(60*60,plotdict["max_skip_secs"])
min_plot_numsecs=max(0.5,plotdict["min_skip_secs"])
use_int_time=False
tick_min_interval=int(total_seconds/(60*plotdict["num_tick_divisions"]))           # tick marker seperation in minutes  None is auto
#set the colormaps for the plotting
beam_cmap=p.cm.cool  
tfreq_cmap=p.cm.spectral
noise_cmap=p.cm.autumn
plot1_cmap=p.cm.jet
plot2_cmap=p.cm.get_cmap("SD_V")

#Set gflg color
gflag_color="grey"
#locations for kodiak and haarp
kod_lat=57.60 #degrees
kod_lon=360-152.2 #degrees
haarp={"lat":62.3,"lon":360-145.3}
fairbanks={"lat":64.8378,"lon":360-147.7164}
kodiak={"lat":57.60,"lon":360-152.2}
adak={"lat":51.89,"lon":360-176.63}
target=fairbanks
rad=adak

major_radius=6370997.0
minor_radius=6356752.3142
f = (major_radius-minor_radius)/major_radius

# setup the geodesic model of the earth from the basemap module
#g=Geod(ellps='clrk80')



# calculate useful tick intervals
numseconds=(endday-startday).seconds
#onesec=p.date2num(datetime(1,1,1,0,0,1))-p.date2num(datetime(1,1,1,0,0,0))
onesec=1.0/(24.*60.*60.)
print onesec 
if plotdict["days_per_plot"] > 1 :
  tick2_minute_interval=HourLocator(byhour=[0,12])
  tick1_minute_interval=HourLocator(byhour=[0,12])
else:
  if tick_min_interval is None:
    minutes=numseconds/60
    if minutes % 5 == 0 : interval=minutes / 5
    elif minutes % 3 == 0 : interval=minutes / 3
    else: interval=minutes / 4
    tick2_minute_interval=MinuteLocator(interval=interval)
    tick1_minute_interval=MinuteLocator(interval=interval)
  else : 
    tick1_minute_interval=MinuteLocator(interval=tick_min_interval)
    tick2_minute_interval=MinuteLocator(interval=tick_min_interval)

# setup the normalization scales for beam,tfreq and plot variable
#if plot_min is None or plot_max is None: norm = matplotlib.colors.normalize()
#else: 
norm1 = matplotlib.colors.normalize(vmin=plotdict["plot1_min"], vmax=plotdict["plot1_max"])
norm2 = matplotlib.colors.normalize(vmin=plotdict["plot2_min"], vmax=plotdict["plot2_max"])
tnorm = matplotlib.colors.normalize(9, 19)
bnorm = matplotlib.colors.normalize(0, 4)
nnorm = matplotlib.colors.normalize(0, 10000)

#calculate haarp distance 
if target_range:
  if target is not None:
    target_lon=target["lon"]
    target_lat=target["lat"]
    radar_lon=rad["lon"]
    radar_lat=rad["lat"]
  target_dist,a,b=greatcircle.vinc_dist(f,major_radius,math.radians(radar_lat),math.radians(radar_lon),math.radians(target_lat),math.radians(target_lon))
  target_dist=target_dist/1E3
  print "Target %s: Distance (km):",target,target_dist

tempdir=None
if plotdict["directory"] is not None:
  try: os.makedirs(plotdict["directory"])
  except: pass

#  print plotdict["directory"]
  tempdir=tempfile.mkdtemp(dir=plotdict["directory"])
#  print tempdir
  datastub="/raid/SuperDARN/data/fit/"
#  datastub="/home/jspaleta/data/fitacf/"
#  datastub="/media/SD_ANALYSIS/SuperDARN/data/fit/"
#  print datastub,tempdir
  tday=startdate
  print plotdict["plot_dir"]
  print "tday:",tday," enddate:",enddate
  eday=max(endday,enddate)
  while tday <= eday:
    date_list=check_for_updates(plotdict["radar"],plotdict["channel"],
          date=tday,
          year=None,
          data_directory=tempdir,
          plot_directory=plotdict["plot_dir"],
          prev_days=90,
          force=options.force)  
    if len(date_list) == 0 :
      date_list=check_for_updates(plotdict["radar"],plotdict["channel"],
          date=tday,
          year=None,
          data_directory=datastub,
          plot_directory=plotdict["plot_dir"],
          prev_days=90,
          force=options.force)  
#    print "Date_list:",date_list
    for date in date_list:
      pull_directory=datastub+"%04d/%02d.%02d/" % (date.year,date.month,date.day)
      if tempdir is not None:
        cwd=os.getcwd() 
        cmdstring="cp %s/*%s*.fitacf* %s" % (pull_directory,lower(plotdict["radar"]),tempdir) 
        print cmdstring
        os.system(cmdstring) 
        os.chdir(tempdir) 
        cmdstring="gzip -f -d *.gz"  
        print cmdstring
        os.system(cmdstring) 
        cmdstring="bzip2 -f -d *.bz2"  
        print cmdstring
        os.system(cmdstring) 
        print os.listdir(tempdir) 
        os.chdir(cwd) 
        print os.getcwd() 
      del pull_directory
    tday=tday+timedelta(days=1)
    print "tday:",tday," eday:",eday
  del datastub
print "Processing Data Now\n"
print startdate,startday,enddate,endday

while startdate < startday :
  outdir='%s/%04d/%02d.%02d/' % (plotdict["plot_dir"],startday.year,startday.month,startday.day)
  print outdir
#  if startday.date() not in date_list: 
#    startday=startday+skiptime
#    continue
  print startday.year,startday.month,startday.day,startday.hour,startday.minute
  print endday.year,endday.month,endday.day,endday.hour,endday.minute
  figstub="%04d%02d%02d%02d%02d_%04d%02d%02d%02d%02d" % \
    (startday.year,startday.month,startday.day,startday.hour,startday.minute, \
    endday.year,endday.month,endday.day,endday.hour,endday.minute)
  if plot:  
    p.figure(200,figsize=(7.5,6),dpi=120)
    p.clf()
    plot1_cmap.set_bad(alpha=0)
    tfreq_cmap.set_bad(alpha=0)
    beam_cmap.set_bad(alpha=0)

  if True:
    flag=True
    goodtimes=[]
    totalpwr=[]
    print "startday: ",startday 
    print "endday: ",endday                
    if True:
        start=clock()
        print "Opening fitacf files %s" %(tempdir)                
        test=fitacf.FitACF(startdate=startday,enddate=endday,walk=options.walk,directory=tempdir,radarcode=plotdict["radar"]+"."+plotdict["channel"],verbose=True)
#        test=fitacf.FitACF(startdate=startday,enddate=endday,walk=options.walk,directory=tempdir,radarcode=plotdict["radar"],verbose=True)
        print "fitacf file open"                
        test.purge_cache()
        #test.cache_limit=0
        #active_vars=('bmnum','tfreq','rsep','frang','nrang','scan.sc','scan.us',plotvar)
        #print active_vars
        #if test.data.cache_limit!=0 :       
        #  print "Filling Data"
        #  for s in active_vars:
        #    test.data[s]
        items=test.data["bmnum"].items()
        beamkeys=[]
        for k,v in items:
          if v in plotdict["beamlist"]: beamkeys.append(k)
        beamkeys.sort() 
#        keys=test.data.times
#        keys.sort()
        if len(beamkeys) == 0 : 
          startday=startday-skiptime
          endday=endday-skiptime
          continue
        print "Finding Scan times"
        end=clock()
        print "Parsing Beam List"
        for beamdir in plotdict["beamlist"]: 
          oldtime=None
          print "Starting to process Beam",beamdir 
          tpixels=[]
          tvalues=[]
          bpixels=[]
          bvalues=[]
          p1pixels=[]
          p1values=[]
          p2pixels=[]
          p2values=[]
          npixels=[]
          nvalues=[]
          if plot:
            p.figure(200)
            p.clf()
            axis_width=0.7
            c1ax = p.axes([0.85, 0.14, 0.02, 0.22],axisbg='white')
            c2ax = p.axes([0.85, 0.44, 0.02, 0.22],axisbg='white')
            tcax = p.axes([0.09, 0.70, 0.05, 0.02],axisbg='white')
#            bcax = p.axes([0.16+axis_width, 0.72, 0.05, 0.02],axisbg='white')
            ncax = p.axes([0.16+axis_width, 0.72, 0.05, 0.02],axisbg='white')
            p1color_ax = p.axes([0.15, 0.1, axis_width, 0.30],axisbg='white')
            p2color_ax = p.axes([0.15, 0.40, axis_width, 0.30],axisbg='white')
            tax = p.axes([0.15, 0.70, axis_width, 0.02],axisbg='white')
#            bax = p.axes([0.15, 0.72, axis_width, 0.02],axisbg='white')
            nax = p.axes([0.15, 0.72, axis_width, 0.02],axisbg='white')

          if oldtime is None: 
            try: oldtime=beamkeys[0]-60
            except: oldtime=0 
          start=clock()
          for i,key in enumerate(beamkeys):
            if plotdict["min_skip_secs"] is not None and not use_int_time: 
              compare_time=oldtime+(plotdict["min_skip_secs"]*onesec)
              if(compare_time > key):
                #if (record['bmnum'] == beamdir) or (beamdir == 16 ):
                  #print "Beam %d Skipping key:" % (record['bmnum']),key,compare_time,p.num2date(key),p.num2date(compare_time)
                  #pass
                continue
            totalpwr=0
            record=test.data[key] 
            if (record['bmnum'] == beamdir) or (beamdir == 16 ):
#                print "Plotting key:",key,p.num2date(key) 
                if plot:
                    x_numsecs=0
                    if (beamdir == 16) or use_int_time:
                       x_numsecs=record['intt.us']*1E-6+record['intt.sc']
                    else:
                       index=p.searchsorted(beamkeys,key)
                       test1_numsecs=N.inf
                       try: 
                           test2_numsecs=(beamkeys[index+1]-beamkeys[index])/onesec
                       except: test2_numsecs=N.inf
                       beam_interval=min(test1_numsecs,test2_numsecs)
                       x_numsecs=beam_interval
                    
                    if not use_int_time:    
                      if min_plot_numsecs is not None: 
                        if x_numsecs < min_plot_numsecs: x_numsecs=min_plot_numsecs
                      else: 
                        test_num_secs=record['intt.us']*1E-6+record['intt.sc']
                        if test_num_secs > x_numsecs: x_numsecs=test_num_secs
                      if max_plot_numsecs is not None: 
                        if x_numsecs > max_plot_numsecs: x_numsecs=max_plot_numsecs
                      x_numsecs=p.ceil(x_numsecs)+1 
                    #print "x_numsecs:",beam_interval,scan_interval,x_numsecs
                    x=[key,key+(x_numsecs*onesec),key+(x_numsecs*onesec),key]
                    oldtime=key
#                    print p.num2date(x)
                    y=[0,0,1,1]
                    tpixels.append(zip(x,y))
                    color = tfreq_cmap(tnorm(record['tfreq']/1000.0))
                    tvalues.append(color) 
#                    tax.fill(x,y,facecolor=color,ec=color,linewidth=0,zorder=1)
#                    bpixels.append(zip(x,y))
#                    bvalues.append(record['bmnum']) 
#                    color = beam_cmap(bnorm(record['bmnum']))
#                    bax.fill(x,y,facecolor=color,ec=color,linewidth=0,zorder=1)
                    npixels.append(zip(x,y))
                    color = noise_cmap(nnorm(record['noise.search']))
                    nvalues.append(color) 
#                    nax.fill(x,y,facecolor=color,ec=color,linewidth=0,zorder=1)

                try: pwr=record[plotdict["plotvar1"]]
                except: pwr=None 
                if pwr is not None:
                  gflag=record["gflg"]
                  total=0
                  if type(pwr)==type({}): pwr_list=pwr.keys()
                  elif type(pwr)==type([]): pwr_list=range(len(pwr))
                  else : 
                    pwr_list=record['slist']
                    tmpdict={}
                    if pwr_list is not None:
                      for r in pwr_list:
                        tmpdict[r]=pwr
                    pwr=tmpdict
                  if pwr_list is not None:
                    for r in pwr_list:
                      rsep=record["rsep"]
                      distance=record["frang"]+record["rsep"]*r
                      if range_distance:
                        y=[distance,distance,distance+rsep,distance+rsep]
                      else :
                        if lat_distance:
                          lat_0,lon_0,rev_angle=greatcircle.vinc_pt(
                          f,major_radius,math.radians(radar_lat),
                          math.radians(radar_lon),
                          math.radians(record["bmazm"]),distance*1E3)
                          geoloc_0=aacgm.Convert(math.degrees(lat_0),math.degrees(lon_0),0,year=2010,flag=0)
                          
                          lat_1,lon_1,rev_angle=greatcircle.vinc_pt(
                          f,major_radius,math.radians(radar_lat),
                          math.radians(radar_lon),
                          math.radians(record["bmazm"]),(distance+record["rsep"])*1E3)
                          geoloc_1=aacgm.Convert(math.degrees(lat_1),math.degrees(lon_1),0,year=2010,flag=0)
                          if geomag_distance:
                            y=[geoloc_0[0],geoloc_0[0],geoloc_1[0],geoloc_1[0]]
                          else:
                            y=[math.degrees(lat_0),math.degrees(lat_0),
                             math.degrees(lat_1),math.degrees(lat_1)]

                        else: 
                          y=[r,r,r+1,r+1]
                      if plot:
                        if show_gflag and plotdict["plotvar1"]=="v" and gflag[r]==1:  color = gflag_color
                        else: color = plot1_cmap(norm1(pwr[r]))
                        p1pixels.append(zip(x,y))
                        p1values.append(color) 
#                        p1color_ax.fill(x,y,facecolor=color,ec=color,linewidth=0,zorder=1)
                try: pwr=record[plotdict["plotvar2"]]
                except: pwr=None 
                if pwr is not None:
                  gflag=record["gflg"]
                  total=0
                  if type(pwr)==type({}): pwr_list=pwr.keys()
                  elif type(pwr)==type([]): pwr_list=range(len(pwr))
                  else : 
                    pwr_list=record['slist']
                    tmpdict={}
                    if pwr_list is not None:
                      for r in pwr_list:
                        tmpdict[r]=pwr
                    pwr=tmpdict
                  if pwr_list is not None:
                    for r in pwr_list:
                      rsep=record["rsep"]
                      distance=record["frang"]+record["rsep"]*r
                      if range_distance:
                        y=[distance,distance,distance+rsep,distance+rsep]
                      else :
                        if lat_distance:
                          lat_0,lon_0,rev_angle=greatcircle.vinc_pt(
                          f,major_radius,math.radians(radar_lat),
                          math.radians(radar_lon),
                          math.radians(record["bmazm"]),distance*1E3)
                          geoloc_0=aacgm.Convert(math.degrees(lat_0),math.degrees(lon_0),0,year=2010,flag=0)
                          lat_1,lon_1,rev_angle=greatcircle.vinc_pt(
                          f,major_radius,math.radians(radar_lat),
                          math.radians(radar_lon),
                          math.radians(record["bmazm"]),(distance+record["rsep"])*1E3)
                          geoloc_1=aacgm.Convert(math.degrees(lat_1),math.degrees(lon_1),0,year=2010,flag=0)
                          if geomag_distance:
                            y=[geoloc_0[0],geoloc_0[0],geoloc_1[0],geoloc_1[0]]
                          else:
                            y=[math.degrees(lat_0),math.degrees(lat_0),
                             math.degrees(lat_1),math.degrees(lat_1)]

                        else: 
                          y=[r,r,r+1,r+1]
                      if plot:
                        if show_gflag and plotdict["plotvar2"]=="v" and gflag[r]==1:  color = gflag_color
                        else: color = plot2_cmap(norm2(pwr[r]))
                        p2pixels.append(zip(x,y))
                        p2values.append(color) 
#                        p2color_ax.fill(x,y,facecolor=color,ec=color,linewidth=0,zorder=1)

            del record
          end=clock()
          start=clock()
          if plot:
            print "Formatting Plots"
            dateFmt = p.DateFormatter('%H:%M')  
#            if plotdict["max_rang"] is None: plotmax_rang=max(py)
#            if plotdict["min_rang"] is None: min_rang=min(py)

            print "Beamdir",beamdir
            p.figure(200)
            if target_range:
              if range_distance:
                p1color_ax.plot([p.date2num(startday),p.date2num(endday)],
                [target_dist,target_dist],linewidth=4,linestyle="--",color="k",alpha=0.5)
              else:
                if lat_distance:
                  if geomag_distance:
                    target_mag=aacgm.Convert(target_lat,target_lon,0,year=2010,flag=0)
                    p1color_ax.plot([p.date2num(startday),p.date2num(endday)],
                      [target_mag[0],target_mag[0]],linewidth=4,linestyle="--",color="k",alpha=0.5)
                  else:
                    p1color_ax.plot([p.date2num(startday),p.date2num(endday)],
                      [target_lat,target_lat],linewidth=4,linestyle="--",color="k",alpha=0.5)

            p.axes(p2color_ax)
            pixs=N.array(p2pixels)
            colors=p2values
            coll = PolyCollection(pixs,edgecolors='none',linewidths=0.0,zorder=10)
            coll.set_antialiased(False)
            coll.set_facecolor(colors)
            coll.set_alpha(1)
            p2color_ax.add_collection(coll)
            p2color_ax.autoscale_view() 
            p2color_ax.xaxis.set_major_formatter(dateFmt)
            p2color_ax.set_xlim(p.date2num(startday), p.date2num(endday))
            p2color_ax.set_ylim(plotdict["min_rang"],plotdict["max_rang"])
            p2color_ax.xaxis.set_major_locator(tick2_minute_interval)
            p2color_locator=MaxNLocator(nbins=6,prune='both',integer=True)
            p2color_ax.yaxis.set_major_locator(p2color_locator)
            p2color_ax.set_xticklabels([])
#            p2color_ax.set_xticks([])
            p2color_ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',alpha=0.5)
            p2color_ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey',alpha=0.5)
            print "pcolor done"

            p.axes(tax)
            pixs=N.array(tpixels)
            colors=tvalues
            coll = PolyCollection(pixs,edgecolors='none',linewidths=0.,zorder=10)
            coll.set_antialiased(False)
            coll.set_facecolor(colors)
            coll.set_alpha(1)
            tax.add_collection(coll)
            tax.autoscale_view()
#            tax.text(0.5, 0.48,'Freq [MHz]',
#              horizontalalignment='center', verticalalignment='center', transform = tax.transAxes,
#              color='darkgrey',fontsize=6)
            tax.xaxis.set_major_formatter(dateFmt)
            tax.xaxis.set_major_locator(tick1_minute_interval)
            tax.set_xlim(p.date2num(startday), p.date2num(endday))
            tax.set_xticklabels([])
            tax.set_yticklabels([])
            tax.set_yticks([])
            #tax.tick_params(axis='x', length=1)
            print "tax done"
#            p.axes(bax)
##            bax.text(0.5, 0.48,'Beam',
##              horizontalalignment='center', verticalalignment='center', transform = bax.transAxes,
##              color='darkgrey',fontsize=6)
#            bax.xaxis.set_major_formatter(dateFmt)
#            bax.xaxis.set_major_locator(tick1_minute_interval)
#            bax.set_xlim(p.date2num(startday), p.date2num(endday))
#            bax.set_xticklabels([])
#            bax.set_yticklabels([])
#            bax.set_yticks([])
#            #bax.tick_params(axis='x', length=1)
            p.axes(nax)
            pixs=N.array(npixels)
            colors=nvalues
            coll = PolyCollection(pixs,edgecolors='none',linewidths=0.,zorder=10)
            coll.set_antialiased(False)
            coll.set_facecolor(colors)
            coll.set_alpha(1)
            nax.add_collection(coll)
            nax.autoscale_view()
#            nax.text(0.5, 0.48,'Noise',
#              horizontalalignment='center', verticalalignment='center', transform = nax.transAxes,
#              color='darkgrey',fontsize=6)
            nax.xaxis.set_major_formatter(dateFmt)
            nax.xaxis.set_major_locator(tick1_minute_interval)
            nax.set_xlim(p.date2num(startday), p.date2num(endday))
            nax.set_xticklabels([])
            nax.set_yticklabels([])
            nax.set_yticks([])
            #nax.tick_params(axis='x', length=1)
            print "nax done"
            p.axes(p1color_ax)
            pixs=N.array(p1pixels)
            colors=p1values
            coll = PolyCollection(pixs,edgecolors='none',linewidths=0.,zorder=10)
            coll.set_antialiased(False)
            coll.set_facecolor(colors)
            coll.set_alpha(1)
            p1color_ax.add_collection(coll)
            p1color_ax.autoscale_view() 
            p1color_ax.xaxis.set_major_formatter(dateFmt)
            p1color_ax.set_xlim(p.date2num(startday), p.date2num(endday))
            p1color_ax.set_ylim(plotdict["min_rang"],plotdict["max_rang"])
            p1color_ax.xaxis.set_major_locator(tick1_minute_interval)
            p1color_locator=MaxNLocator(nbins=6,prune='both',integer=True)
            p1color_ax.yaxis.set_major_locator(p1color_locator)
            p1color_ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
            p1color_ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
            p.xlabel("Time [UTC]")
            if range_distance:
              p.figtext(0.05,0.3,"Slant Range [km]",rotation="vertical")
            else:
              if lat_distance:
                if geomag_distance:
                  p.figtext(0.05,0.6,"GeoMagnetic Latitude [Degrees]",rotation="vertical")
                else:
                  p.figtext(0.05,0.6,"Geographic Latitude [Degrees]",rotation="vertical")
              else:
                p.figtext(0.05,0.3,"Virtual Range Bin",va="center",rotation="vertical")
            p.axes(nax)
#            p.axes(bax)
            if beamdir==16: text='All Beams'
            else : text="%d" % beamdir 
            p.title("%(radar)s channel %(channel)s :: RTI Plot of %(plotvar1)s\n" % (plotdict) + "on %d/%d/%d\nAlong Beam Direction: %s\n" %
             (startday.month,startday.day,startday.year,text,))

            if True:
              clocator=MaxNLocator(nbins=4)
              c1b = matplotlib.colorbar.ColorbarBase(
                   c1ax, cmap=plot1_cmap,norm=norm1,orientation='vertical',ticks=clocator)
              c2b = matplotlib.colorbar.ColorbarBase(
                   c2ax, cmap=plot2_cmap,norm=norm2,orientation='vertical',ticks=clocator)
              c1b.set_label(plotdict["plotvar1"]+" "+plotdict["plotvar1_label"])
              c2b.set_label(plotdict["plotvar2"]+" "+plotdict["plotvar2_label"])
              tcax.xaxis.set_ticks_position('bottom')
              tb = matplotlib.colorbar.ColorbarBase(
                   tcax, cmap=tfreq_cmap,norm=tnorm,
                   orientation='horizontal',ticks=[9,14,19])
              tcax.xaxis.set_label_text("Freq [MHz]",fontsize=6,va='center',ha='right')
              tcax.xaxis.set_label_coords(-0.2,0.5)
              labels=tcax.xaxis.get_majorticklabels()
              for label in labels: label.set_fontsize(6)  
              #tcax.tick_params(axis='x', labelsize=6)
#              bcax.xaxis.set_ticks_position('top')
#              bb = matplotlib.colorbar.ColorbarBase(
#                   bcax, cmap=beam_cmap,norm=bnorm,
#                   orientation='horizontal',ticks=[0,1,2,3,4])
#              bcax.xaxis.set_label_text("Beam",fontsize=6,va='center',ha='left')
#              bcax.xaxis.set_label_coords(1.2,0.5)
#              #bcax.tick_params(axis='x', labelsize=6)
#              labels=bcax.xaxis.get_majorticklabels()
#              for label in labels: label.set_fontsize(6)  
#              bcax.xaxis.get_offset_text().set_visible(False) 

              ncax.xaxis.set_ticks_position('top')
              nformat=p.ScalarFormatter(useOffset=False)
              nformat.set_powerlimits((0,0))
              nb = matplotlib.colorbar.ColorbarBase(
                   ncax, cmap=noise_cmap,norm=nnorm,format=nformat,
                   orientation='horizontal',ticks=[0,5000,10000])
              ncax.xaxis.set_label_text("Noise [x1E4]",fontsize=6,va='center',ha='left')
              ncax.xaxis.set_label_coords(1.2,0.5)
              #ncax.tick_params(axis='x', labelsize=6,labeltop=True,labelbottom=False)
              labels=ncax.xaxis.get_majorticklabels()
              for label in labels: label.set_fontsize(6)  
              ncax.xaxis.get_offset_text().set_visible(False) 
              #print dir(ncax.xaxis)
            if savefile:
              print "Saving Plots now"
              start=clock()
              try: os.makedirs(outdir)
              except: pass
              p.savefig('/%s/' %(outdir)
                        +'RTI-%(radar)s.%(channel)s-%(plotvar1)s' % plotdict
                        +'-beam_%02d-%s.pdf' % (beamdir,figstub),dpi=300)
              p.close(200)
              end=clock()
              print "Time required:",end-start
          if show: p.show() 
          print "startday: ",startday 
          print "endday: ",endday                

#  print "delete variables"
#  print "startday: ",startday 
#  print "endday: ",endday                
#  del test,beamkeys,
#  try: del pwr,tmpdict,pwr_list
#  except: pass
  startday=startday-skiptime
  endday=endday-skiptime
#  print "startday: ",startday 
#  print "endday: ",endday                
#  print "enddate: ",enddate                

if tempdir is not None: rmtree(plotdict["directory"])
#sys.exit(0)

