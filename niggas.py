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
import zipfile
import zlib
import io
import StringIO

class InMemoryZip(object):
    
    def __init__(self):
        # Create the in-memory file-like object
        self.in_memory_zip = StringIO.StringIO()
    def mfinit(self):
        global mf
        
        mf = StringIO.StringIO()

    def append(self, filename_in_zip, zf):
        zf.write(filename_in_zip)
        
    def writetofile(self):
        global mf
        global f
        f = file("test.zip", "a")
        f.write(mf.getvalue())
        print "test.zip created"
        f.close()

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
    numfiles = 0
    flag = 0
    global mf
    print "Listing files in current directory"
    path = os.getcwd()
    sys.path.append(path)
    files = os.listdir(path)
    for file1 in files:
        print num,'.',file1,'\n'
        num += 1
    data2 = "test.zip"    
    while True:
        imz = InMemoryZip()
        imz.mfinit()
        numfiles = raw_input("Number of files?")
        numfiles = int(numfiles)
        with zipfile.ZipFile(mf, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
            while flag!=numfiles:
                flag = flag+1
                data = raw_input("Which file?")
                if data!= "done":
                    imz.append(data, zf)
                else:
                    break

        imz.writetofile()
        print data2
        print 'written'
        print "The following data was received - ",data2
        print "Opening file - ",data2
        s.sendto(data2, (addrinfo[4][0], MYPORT))
        with open(data2, "rb") as imageFile:
            initial_data = imageFile.read()
            strng = base64.b64encode(initial_data)
            num_initial = len(initial_data)
            padding = { 0:0, 1:2, 2:1 }[num_initial % 3]
            l = len(strng)
            print l
            print '%d bytes before encoding' % num_initial
            print 'Expect %d padding bytes' % padding
            print '%d bytes after encoding' % l
            '''
            print
            #print encoded_data
            for i in xrange((l/40)+1):
                print strng[i*40:(i+1)*40]
            print l
            '''
            p = str(l)
            s.sendto(p, (addrinfo[4][0], MYPORT))
            k = 32767
            u = l/32768
            print u
            for j in range(u+1):
                if l<k:
                    k = l
                str2= strng[i : k]
                x = len(str2)
                tr = str(x)
                print tr
                s.sendto(tr, (addrinfo[4][0], MYPORT))

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
    words = fname.split(".")
    type1 = words[1]
    type2 = words[2]
    while True: 
        print "g"
        length, addr = s.recvfrom(4567)
        length = int(length)
        print length
        k2 = 32767
        i2 = 0
        u2 = length/32768
        st = ''''''
        print u2
        for j2 in range(u2+1):
            if length<k2:
                k2 = length
            stm, addr = s.recvfrom(60000)
            
            if k2>length:
                break
            else:
                i2 = k2
                k2 = k2+32767
            st += stm
        if type2 != "tar": 
            if type1 == "jpg":
                fh = open("imageToSave.jpg", "wb") 
            if type1 == "png":
                fh = open("imageToSave.png", "wb")
            if type1 == "mp4":
                fh = open("videoToSave.mp4", "wb")
            if type1 == "mkv":
                fh = open("videoToSave.mkv", "wb")
        elif type2 == "tar":
            fh = open("folder.tar.gz", "wb")
        missing_padding = 4 - len(st) % 4
        if missing_padding:
            st += b'='* missing_padding
        fh.write(base64.decodestring(st))
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
    f = open("test.zip", 'w')
    mf =0
    main()