# poorly written script to log BER and RSL of ExtendAir r5005 routers over telnet

import telnetlib, time, csv, pywapi

csvfilename = 'routerlog_' + time.ctime().replace(' ','_') + '.csv'
csvfile = open(csvfilename, 'w')
csvwriter = csv.writer(csvfile, delimiter=';')
csvwriter.writerow(['localtime', 'time (UTC seconds from epoch)', 'local RSL (dBm)', 'local BER', 'remote RSL (dBm)', 'remote BER', 'wind (mph)', 'wind gust (mph)', 'wind dir (deg)', 'weather', 'temp (F)'])
router = 'localhost' # SET ROUTER IP
user = 'admin'
password = 'SETPASSWORD'
noaastation = 'PADQ'

tn = telnetlib.Telnet(router)
print tn.read_until('login: ')
time.sleep(.5)
tn.write(user + '\n')
print tn.read_until('Password: ')
time.sleep(.5)
tn.write(password + '\n')
print 'logged in to router'

print tn.read_until('Select from 1 to 7, h: ')
time.sleep(.5)
tn.write('4\n')
print tn.read_until('Select from 0 to 4, h: ')
time.sleep(.5)
tn.write('3\n')

print tn.read_until('Select from 0 to 3, h: ')
time.sleep(.5)
tn.write('1\n')


for i in range(18000):
    response = tn.read_until('Select from 0 to 3, h: ').lower()
    time.sleep(.5)

    tn.write('1\n')
    time.sleep(4.5)
 
    lber = response.split('\n')[2].split('\t')[-1][:-1]
    lrsl = response.split('\n')[3].split('\t')[-1][:-1]

    if 'performance data is not available' in response:
        rber = 1
        rrsl = 0
    else:
        rber = response.split('\n')[11].split('\t')[-1][:-1]
        rrsl = response.split('\n')[12].split('\t')[-1][:-1]

    # update weather every 5 minutes (NOAA only updates every hour..)
    if (i % 60) == 0:
        print 'updating weather'
        noaa = pywapi.get_weather_from_noaa(noaastation)
        wind = noaa['wind_mph']
#wind_gust = noaa['wind_gust_mph']
        wind_gust = 0 #wind gust field doesn't work on PADQ 
        wind_deg = noaa['wind_degrees'] 
        weather = noaa['weather']
        temp = noaa['temp_f']

    print 'rber: ' + str(rber) + ' rrsl: ' + str(rrsl) + ' lber: ' + str(lber) + ' lrsl: ' + str(lrsl)
    print 'wind: ' + wind  
    csvwriter.writerow([time.asctime(time.localtime()), str(time.time()), str(lrsl), str(lber), str(rrsl), str(rber), wind, wind_gust, wind_deg, weather, temp])


tn.close()
csvfile.close()
