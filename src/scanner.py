from socket import *;
import sys
from IPy import IP

def scan_port(sock, ip, port):
    try:
        sock.connect((ip, port)) 
        return True
    except:
    
        return False

def scan_ports_from_ip(ip, range_max, range_min, detail):
    resultArray = []
    for port in range(range_min, range_max):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(0.05) 
        if detail: 
            if scan_port(sock, ip, port): 
                print("[+] Port {} is open".format(port))
                resultArray.append(port)
            else:
                print("[-] Port {} is closed".format(port))
        else:
            if scan_port(sock, ip, port): resultArray.append(port)

        sock.close()
    return resultArray


def scan_ports_from_name(name, range_max, range_min, detail):
    ip = gethostbyname(name)
    return scan_ports_from_ip(ip, range_max, range_min, detail)

def isIP(name):
    try: 
        IP(name)
        return True
    except ValueError:
        return False

def default_scan(name, detail):
    resultArray = []
    defaultPortList = [20,21,22,23,25,53,137,139,445,80,443,8080,8443,1433,1434,3306,3389]
    with open('resource/defaultPort.txt') as f:
        lines = f.readlines()
    if not isIP(name):
        name = gethostbyname(name)

    for port in defaultPortList:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(0.05) 
        if detail: 
            if scan_port(sock, name, port): 
                print("[+] Port {} is open".format(port))
                resultArray.append(port)
            else:
                print("[-] Port {} is closed".format(port))
        else:
            if scan_port(sock, name, port): resultArray.append(port)
    
    print('\n[+] Scanning finished\n\n')
    for port in resultArray:
        for line in lines:
            if port == int(line.split(':')[0]):
                print("[+] Port" + line.split(':')[1].replace('\n','') + " " + str(port) + " is open")
    
    sys.exit(0)
def help():
    print("\t-u: scan ports from hostname")
    print("\t-i: scan ports from ip")
    print("\t-min: minimum port to scan")
    print("\t-max: maximum port to scan")
    print("\t-d: detail scan")
    print("\t-h: help")
    print('\t--default: scan default ports')
    sys.exit(0) 

if __name__ == '__main__':

    if '-h' in sys.argv: help()
    if '-u' in sys.argv: url = sys.argv[sys.argv.index('-u') + 1]
    elif '-i' in sys.argv: ip = sys.argv[sys.argv.index('-i') + 1]
    else : print("[-] Please specify an ip or url")

    if '-d' in sys.argv: detail = True
    else: detail = False
    

    if '--default' in sys.argv: 
        if 'url' in locals(): default_scan(url, detail)
        elif 'ip' in locals(): default_scan(ip, detail)
    else:
        if '-min' in sys.argv: min = int(sys.argv[sys.argv.index('-min') + 1]) 
        else: min = 0

        if '-max' in sys.argv: max = int(sys.argv[sys.argv.index('-max') + 1])
        else : max = 100

    

    if 'url' in locals(): result = scan_ports_from_name(url, max, min, detail)
    elif 'ip' in locals(): 
        result = scan_ports_from_ip(ip, max, min, detail)
    else: 
        print('Enter -u or -i')
        sys.exit(0) 
    
    print('Open ports: ', result)

## TODO idea : excludes ports, timeout, 