from oretPixControl import connectToPix, distance_to_wp, download_mission
from advancecal import calc
import time, math

wp = 0
vehicle_speed = 0
vehicle_alt = 0
dist = 0
projectile_dist = 0

try:
    vehicle = connectToPix()
    download_mission()
except:
    print "Error accures while connecting"

wp = input("Type number of wp for drop: ")
    
download_mission()
while True:
    alt   = vehicle.location.global_relative_frame.alt
    speed = vehicle.groundspeed
    dist  = distance_to_wp(wp)
    projectile_dist = calc(alt, speed)
    try:
        if (dist <= projectile_dist):
            print "Drop at " + str(dist) + " m distance, " + str(vehicle.groundspeed) + "m/s speed, " + str(vehicle.location.global_relative_frame.alt) + "m alt"
            break
    except:
        print "error"
    print str(dist) + "--" + str(projectile_dist)


