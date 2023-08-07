#!/usr/bin/env python

import paramiko, getpass, time

devices = {'iol-01': {'ip': '192.168.100.6'}, 
           'iol-02': {'ip': '192.168.100.7'}}
commands = ['show run | i hostname \n', 'show clock \n']
username = "gandalf"
password = getpass.getpass('Password: ')

max_buffer = 65535

def clear_buffer(connection):
    if connection.recv_ready():
        return connection.recv(max_buffer)
    
for device in devices.keys():
    outputFileName = "01_" + device + '_output.txt'
    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(devices[device]['ip'], username = username, password = password, look_for_keys=False, allow_agent = False)
    new_connection = connection.invoke_shell()
    output = clear_buffer(new_connection)
    with open(outputFileName, 'wb') as f:
        for command in commands:
            new_connection.send(command)
            time.sleep(2)
            output = new_connection.recv(max_buffer)
            print(output)
            f.write(output)


    new_connection.close()            

"""
OUTPUT GOVNO:
Password: 
b'iol-rtr157-02#show run | i hostname \r\nhostname iol-rtr157-02\r\niol-rtr157-02#'
b'show clock \r\n21:37:00.057 EET Mon Aug 7 2023\r\niol-rtr157-02#'
b'\r\niol-rtr157-01#show run | i hostname \r\nhostname iol-rtr157-01\r\niol-rtr157-01#'
b'show clock \r\n21:37:04.655 EET Mon Aug 7 2023\r\niol-rtr157-01#'
"""