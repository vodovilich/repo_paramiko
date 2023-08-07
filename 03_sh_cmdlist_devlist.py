import paramiko
import time
import socket
from pprint import pprint

#
#PYNENG
#

def sh_cmd_list_dev_list(
    ip,
    username,
    password,
    command,
    max_bytes=90000,
    short_pause=1,
    long_pause=5,  
):
    cl = paramiko.SSHClient()
    cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cl.connect(
        hostname=ip,
        username=username,
        password=password,
        look_for_keys=False,
        allow_agent=False,
    )
    
    with cl.invoke_shell() as ssh:
        ssh.send("terminal length 0\n")
        time.sleep(short_pause)
        ssh.recv(max_bytes)
        
        result = {}
        for command in commands:
            ssh.send(f"{command}\n")
            ssh.settimeout(5)
                           
            output = ""
            while True:
                try:
                    part = ssh.recv(max_bytes).decode("utf-8")
                    output += part
                    time.sleep(0.5)
                except socket.timeout:
                    break
            result[command] = output
        return result
    
if __name__== "__main__":
    devices = ["192.168.100.5", "192.168.100.6"]
    commands = ["sh arp", "sh int desc"]
    for dev in devices:
        print(f"\n\nConnecting to {dev}:")
        result = sh_cmd_list_dev_list(dev, "gandalf", "grey", commands)
        pprint(result, width=120)
    
"""
OUTPUT GOVNO
(paramiko-venv) gandalf@debian11:~/Python/repo_paramiko$ python3 03_natasha.py 
{'sh arp': 'sh arp\r\n'
           'Protocol  Address          Age (min)  Hardware Addr   Type   Interface\r\n'
           'Internet  192.168.100.1           0   2cc8.1b89.4d53  ARPA   GigabitEthernet1\r\n'
           'Internet  192.168.100.4           2   0050.0000.0400  ARPA   GigabitEthernet1\r\n'
           'Internet  192.168.100.5           -   5000.0006.0000  ARPA   GigabitEthernet1\r\n'
           'Internet  192.168.100.6           0   aabb.cc00.3000  ARPA   GigabitEthernet1\r\n'
           'Internet  192.168.100.7           0   aabb.cc00.1000  ARPA   GigabitEthernet1\r\n'
           'Internet  192.168.100.67          3   8000.0b59.a02e  ARPA   GigabitEthernet1\r\n'
           'csr1000v-01#',
 'sh inv': 'sh inv\r\n'
           'NAME: "Chassis", DESCR: "Cisco CSR1000V Chassis"\r\n'
           'PID: CSR1000V          , VID: V00  , SN: 94N9U8ZRS16\r\n'
           '\r\n'
           'NAME: "module R0", DESCR: "Cisco CSR1000V Route Processor"\r\n'
           'PID: CSR1000V          , VID: V00  , SN: JAB1303001C\r\n'
           '\r\n'
           'NAME: "module F0", DESCR: "Cisco CSR1000V Embedded Services Processor"\r\n'
           'PID: CSR1000V          , VID:      , SN:            \r\n'
           '\r\n'
           '\r\n'
           'csr1000v-01#'}
           
KAK PARSIT ETO GOVNO - HUI ZNAET
"""