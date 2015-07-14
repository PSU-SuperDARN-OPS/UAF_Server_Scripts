from pyrpos import PosGeo, PosMag, PosCubic
import datetime
def main():
  print "Test"
  print dir(PosGeo)
  print type(datetime.datetime.now())
  for i in range(20):
    print PosGeo(radarcode='kod',bcrd=i)
#  print PosGeo(radarcode='kod')
if __name__ == '__main__':
    main()

