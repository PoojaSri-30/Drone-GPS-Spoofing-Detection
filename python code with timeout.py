import asyncio
from mavsdk import System
from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000.0  # Earth radius in meters
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c 

def check_spoofing(lat, lon, expected_lat, expected_lon, threshold):
    dist = calculate_distance(lat, lon, expected_lat, expected_lon)
    if dist > threshold:
        print(f"Possible GPS spoofing detected! Distance: {dist} meters.")
        
    else:
        print(f"GPS data seems valid. Distance: {dist} meters.")

async def main():
    drone = System(mavsdk_server_address="localhost", port=50051
    print("Connecting to the drone...")

    try:
        # Set timeout for connection attempt
        await asyncio.wait_for(drone.connect(system_address="udp://:14540"), timeout=60)
    except asyncio.TimeoutError:
        print("Failed to connect to drone. Connection timed out.")
        return

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected!")
            break
    else:
        print("Drone not connected! Check the connection and try again.")
        return

    expected_lat = 20.0
    expected_lon = 77.0
    threshold = 100.0  # meters

    print("Waiting for GPS data...")
    try:
        async for position in drone.telemetry.position():
            print("Received GPS position:", position)
            current_lat = position.latitude_deg
            current_lon = position.longitude_deg
            print(f"Current GPS Position: Latitude: {current_lat}, Longitude: {current_lon}")
            check_spoofing(current_lat, current_lon, expected_lat, expected_lon, threshold)

            await asyncio.sleep(120)  # Run for 2 minutes
            break
    except Exception as e:
        print(f"Error receiving telemetry: {e}")

if __name__ == "__main__":
    asyncio.run(main())
