from socket import *;
import sys
 
def scan_port(sock, ip, port):
    try:
        sock.connect((ip, port)) 
        return True
    except:
    
        return False

def scan_ports_from_ip_detail(ip, range_max, range_min):
    resultArray = []
    for i in range(range_min, range_max):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(0.05) 
        if scan_port(sock, ip, i): 
            print("[+] Port {} is open".format(i))
            resultArray.append(i)

        else:
            print("[-] Port {} is closed".format(i))

        sock.close()
    return resultArray

def scan_ports_from_ip(ip, range_max, range_min):
    resultArray = []
    for i in range(range_min, range_max):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(0.05)  
        if scan_port(sock, ip, i): resultArray.append(i)
        sock.close()
    return resultArray

def scan_ports_from_name(name, range_max, range_min, detail):
    ip = gethostbyname(name)
    if detail : return scan_ports_from_ip_detail(ip, range_max, range_min)
    else : return scan_ports_from_ip(ip, range_max, range_min)

def help():
    print("Usage: python3 scanner.py <ip/url> <port_range_max> <port_range_min>")
    print("\t-u: scan ports from hostname")
    print("\t-i: scan ports from ip")
    print("\t-min: minimum port to scan")
    print("\t-max: maximum port to scan")
    sys.exit(0) 

if __name__ == '__main__':

    if '-h' in sys.argv: help()
    if '-u' in sys.argv: url = sys.argv[sys.argv.index('-u') + 1]
    elif '-i' in sys.argv: ip = sys.argv[sys.argv.index('-i') + 1]

    if '-min' in sys.argv: min = int(sys.argv[sys.argv.index('-min') + 1]) 
    else: min = 0

    if '-max' in sys.argv: max = int(sys.argv[sys.argv.index('-max') + 1])
    else : max = 100
    if '-d' in sys.argv: detail = True; 
    else: detail = False;
    

    if 'url' in locals(): result = scan_ports_from_name(url, max, min, detail)
    elif 'ip' in locals(): 
        if detail :
            result = scan_ports_from_ip_detail(ip, max, min)
        else : 
            result = scan_ports_from_ip(ip, max, min)
    else: 
        print('Enter -u or -i')
        sys.exit(0) 
    
    print('Open ports: ', result)

## TODO idea : excludes ports, timeout, 