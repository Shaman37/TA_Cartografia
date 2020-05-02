import re
import csv 
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Cartografia",timeout=10)
addresses = set()

out_header = ['Date','Country','City','no2_mean','Longitude','Latitude',]

result = list()

with open('waqi-covid19-airqualitydata-2020.csv','r') as file_in, open('no2_tracking.csv','w') as file_out:

    read = csv.reader(file_in, delimiter=',', skipinitialspace=True)
    next(read)

    filtered_no2 = filter(lambda x: x[3] in ("no2"), read)
    sorted_no2 = sorted(filtered_no2, key=lambda row: (row[1], row[2], row[0]))
 
    for row in sorted_no2:
        addresses.add(f"{row[1]} {row[2]}")  # Add "{Country Code} {City}" to address set
        
        if(not "2019" in row[0]):
            result.append([row[0],row[1],row[2],row[7]])

    addresses = sorted(list(addresses))

    coordinates = list()    
    
    for i,adr in enumerate(addresses):
        print(i,'->',adr)
        location = geolocator.geocode(adr)
        coordinates.append((location.longitude,location.latitude))

    coords_by_address = dict(zip(addresses,coordinates))

    print("# Adresses found = ",len(addresses))
    print("# Coordinates found = ",len(coordinates))

    out = csv.writer(file_out)
    out.writerow(out_header)

    for row in result:
        out.writerow(row + list(coords_by_address[f"{row[1]} {row[2]}"])) 