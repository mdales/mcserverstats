#!/usr/bin/env python

import re
import sys
import time
from urllib import urlopen, urlencode

URL_PREFIX = sys.argv[1]
LOG_FILE = sys.argv[2]

logfile = open(LOG_FILE, "r")

join_re = re.compile('^([0-9\ :\-]+) \[INFO\] ([\w_]+) {0,1}\[.* logged in.*$')
leave_re = re.compile('^([0-9\ :\-]+) \[INFO\] ([\w_]+) lost connection.*$')
death_re = re.compile('^([0-9\ :\-]+) \[INFO\] ([\w_]+) ([\w ]+)$')

users = set()

while True:
    
    entry = logfile.readline()
    
    if entry == None or entry == '':
        time.sleep(5)
        continue
    
    match = join_re.match(entry)
    if match:
        raw = match.groups()
        info = {'username': raw[1], 
            'datetime': raw[0]}                
        
        users.add(raw[1])
        
        urlopen("%s/join/" % URL_PREFIX, data=urlencode(info)).close()
        time.sleep(0.5)
        continue
        
    match = leave_re.match(entry)
    if match:
        raw = match.groups()
        info = {'username': raw[1], 
            'datetime': raw[0]}                
        
        users.add(raw[1])
                
        urlopen("%s/leave/" % URL_PREFIX, data=urlencode(info)).close()
        time.sleep(0.5)
        continue
    
    match = death_re.match(entry)
    if match:
        raw = match.groups()
        
        if raw[1] in users:
            info = {'username': raw[1], 
                'datetime': raw[0],
                'reason': raw[2]}      
            urlopen("%s/died/" % URL_PREFIX, data=urlencode(info)).close()
            time.sleep(0.5)

        continue