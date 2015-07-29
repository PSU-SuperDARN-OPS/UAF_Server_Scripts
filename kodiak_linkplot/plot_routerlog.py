from pylab import *
matplotlib.use("Agg")
import csv
import datetime

filename = 'routerlog_Fri_Sep_19_09:04:18_2014.csv'

csvfile = open(filename, 'r')
csvreader = csv.reader(csvfile, delimiter=';')

print csvfile.next()

rber = []
lber = []
rrsl = []
lrsl = []

wind = []
winddir = []
rain = []
times = []

for row in csvreader:
    if len(row) >= 11:
        print row
        print len(row)
        times.append(datetime.datetime.fromtimestamp(float(row[1])))
        lber.append(10*log10(float(row[3])))
        if float(row[2]) < -50:
            lrsl.append(float(row[2]))
        else:
            lrsl.append(-120)
        if float(row[4]) != 0: 
            rrsl.append(float(row[4]))
        else:
            rrsl.append(-120)

        if float(row[5]) != 0:
            rber.append(10*log10(float(row[5])))
        else:
            rber.append(-120)
        wind.append(float(row[6]))
        winddir.append(float(row[8]))
        rain.append(('rain' in row[9].lower()) * 10)

plot(times, rrsl)
plot(times, lrsl)
plot(times, wind)
plot(times, rain)
#plot(times, rber)
plot(times, lber)
plot(times, len(times)*[10*log10(10e-3)], 'r-.')
#plot(times, len(times)*[10*log10(10e-6)], 'g.')
plot(times, len(times)*[-86], 'p-.')
xlabel('kodiak localtime')
ylabel('see legend')
legend(['far end RSL (dBm)', 'near end RSL (dBm)', 'wind (mph)', 'rain (nonzero is rain)', '10log10(near end bit error rate)','BER 10e-3','-86 dBm'],loc='lower left',fancybox=True,ncol=2)
grid(True)
title('kodiak microwave link, near end is kodiak, far end is chiniak')
gcf().autofmt_xdate()
show()

