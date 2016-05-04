#!/usr/bin/env python
#
# Send/receive UDP multicast packets.
# Requires that your OS kernel supports IP multicast.
#
# Usage:
#   mcast -s (sender, IPv4)
#   mcast -s -6 (sender, IPv6)
#   mcast    (receivers, IPv4)
#   mcast  -6  (receivers, IPv6)

MYPORT = 8002
MYGROUP_4 = '225.0.0.250'
MYGROUP_6 = 'ff15:7079:7468:6f6e:6465:6d6f:6d63:6173'
MYTTL = 5 # Increase to reach other networks

import time
import struct
import socket
import sys
import os
import base64
from PIL import Image
import io


def main():
    group = MYGROUP_6 if "-6" in sys.argv[1:] else MYGROUP_4

    if "-s" in sys.argv[1:]:
        sender(group)
    else:
        receiver(group)


def sender(group):
    addrinfo = socket.getaddrinfo(group, None)[0]
    print addrinfo
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    # Set Time-to-live (optional)
    ttl_bin = struct.pack('@i', MYTTL)
    if addrinfo[0] == socket.AF_INET: # IPv4
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
    else:
        s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)
    strng = ''''''    
    i = 0
    num =1
    print "Listing files in current directory"
    path = os.getcwd()
    sys.path.append(path)
    files = os.listdir(path)
    for file1 in files:
        print num,'.',file1,'\n'
        num += 1
    while True:
        data = raw_input("Which file?")
        print "The following data was received - ",data
        print "Opening file - ",data
        s.sendto(data, (addrinfo[4][0], MYPORT))
        with open(data, "rb") as imageFile:
            strng = base64.b64encode(imageFile.read())
            l = len(strng)
            print l
            p = str(l)
            s.sendto(p, (addrinfo[4][0], MYPORT))
            k = 32767
            u = l/32768
            print u
            for j in range(u+1):
                if l<k:
                    k = l
                str2= strng[i : k]
                s.sendto(str2, (addrinfo[4][0], MYPORT))
                if k>l:
                    break
                else:
                    i = k
                    k = k+32767
            print "Data sent successfully"
        exit()


def receiver(group):
    # Look up multicast group address in name server and find out IP version
    addrinfo = socket.getaddrinfo(group, None)[0]

    # Create a socket
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    # Allow multiple copies of this program on one machine
    # (not strictly needed)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 5)
    
    
    # Bind it to the port
    s.bind((MYGROUP_4, MYPORT))

    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    # Join group
    if addrinfo[0] == socket.AF_INET: # IPv4
        mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    else:
        mreq = group_bin + struct.pack('@I', 0)
        s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    # Loop, printing any data we receive
    fname, addr = s.recvfrom(4567)
    print fname
    #fname = "file.zip"
    words = fname.split(".")
    type1 = words[1]
    print type1
    #type2 = words[2]
    while True: 
        print "inside client"
        length, addr = s.recvfrom(4567)
        length = int(length)
        print length
        #length = 100000
        k2 = 32767
        i2 = 0
        u2 = length/32768
        st = ''''''
        yy= ''''''
        print u2
        for j2 in range(u2+1):
            if length<k2:
                k2 = length
            trial,addr = s.recvfrom(1024)
            print int(trial)
            stm, addr = s.recvfrom(60000)
            
            if k2>length:
                break
            else:
                i2 = k2
                k2 = k2+32767
            st += stm
            
        print type1
        if type1 == "zip": 
            fh = open("folder.zip", "wb")
        #print encoded_data
        '''
        l = len(st)
        for i in xrange((l/40)+1):
            print st[i*40:(i+1)*40]
        print l
            
        missing_padding = 4 - len(st) % 4
        
        if missing_padding:
            st += b'='* missing_padding
        
        if missing_padding == 3:
            st += b'==' 
        elif missing_padding == 1 or missing_padding == 2:
            st += b'=' * missing_padding
    
        if len(st) % 4 != 0:
            missing_padding = 4 - (len(st) % 4)
            st = ''.join((st,'='* missing_padding))
        '''
        yy = base64.b64decode(st)
        fh.write(yy)
        fh.close()
        print "Data Received successfully"
        #if type1 == "jpg":
        #    img = Image.open(StringIO('imageToSave.jpg')) 
        #if type1 == "png":
        #    img = Image.open('imageToSave.png')
        
        #img.show()
        '''
        try:
            pilImg.load()
        except IOError:
            pass # You can always log it to logger
        '''

        exit()
        #data = 'viewnior '+fname
        #os.system(data)
        

if __name__ == '__main__':
    main()