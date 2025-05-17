# Drone-GPS-Spoofing-Detection
To identify GPS spoofing attacks by comparing the real-time GPS coordinates of a drone with its expected location. If the difference exceeds a defined threshold, the system flags a possible spoofing attempt

# Technologies Used:
Python 
mavsdk (Drone SDK)
asyncio for asynchronous tasks
Math functions (sin, cos, radians) for distance calculation using Haversine formula

# Core Functionality
# Haversine Formula: 
Calculates the distance between two GPS coordinates on the Earth's surface.

# Spoof Detection: 
Compares the current GPS coordinates to an expected location.

# Async Drone Communication:
Connects to the drone via MAVSDK using localhost and a port.
Waits for a connection with a timeout.
Streams GPS data and checks every few seconds.

# Alerts:
Prints a warning if the drone is detected far from the expected coordinates.
