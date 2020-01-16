from oretPixControl import connectToPix, distance_to_wp, download_mission
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

def payload_fly_time():
    alt = vehicle.location.global_relative_frame.alt
    time = math.sqrt(2 * alt / 9.81)
    return time

def projectile_range():
    p_range = vehicle.groundspeed * payload_fly_time()
    return p_range
    
download_mission()
while True:
    dist = distance_to_wp(wp)
    projectile_dist = projectile_range()
    try:
        if (dist <= projectile_dist):
            print "Drop at " + str(dist) + " m distance, " + str(vehicle.groundspeed) + "m/s speed, " + str(vehicle.location.global_relative_frame.alt) + "m alt"
            break
    except:
        print "error"


