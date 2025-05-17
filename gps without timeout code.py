import asyncio
from mavsdk import System
from math import sin, cos, sqrt, atan2, radians

# Function to calculate the distance between two geographic points
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000.0  # Earth radius in meters

    # Convert degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Function to check for GPS spoofing
def check_spoofing(lat, lon, expected_lat, expected_lon, threshold):
    dist = calculate_distance(lat, lon, expected_lat, expected_lon)
    if dist > threshold:
        print(f"Possible GPS spoofing detected! Distance: {dist} meters.")
    else:
        print(f"GPS data seems valid. Distance: {dist} meters.")

async def main():
    # Connect to mavsdk_server on localhost:50051
    print("Connecting to the drone...")
    drone = System(mavsdk_server_address="localhost", port=50051)
    await drone.connect(system_address="udp://:14540")

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
    async for position in drone.telemetry.position():
        print("Received GPS position:", position)
        current_lat = position.latitude_deg
        current_lon = position.longitude_deg

        print(f"Current GPS Position: Latitude: {current_lat}, Longitude: {current_lon}")
        check_spoofing(current_lat, current_lon, expected_lat, expected_lon, threshold)

        # Exit after running for 1 minutes (or adjust as needed)
        await asyncio.sleep(60)  # 1 minutes
        break

if __name__ == "__main__":
    asyncio.run(main())
