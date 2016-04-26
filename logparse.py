import re
import os
import geoip2.database
from datetime import datetime

# Path to the GeoLite database
geodb = "/GeoLite2-City.mmdb"
# Path to the Apache log file
logfile = "access.log"
# Current working directory
filepath = os.getcwd()

# Load up the GeoIP database
reader = geoip2.database.Reader(filepath + geodb)
          
# Open a file for writing out our CSV data
fout = open("iplocation.csv", 'w')     

# Open the Apache log file
with open(logfile) as fp:
  # For each line in the Apache log file
  for line in fp:
    # Get a list of IP matches on this line [:1] gives us first item in list
    iplist = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )[:1]
    # Get the first timestamp from the line [:1] gives us first item in list
    stamp = re.findall(r'\[(.*?)\]',line)[:1]
    # If we have a timestamp and ip address NOTE: once they are not empty lists
    if (iplist and stamp):
      try:
        # Make a nicer timestamp for the file - strip off timezone
        dstamp = stamp[0]
        dstamp = dstamp[0:dstamp.find(' ')]
        # Format the date to YYYY-MM-DD HH:MM:SS
        dstamp = datetime.strptime(dstamp,"%d/%b/%Y:%H:%M:%S")
        # Try to get a response back for the IP address
        response = reader.city(iplist[0])
        # Just do some output to make sure something is happening
        print str(dstamp) + " " + str(iplist[0]) + " " + response.country.name + " " + response.city.name
        # Write out the stamp,IP, Country, City
        fout.write(str(dstamp) + "," + str(iplist[0]) + "," + str(response.country.name) + "," + str(response.city.name + "\n"))
      except Exception as e:
        print "Cannot process IP address: " + str(iplist[0])

fout.close()
