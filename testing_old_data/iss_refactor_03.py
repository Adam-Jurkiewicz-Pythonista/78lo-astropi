import numpy
from orbit import ISS
from datetime import datetime, timedelta
from math import sin, cos, acos, sqrt


def fun_dt(date_in):
    return (date_in / 240) * (3.1415 / 180)


def dist_calculation(altitude, slat, elat, slon, elon):
    return (6371.0 + altitude) * acos(
        sin(slat) * sin(elat) + cos(slat) * cos(elat) * cos(slon - elon)
    )


iss1 = ISS()
point = iss1.coordinates()
lat = [point.latitude.radians]
lon = [point.longitude.radians]
alt = [point.elevation.km]
# time_f.append(time_superduper.seconds)
# lat.append(point.latitude.radians)
# lon.append(point.longitude.radians)
# alt.append(point.elevation.km)

v1 = []
v2 = []
now_time = datetime.now()
start_time = now_time
costam_time = now_time
i = 0
time_superduper = timedelta(0)  # start_time-start_time
time_f = [time_superduper.seconds]
g = 0.0000000004454628049
m = 5972200000000000000000000
gm = 399000000000
iss1 = ISS()
while now_time <= (start_time + timedelta(minutes=2)):
    now_time = datetime.now()

    if now_time >= (costam_time + timedelta(seconds=10)):
        if i > 0:
            print(
                f"""{i=} secs: {time_f[i]} | lattitude: {lat[i]}
| longitude: {lon[i]} | elevation: {alt[i]} 
| v1: {v1[i - 1]} | v2: {v2[i - 1]}  """
            )

        time_superduper = datetime.now() - start_time
        point = iss1.coordinates()
        time_f.append(time_superduper.seconds)
        lat.append(point.latitude.radians)
        lon.append(point.longitude.radians)
        alt.append(point.elevation.km)

        i += 1
        slat = lat[i - 1]
        slon = lon[i - 1]
        elat = lat[i]
        elon = lon[i]
        dt = time_f[i] - time_f[i - 1]
        elon += fun_dt(dt)
        dist = dist_calculation(alt[i], slat, elat, slon, elon)

        v1.append(dist / dt)
        point = iss1.coordinates()
        total_R = 6370 + point.elevation.km
        v2.append(sqrt(gm / total_R) / 1000)

        costam_time = datetime.now()

s1 = numpy.std(v1, ddof=1)  # odchylenie standardowe tabeli v1
print(s1)
v1m = numpy.median(v1)  # mediana prędkości v1
print(v1m)
s2 = numpy.std(v2, ddof=1)  # odchylenie standardowe tabeli v2
v2m = numpy.median(v2)  # mediana prędkosci v2
print(v2m)


if s1 < s2:
    estimate_kmps = v1m
else:
    estimate_kmps = v2m

estimate_kmps_formatted = "{:.4f}".format(estimate_kmps)

# Create a string to write to the file
output_string = estimate_kmps_formatted

# Write to the file
file_path = "result.txt"  # Replace with your desired file path
with open(file_path, "w") as file:
    file.write(output_string)

print("Writing:" + output_string)
print("Data written to", file_path)
file.close()
print(f"Czas wykonania: {datetime.now()-start_time}")
