import socket

TIMEOUT = 20

radar_streamports = {  \
            'ade':1401,\
            'adw':1501,\
            'kod':2024,\
            'koc':2023,\
            'spa':10011,\
            'mca':1024,\
#            'mcb':1025,\ # mcb is disabled (2/06/14)
            'ksr':1024}
            

def check_stream(host, port):
    retval = False

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)

    try:
    	s.connect((host, port))
        data = s.recv(1024)
        retval = True

    except:
	pass

    s.close()
    return retval

def check_radar_streams():
    failures = []
    for radar in radar_streamports:
	print 'checking ' + radar + '...'
        if check_stream(radar, radar_streamports[radar]):
            print radar + ' data stream working'
        else:
            failures.append(radar) 
            print radar + ' data stream connection timeout'
    return failures

if __name__ == '__main__':
    print check_radar_streams()

