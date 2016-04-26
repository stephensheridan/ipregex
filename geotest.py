import geoip2.database

reader = geoip2.database.Reader('GeoLite2-City.mmdb')

response = reader.city('128.101.101.101')

country = response.country.name
city = response.city.name

print country + " " + city
