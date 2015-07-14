from pyaacgm import Convert 
import datetime
def main():
  print "Test"
  print dir(Convert)
  print "Kodiak Radar Geographic Location:"
  print [57.6,-152.2]
  print "2010:",Convert(57.17,-96.28,0.0,year=2010,flag=1)
#  print "1990:",Convert(57.17,-96.28,0.0,year=1990,flag=1)
#  print "Kodiak Radar GeoMagnetic Location:"
#  print [57.17,-96.28]
#  print "2010:",Convert(57.6,-152.2,0,year=2010)
#  print "1990:",Convert(57.6,-152.2,0,year=1990)
#  for mag_lat in range(0.,80.,5.):
#    for mag_lon in range(180,-180,-1.):
#      print mag_lat,mag_lon,"  ",Convert(mag_lat,mag_lon,250.0,flag=1)

if __name__ == '__main__':
    main()

