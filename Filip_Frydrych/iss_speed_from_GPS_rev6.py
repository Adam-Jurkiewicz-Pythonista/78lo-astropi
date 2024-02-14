if __name__ == "__main__":


#library import
    
    from orbit import ISS
    from datetime import datetime, timedelta
    from math import radians, sin, cos, acos, sqrt
    from sense_hat import SenseHat
    import time
    import numpy

#variables and constants definitions
    G=6.67430E-11                          #G - gravity constant N*m2/kg2
    M=5972200000000000000000000            # mass of Earth, kg
    time_f=[]                              #table for time
    lat=[]                                 #table for WGS84 coordinate - lattitude N S
    lon=[]                                 #table for WGS84 coordinate - longitude W E
    alt=[]                                 #table for altitude of ISS
    v1=[]                                  #table for ISS velocity calculated from WGS84 coordinates change in time
    v2=[]                                  #table for ISS velocity calculated from formula for satelite speed v=sqrt[G*M/(R+alt)]
    gyro_x=[]
    gyro_y=[]
    gyro_z=[]
    ITERATION_TIME=10                      #number of seconds for each iteration delay
    RUN_TIME=1                             #main program part working time in minutes (max 8 minutes)

#objects definitions
    iss1=ISS()
    sense = SenseHat()
    
#start of the program - setup
    
    print("Filip Frydrych - Program started")
    now_time = datetime.now()                          #current time
    start_time = now_time                              #saving start time to check if program runs longer than 8 minutes
    loop_time = now_time                               #temporary time inside the loop, to check if 10 seconds have passed
    i=0;                                               #counter for variable tables
    point = iss1.coordinates()                         #point containing current ISS coordinates
    time_difference = start_time-start_time            #timedifference zero - definition of differential time variable
    time_f.append(time_difference.seconds)             #initial time difference = 0
    lat.append(point.latitude.radians)                 #initial lattitude in radians
    lon.append(point.longitude.radians)                #initial longitude in radians
    alt.append(point.elevation.km)                     #initial elevation
    gyro_raw = sense.get_gyroscope_raw()           
    tgyro_x = gyro_raw["x"] * 180 / 3.14159
    tgyro_y = gyro_raw["y"] * 180 / 3.14159
    tgyro_z = gyro_raw["z"] * 180 / 3.14159
    gyro_x.append(tgyro_x)
    gyro_y.append(tgyro_y)
    gyro_z.append(tgyro_z)
    print('t=' + str(time_f[i]) +'sec,  lattitude=' + str(lat[i]) +' rad, longitude=' + str(lon[i]) + ' rad, elevation=' + str(alt[i]) +" km")


#main calculating loop

    while (now_time <= (start_time + timedelta(minutes=RUN_TIME))):            #run for RUN_TIME in minutes
        now_time = datetime.now()                                              #save current time
        
        if now_time >= (loop_time + timedelta(seconds=ITERATION_TIME)):        #after every ITERATION_TIME seconds do calculations
            
            time_difference = datetime.now()-start_time
            
            #CALCULATION OF SPEED ON A BASIS OF COORDINATES
            
            point = iss1.coordinates()
            time_f.append(time_difference.seconds)
            lat.append(point.latitude.radians)
            lon.append(point.longitude.radians)
            alt.append(point.elevation.km)
            i=i+1
            start_lat=lat[i-1]
            start_lon=lon[i-1]
    
            end_lat=lat[i]
            end_lon=lon[i]
    
            dt=time_f[i]-time_f[i-1]
    
            end_lon=end_lon+((dt/240)*(3.1415/180))    #added displacement of ending longitude due to Earth rotation in dt
    
            #calculate distance travelled by ISS on a basis of WGS84 coordinates replacement
            dist = (6371.0 + alt[i]) * acos(sin(start_lat)*sin(end_lat)+cos(start_lat)*cos(end_lat)*cos(start_lon-end_lon))
            #calculate ISS speed
            iss_speed=dist/(dt)
            #append calculated speed to table
            v1.append(iss_speed)
            
            
            #CALCULATION OF SPEED ON A BASIS OF RADIUS OF A SATELITE v=sqrt[G*M/(R+alt)]
            
            
            point = iss1.coordinates()
            total_R=6370+point.elevation.km
            kkk =G*M/(total_R*1000)
            iss_speed2=sqrt(kkk)/1000
            v2.append(iss_speed2)
            print('t=' + str(time_f[i]) +'sec, lattitude=' + str(lat[i]) +' rad, longitude=' + str(lon[i]) + ' rad, elevation=' + str(alt[i]) + " km, v1= " + str(v1[i-1]) +" km/s, v2= " + str(v2[i-1]) + " km/s")
            
            
            #SAVING OF GYROSCOPE DATA
            gyro_raw = sense.get_gyroscope_raw()
            
            tgyro_x = gyro_raw["x"] * 180 / 3.14159
            tgyro_y = gyro_raw["y"] * 180 / 3.14159
            tgyro_z = gyro_raw["z"] * 180 / 3.14159
            gyro_x.append(tgyro_x)
            gyro_y.append(tgyro_y)
            gyro_z.append(tgyro_z)
            
            
            print("x= "+str(tgyro_x)+" deg/s  y= "+str(tgyro_y)+" deg/s   z= "+str(tgyro_z)+" deg/s")
            
            loop_time = datetime.now()


#data acquired, final calculations and results saving
            
            
    s1 = numpy.std(v1, ddof=1) # odchylenie standardowe tabeli v1
    print(s1)
    v1m = numpy.median(v1) # mediana prędkości v1
    print(v1m)
    s2 = numpy.std(v2, ddof=1) # odchylenie standardowe tabeli v2
    v2m = numpy.median(v2) # mediana prędkosci v2
    print(v2m)

    
    if(s1<s2):
        estimate_kmps=v1m
    else:
        estimate_kmps=v2m
        
    estimate_kmps_formatted = "{:.4f}".format(estimate_kmps)

    # Create a string to write to the file
    output_string = estimate_kmps_formatted

    # Write to the file
    file_path = "result.txt"  # Replace with your desired file path
    with open(file_path, 'w') as file:
        file.write(output_string)
    
    print("Writing:" + output_string)
    print("Data written to", file_path)     
    file.close()    
