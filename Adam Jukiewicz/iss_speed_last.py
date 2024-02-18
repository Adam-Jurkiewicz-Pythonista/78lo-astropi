from orbit import ISS
from datetime import datetime, timedelta
from math import sin, cos, acos, sqrt
from sense_hat import SenseHat
from pathlib import Path
import numpy

# variables and constants definitions
G = 6.67430e-11  # G - gravity constant N*m2/kg2
M = 5972200000000000000000000  # mass of Earth, kg
time_f = []  # table for time
lat = []  # table for WGS84 coordinate - lattitude N S
lon = []  # table for WGS84 coordinate - longitude W E
alt = []  # table for altitude of ISS
v1 = []  # table for ISS velocity calculated from WGS84 coordinates change in time
v2 = (
    []
)  # table for ISS velocity calculated from formula for satelite speed v=sqrt[G*M/(R+alt)]
gyro_x = []
gyro_y = []
gyro_z = []
accelerator_x = []
accelerator_y = []
accelerator_z = []
ITERATION_TIME = 1  # number of seconds for each iteration delay
RUN_TIME = 8  # main program part working time in minutes (max 9 minutes)

# objects definitions
iss1 = ISS()
sense = SenseHat()
base_folder = Path(__file__).parent.resolve()
data_file = base_folder / "data.txt"
result_file = base_folder / "result.txt"
result2_file = base_folder / "result2.txt"

# start of the program - setup

print("Program started")
now_time = datetime.now()  # current time
start_time = (
    now_time  # saving start time to check if program runs longer than 8 minutes
)
loop_time = (
    now_time  # temporary time inside the loop, to check if 10 seconds have passed
)
i = 0  # counter for variable tables
point = iss1.coordinates()  # point containing current ISS coordinates
time_difference = (
    start_time - start_time
)  # timedifference zero - definition of differential time variable
time_f.append(time_difference.seconds)  # initial time difference = 0
lat.append(point.latitude.radians)  # initial lattitude in radians
lon.append(point.longitude.radians)  # initial longitude in radians
alt.append(point.elevation.km)  # initial elevation
gyro_raw = sense.get_gyroscope_raw()  # acquire for gyro data
tgyro_x = gyro_raw["x"] * 180 / 3.14159  # radians to degrees
tgyro_y = gyro_raw["y"] * 180 / 3.14159
tgyro_z = gyro_raw["z"] * 180 / 3.14159
gyro_x.append(tgyro_x)  # initial gyro readings wrote to tables
gyro_y.append(tgyro_y)
gyro_z.append(tgyro_z)

# main calculating loop
while now_time <= (
    start_time + timedelta(minutes=RUN_TIME)
):  # run for RUN_TIME in minutes
    now_time = datetime.now()  # save current time

    if now_time >= (
        loop_time + timedelta(seconds=ITERATION_TIME)
    ):  # after every ITERATION_TIME seconds do calculations
        time_difference = datetime.now() - start_time

        # CALCULATION OF SPEED ON A BASIS OF WGS84 COORDINATES

        point = iss1.coordinates()
        time_f.append(time_difference.seconds)
        lat.append(point.latitude.radians)
        lon.append(point.longitude.radians)
        alt.append(point.elevation.km)
        i = i + 1
        start_lat = lat[i - 1]
        start_lon = lon[i - 1]

        end_lat = lat[i]
        end_lon = lon[i]

        dt = time_f[i] - time_f[i - 1]

        end_lon = end_lon + (
            (dt / 240) * (3.1415 / 180)
        )  # added displacement of ending longitude due to Earth rotation in dt

        # calculate distance travelled by ISS on a basis of WGS84 coordinates replacement
        dist = (6371.0 + alt[i]) * acos(
            sin(start_lat) * sin(end_lat)
            + cos(start_lat) * cos(end_lat) * cos(start_lon - end_lon)
        )
        # calculate ISS speed
        iss_speed = dist / dt
        # append calculated speed to table
        v1.append(iss_speed)

        # CALCULATION OF SPEED ON A BASIS OF RADIUS OF A SATELITE ORBIT v=sqrt[G*M/(R+alt)]

        point = iss1.coordinates()
        total_R = (
            6370 + point.elevation.km
        )  # Current altitude of ISS, meters above the ground
        kkk = G * M / (total_R * 1000)
        iss_speed2 = sqrt(kkk) / 1000
        v2.append(iss_speed2)

        # SAVING OF GYROSCOPE DATA
        gyro_raw = sense.get_gyroscope_raw()  # getting gyroscope values

        tgyro_x = gyro_raw["x"] * 180 / 3.14159  # converting x radians to degrees
        tgyro_y = gyro_raw["y"] * 180 / 3.14159  # converting y radians to degrees
        tgyro_z = gyro_raw["z"] * 180 / 3.14159  # converting z radians to degrees
        gyro_x.append(tgyro_x)  # appending gyro x value to the gyro x table
        gyro_y.append(tgyro_y)  # appending gyro y value to the gyro y table
        gyro_z.append(tgyro_z)  # appending gyro z value to the gyro z table

        # GETTING ACCELERATOR DATA

        accelerator_raw = sense.get_accelerator_raw()  # getting accelerator values
        accelerator_x.append(
            accelerator_raw["x"]
        )  # appending accelerator x value to the gyro x table
        accelerator_y.append(
            accelerator_raw["y"]
        )  # appending accelerator y value to the gyro y table
        accelerator_z.append(
            accelerator_raw["z"]
        )  # appending accelerator z value to the gyro z table

        loop_time = datetime.now()

# END OF LOOP
# data acquired, final calculations and results saving


s1 = numpy.std(v1, ddof=1)  # standard deviation of calculated v1
# print(s1)
v1m = numpy.median(v1)  # mediana of calculated v1
# print(v1m)
s2 = numpy.std(v2, ddof=1)  # standard deviation of calculated v2
# print(s2)
v2m = numpy.median(v2)  # mediana of calculated v2
# print(v2m)


if s1 < s2:  # better result is saved to the file
    estimate_kmps = v1m
else:
    estimate_kmps = v2m

estimate_kmps_formatted = "{:.4f}".format(estimate_kmps)

# Create a string to write to the file
output_string = estimate_kmps_formatted

# Write to the file

with open(result2_file, "w") as file2:
    file2.write(output_string)
# print("Writing:" + output_string)
# print("Result written to ", result2_file)
# file2.close()

gxm = numpy.median(gyro_x)  # mediana of rotation speed axis x
gym = numpy.median(gyro_y)  # mediana of rotation speed axis y
gzm = numpy.median(gyro_z)  # mediana of rotation speed axis m

gmax = max(
    gxm, gym, gzm
)  # checking which axis describes iss movement- the highest value is the right one

# print("gx=" + str(gxm) + "gy=" + str(gym) + "gz=" + str(gzm)) #printing the average x, y and z rotating speed values

ISS_T = (360 / gmax) / 60
# print("ISS time for full orbit:" +str(ISS_T) + " min") #printing full orbit (360) time

estimate_kmps = (
    2 * 3.14159 * (6371.0 + numpy.median(alt)) / (ISS_T * 60)
)  # calculating iss speed
estimate_kmps_formatted2 = "{:.4f}".format(estimate_kmps)  # formatting calculated speed
# Create a string to write to the file
output_string = estimate_kmps_formatted2
# print("ISS speed calculated from gyroscope:" + output_string + "km/s" ) #printing iss speed from gyro
# Write to the file

with open(result_file, "w") as file1:
    file1.write(output_string)
# print("Writing:" + output_string)
# print("Result written to ", result_file)
# file1.close()

# getting extra data and saving it for future
L = []
for j in range(0, i):
    L.append(
        "time_f="
        + str(time_f[j])
        + ", lat="
        + str(lat[j])
        + ", lon="
        + str(lon[j])
        + ", alt="
        + str(alt[j])
        + ", v1="
        + str(v1[j])
        + ", v2="
        + str(v2[j])
        + ", gx="
        + str(gyro_x[j])
        + ", gy="
        + str(gyro_y[j])
        + ", gz="
        + str(gyro_z[j])
        + ", accelx="
        + str(accelerator_x[j])
        + ", acely="
        + str(accelerator_x[j])
        + ", accelz="
        + str(accelerator_z[j])
        + "\n"
    )

with open(data_file, "w") as file3:
    file3.writelines(L)
# print("Data written to ", data_file)
# file3.close()
