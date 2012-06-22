#read in logfile and convert to json
import re
import sys
import time
import httplib
import datetime
import itertools
import simplejson
#read in from file using command line
args = sys.argv[1:]
if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

todir = ''
if args[0] == '--todir':
    todir = args[1]
    del args[0:2]
f = open(args[0])
f2 = open("output.json","w")
#define compile method
LOGLINE = re.compile(
   r'(?P<origin>\d+\.\d+\.\d+\.\d+) '
   + r'(?P<identd>-|\w*) (?P<auth>-|\w*) '
   + r'\[(?P<ts>(?P<date>[^\[\]:]+):(?P<time>\d+:\d+:\d+)) (?P<tz>[\-\+]?\d\d\d\d)\] '
   + r' "(?P<method>\w+) (?P<path>[\S]+) (?P<protocol>[^"]+)" (?P<status>\d+) (?P<bytes>-|\d+)'
   + r' "(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"'
   + r' "(?P<calling_line_id>[^"]*)" "(?P<vodafone_area>[^"]*)"'
   )
   
#create timestamps
class timezone(datetime.tzinfo):
    def __init__(self, name="+0000"):
        self.name = name
        seconds = int(name[:-2])*3600+int(name[-2:])*60
        self.offset = datetime.timedelta(seconds=seconds)

    def utcoffset(self, dt):
        return self.offset

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return self.name

def parse_apache_date(date_str, tz_str):
    '''
    Parse the timestamp from the Apache log file, and return a datetime object
    '''
    tt = time.strptime(date_str, "%d/%b/%Y:%H:%M:%S")
    tt = tt[:6] + (0, timezone(tz_str))
    return datetime.datetime(*tt)

entries = []
   
#read every line in file and match info
for i,line in enumerate(f):
    match_info = LOGLINE.match(line)
    entry = {}
    timestamp = parse_apache_date(match_info.group('ts'), match_info.group('tz'))
    timestamp_str = timestamp.isoformat()
    entry['id'] = match_info.group('origin') + ':' + timestamp_str + ':' + str(i)
    entry['origin'] = match_info.group('origin')
    entry['timestamp'] = timestamp_str
    entry['path'] = match_info.group('path')
    entry['method'] = match_info.group('method')
    entry['protocol'] = match_info.group('protocol')
    entry['status'] = match_info.group('status')
    entry['status'] += ' ' + httplib.responses[int(entry['status'])]
    if match_info.group('bytes') != '-':
        entry['bytes'] = match_info.group('bytes')
    if match_info.group('referrer') != '"-"':
        entry['referrer'] = match_info.group('referrer')
    entry['user_agent'] = match_info.group('user_agent')
    entry['calling_line_id'] = match_info.group('calling_line_id')
    entry['vodafone_area'] = match_info.group('vodafone_area')
    entries.append(entry)
    

sour=simplejson.dumps({'items': entries}, indent=4)

f2.write(sour)

f2.close()
    