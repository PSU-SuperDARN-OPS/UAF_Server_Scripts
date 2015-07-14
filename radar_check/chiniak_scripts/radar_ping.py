import subprocess, pdb
from remote_command import remote_command_echo

TIMEOUT = str(5) # timeout of netcat pinging

kodiak = {\
    'kodiak-nw-fitc':'kodiak-nw-fitc',\
    'kodiak-lnx':'kodiak-lnx',\
    'kodiak-dds':'kodiak-dds',\
    'kodiak-nw-site':'kodiak-nw-site'}

kingsalmon = {\
    'ks-rst':'ks-lnx',\
    'ks-ros':'ks-qnx',\
    'ks-nw-bbtc':'ks-nw-bbtc',\
    'ks-nw-site':'ks-nw-site'}

adak = {\
    'adak-lnx':'adak-lnx',\
    'adak-ups':'adak-ups',\
    'adak-qnx':'adak-qnx'}

mcmurdo = {\
    'mcm-lnx':'mcm-lnx',\
    'mcm-qnx':'mcm-qnx',\
    'mcm-ups2':'mcm-ups-cpu',\
    'mcm-ups1':'mcm-ups-tx'}

southpole = {
    'sps-lnx':'sps-lnx',\
    'sps-qnx':'sps-qnx'}

servers = {\
    'chiniak':'chiniak.gi.alaska.edu',\
    'kodiak':'kodiak.gi.alaska.edu',\
    'raid4':'192.168.1.12',\
    'raid0':'192.168.1.10'}

def netcat_checkport(ip, port=22):
    nc = subprocess.Popen(["nc", "-zv", ip, str(port), "-w", TIMEOUT], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, error = nc.communicate()
    if 'succeeded' in out:
        return True
    return False
 
def ping_ip_loss(ip):
    ping = subprocess.Popen(["ping", "-c", "4", ip], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, error = ping.communicate()
    return out.split('\n')[-3].split(' ')[5] 

# ssh into sshuser@sship, ping pingip
# useful for getting around firewalls in antarctica to check on the pdus..
def ping_pivot(sship, sshuser, pingip, port = 22):
    down = []
    command = 'ping -c 1 ' + pingip 
    pingresult = remote_command_echo(sshuser, sship, command, port = port)
    try:
    	pingresult = pingresult.split('\n')[-3].split(' ')[5] 
	if pingresult == '100%':
	    down.append(pingip)
	else:
	    print pingip + ' appears online'
    except:
        down.append(pingip)

    return down

def ping_site(site):
    down = []
    for computer in site:
        result = ping_ip_loss(site[computer])
        print computer + ' - ' + result + ' packet loss'

        if result == '100%':
            down.append(computer)
    return down 

def poke_site(site, port = 22):
    down = []
    for computer in site:
       	result = netcat_checkport(site[computer], port)

        if not result:
            print 'computer ' + computer + ' appears down'
            down.append(computer)
        else:
            print 'computer ' + computer + ' appears online'
    return down 

# hardcoded because adak is odd..
def check_ports(ip, ports):
    down = []
    for port in ports:
        if netcat_checkport(ip, port):
            print ip + ' computer ' + str(port) + ' appears online'
        else:
            print ip + ' computer ' + str(port) + ' appears down'
            down.append(port)
    return down

def poke_adak():
    down = []
    down += check_ports('adak-lnx', [6022, 7022, 8022, 9022])
    return down

def check_sites():
    down = []
    down += poke_site(mcmurdo)
    down += ping_pivot('mcm-lnx', 'radar', 'mcm-pdu1')
    down += ping_pivot('mcm-lnx', 'radar', 'mcm-pdu2')

    down += ping_pivot('ade-lnx', 'radar', 'pdu-e1', port = 7022)
    down += ping_pivot('ade-lnx', 'radar', 'pdu-e2', port = 7022)
    down += ping_pivot('ade-lnx', 'radar', 'pdu-w1', port = 7022)
    down += ping_pivot('ade-lnx', 'radar', 'pdu-w2', port = 7022)

    down += poke_site(southpole)
    down += poke_adak()
    down += ping_site(kodiak)
    down += ping_site(kingsalmon)
    down += ping_site(servers)

    return down

if __name__ == '__main__':
    down = []
    down += ping_pivot('ade-lnx', 'radar', 'pdu-w2', port = 7022)
    down += ping_pivot('ade-lnx', 'radar', 'pdu-e2', port = 7022)
    down += ping_pivot('ade-lnx', 'radar', 'pdu-w1', port = 7022)
    down += ping_pivot('ade-lnx', 'radar', 'pdu-w2', port = 7022)
    print down
