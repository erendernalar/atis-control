from dronekit import connect, Command, VehicleMode, LocationGlobalRelative, LocationGlobal
from pymavlink import mavutil
import time
import math

cmds = 0

def connectToPix():
    print ("Attemting to connect vehicle")
    global vehicle
    vehicle = connect('udp:127.0.0.1:14551',_initialize=True)
    print("Connected to the vehicle")
    return vehicle

#Variables
topCapChannel = 6
bottomCapChannel = 5

rudderCoefficient = 900

#End Variables

#Functions



def OpenTopCap():
    vehicle.channels.overrides['6'] = 800

def OpenBottomCap():
    vehicle.channels.overrides[str(bottomCapChannel)] = 800

def RudderOverride(value):
    val = 1500 + (value * rudderCoefficient)
    vehicle.channels.overrides['4'] = val

def CloseTopCap():
    vehicle.channels.overrides[str(topCapChannel)] = 2200

def CloseBottomCap():
    vehicle.channels.overrides[str(bottomCapChannel)] = 2200

def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.
    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5

def download_mission():
    global cmd
    cmd = vehicle.commands
    cmd.download()
    cmd.wait_ready()

def GetDistanceToNextPoint():
    nextwaypoint = vehicle.commands.next
    if nextwaypoint == 0:
        return 1000
    missionitem = cmd[nextwaypoint-1] #commands are zero indexed
    lat = missionitem.x
    lon = missionitem.y
    alt = vehicle.location.global_relative_frame.alt
    targetWaypointLocation = LocationGlobalRelative(lat,lon,alt)
    distancetopoint = get_distance_metres(vehicle.location.global_frame, targetWaypointLocation)
    return distancetopoint


def estimatedSec():
    time = math.sqrt(vehicle.location.global_relative_frame.alt / 4.905)
    return time 

def distance_to_wp(wp):
    nextwaypoint = vehicle.commands.next - 1
    if nextwaypoint == 0:
        return 1000
    missionitem = cmd[wp - 1] #commands are zero indexed
    lat = missionitem.x
    lon = missionitem.y
    alt = vehicle.location.global_relative_frame.alt
    targetWaypointLocation = LocationGlobalRelative(lat,lon,alt)
    distancetopoint = get_distance_metres(vehicle.location.global_frame, targetWaypointLocation)
    return distancetopoint

#    missionitem = vehicle.commands[wp - 1]
#    distancetopoint = get_distance_metres(vehicle.location.global_frame, targetWaypointLocation)
#    time = distancetopoint / vehicle.groundspeed
#    return time

    
def getNextWaypoint():
    return vehicle.commands.next - 1
#End Functions