import pydmap
import time
variables={'scalars': ['atten', 'bmazm', 'bmnum', 'channel', 'combf', 'cp', 'ercod', 'fitacf.revision.major','fitacf.revision.minor', 'frang', 'intt.sc', 'intt.us', 'lagfr', 'lvmax', 'mpinc', 'mplgs','mppul', 'mxpwr', 'nave', 'noise.lag0', 'noise.mean', 'noise.search', 'noise.sky', 'noise.vel', 'nrang','offset', 'origin.code', 'origin.command', 'origin.time', 'radar.revision.major', 'radar.revision.minor','rsep', 'rxrise', 'scan', 'smsep', 'stat.agc', 'stat.lopwr', 'stid', 'tfreq', 'time.dy','time.hr', 'time.mo', 'time.mt', 'time.sc', 'time.us', 'time.yr', 'txpl', 'txpow', 'xcf'], 'arrays':['elv','elv_high', 'elv_low', 'gflg', 'ltab', 'nlag', 'p_l', 'p_l_e', 'p_s', 'p_s_e', 'phi0', 'phi0_e', 'ptab', 'pwr0','qflg', 'sd_l', 'sd_phi', 'sd_s', 'slist', 'v', 'v_e', 'w_l', 'w_l_e', 'w_s', 'w_s_e', 'x_gflg', 'x_p_l','x_p_l_e', 'x_p_s', 'x_p_s_e', 'x_qflg', 'x_sd_l', 'x_sd_phi', 'x_sd_s', 'x_v', 'x_v_e', 'x_w_l', 'x_w_l_e','x_w_s', 'x_w_s_e']}
test=pydmap.PyDMapObject('/home/jspaleta/Data/SuperDarn/20070426.0600.01.kod.fitacf',variables=variables,required_arrays=['slist'],badrecords=None)
print dir(test)
#for f in range(0,100): p_l=test.getvar("p_l")
#pwr0=test.getvar("pwr0")
#time.sc=test.getvar("time.sc")
#print len(p_l),len(time.sc),len(pwr0)
