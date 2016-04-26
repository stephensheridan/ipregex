import re
import os
import geoip2.database


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
    # Get a list of IP matches on this line
    iplist = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line )
    # Get the first timestamp from the line
    stamp = re.findall(r'\[(.*?)\]',line)[:1]
    # For each IP match in the list
    for ip in iplist:
      try:
        # Try to get a response back for the IP address
        response = reader.city(ip)
        # Just do some output to make sure something is happening
        print response.country.name + " " + response.city.name
        # Write out the stamp,IP, Country, City
        fout.write(str(stamp[0]) + "," + str(ip) + "," + str(response.country.name) + "," + str(response.city.name + "\n"))
      except Exception as e:
        print "Cannot process IP address: " + str(ip)

fout.close()
