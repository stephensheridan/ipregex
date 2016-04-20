import re
import os
import pygeoip


## Some Globals
geofilename = "/GeoLiteCity.dat"
logfile = "access.log"
filepath = os.getcwd()
rawdata = pygeoip.GeoIP(filepath + geofilename)


def ipquery(ip):
    try:
        data = rawdata.record_by_name(ip)
        country = data['country_name']
        city = data['city']
        longi = data['longitude']
        lat = data['latitude']
        ## Do some output to the console
        print ''
        print '[x] ' + ip
        print '[x] '+str(city)+',' +str(country)
        print '[x] Latitude: '+str(lat)+ ', Longitude: '+ str(longi)
    except Exception as e:
        print "Cannot process IP address: " + str(ip)
          
     

with open(logfile) as fp:
    for line in fp:
        iplist = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )
        for ip in iplist:
            print "***** " + str(ip) + " *****"
            ipquery(ip)