from xml.etree import ElementTree
import time
from datetime import datetime

def parse(string):
    if 'gpxdata:' in string:
        string = string.replace('gpxdata:', '')
    elem = ElementTree.fromstring(string)
    track = []

    for trkpt in elem.getiterator("{http://www.topografix.com/GPX/1/1}trkpt"):
        lat = float(trkpt.get("lat"))
        lon = float(trkpt.get("lon"))
        ele = int(float(trkpt.findtext("{http://www.topografix.com/GPX/1/1}ele")))
        timestr = trkpt.findtext("{http://www.topografix.com/GPX/1/1}time")
        if len(timestr) == 20:
            dtime = int(time.mktime(datetime.strptime(timestr, '%Y-%m-%dT%H:%M:%SZ').timetuple()))
        else:
            dtime = int(time.mktime(datetime.strptime(timestr[:19], '%Y-%m-%dT%H:%M:%S').timetuple()))

        track.append([lat, lon, ele, dtime])

    return track

if __name__ == '__main__':
    import sys
    with open(sys.argv[1], 'r') as f:
        str = f.read()
        print parse(str)

