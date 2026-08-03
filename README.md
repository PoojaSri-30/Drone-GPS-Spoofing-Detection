# Drone GPS Spoofing Detection

![Python](https://img.shields.io/badge/Python-3-3776AB?style=flat&logo=python&logoColor=white)
![MAVSDK](https://img.shields.io/badge/MAVSDK-Drone%20SDK-0091FF?style=flat)
![MAVLink](https://img.shields.io/badge/Protocol-MAVLink-orange?style=flat)
![asyncio](https://img.shields.io/badge/asyncio-async%2Fawait-3776AB?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-3776AB?style=flat)

A real-time monitoring tool that detects GPS spoofing attempts on a drone by streaming live GPS telemetry via **MAVSDK** and comparing it against an expected location using the **Haversine formula**. If the live position drifts beyond a configurable distance threshold, the system flags a possible spoofing attempt.

## Overview

GPS spoofing is a class of attack where an adversary broadcasts fake GPS signals to trick a drone (or any GNSS receiver) into believing it's somewhere it isn't — a serious risk for autonomous and remotely piloted aircraft. This project implements a lightweight, real-time detector: it streams the drone's live GPS position, computes the great-circle distance to a known/expected coordinate, and raises an alert when that distance exceeds a safety threshold.

**Pipeline:**
```
MAVSDK connects to drone (SITL or real, over UDP)
        → streams live GPS telemetry (async)
        → Haversine distance to expected coordinate
        → threshold check → valid / spoofing alert
```

## Core Functionality

| Component | What it does |
|---|---|
| **Haversine distance** | Calculates the great-circle distance in meters between two GPS coordinates, accounting for Earth's curvature (`R = 6,371,000 m`) |
| **Spoof detection** | Compares the drone's live `(lat, lon)` against an expected `(lat, lon)`; flags a possible spoof if the distance exceeds the threshold (default: **100 m**) |
| **Async drone communication** | Connects to the drone via `mavsdk.System` over UDP (`udp://:14540`), waits for the connection to establish, then streams telemetry asynchronously |
| **Alerting** | Prints a warning to the console when the distance threshold is exceeded, otherwise confirms the GPS data looks valid |

## Two Script Variants

The repo contains two versions of the detector:

- **`gps without timeout code.py`** — the baseline version. Connects to the drone and blocks indefinitely waiting for a connection; streams position for ~1 minute before exiting.
- **`python code with timeout.py`** — adds connection resilience: wraps the connection attempt in `asyncio.wait_for(..., timeout=60)` so the script fails gracefully instead of hanging if the drone never responds, wraps telemetry streaming in a `try/except` for error recovery, and runs for ~2 minutes.

> ⚠️ **Known issue:** `python code with timeout.py` currently has a syntax error — the `System(...)` constructor call is missing its closing parenthesis, so this file won't run as-is. Fix: close the call as `System(mavsdk_server_address="localhost", port=50051)`.

## Tech Stack

- **Python 3**
- **[MAVSDK-Python](https://github.com/mavlink/MAVSDK-Python)** — async drone telemetry and control over MAVLink
- **asyncio** — non-blocking connection handling and telemetry streaming
- **math** (`sin`, `cos`, `sqrt`, `atan2`, `radians`) — Haversine distance calculation

## How It Works

1. Connects to a running `mavsdk_server` instance (`localhost:50051`) which bridges to the drone over MAVLink (`udp://:14540`) — this can be a real drone or a SITL (Software-In-The-Loop) simulator such as PX4 or ArduPilot.
2. Waits for `drone.core.connection_state()` to confirm the link is live.
3. Streams `drone.telemetry.position()` and, for each update, computes the Haversine distance between the live coordinate and a hardcoded expected coordinate.
4. If the distance exceeds the threshold, logs a spoofing warning; otherwise confirms the position is valid.

## Getting Started

### Prerequisites
```bash
pip install mavsdk
```
You'll also need a running MAVSDK server and a drone connection — either a real vehicle or a simulator (e.g. [PX4 SITL](https://docs.px4.io/main/en/simulation/)) broadcasting on UDP port 14540.

### Configuration
Set your expected coordinate and alert threshold at the top of `main()`:
```python
expected_lat = 20.0
expected_lon = 77.0
threshold = 100.0  # meters
```

### Run
```bash
python "gps without timeout code.py"
```

## Future Work

- [ ] Fix the syntax error in `python code with timeout.py` and consolidate both variants into a single configurable script (e.g. `--timeout` flag)
- [ ] Replace the hardcoded expected coordinate with a dynamic flight-plan/waypoint comparison, so "expected location" updates as the mission progresses
- [ ] Add persistent logging (CSV/JSON) of every position + distance reading instead of just console output, for post-flight analysis
- [ ] Add unit tests for `calculate_distance()` against known coordinate pairs
- [ ] Trigger an automated failsafe action (e.g. return-to-home) on repeated spoofing detections, not just a console warning

## Author

**Poojasri R** — B.Tech Computer Science (Cybersecurity & Digital Forensics), VIT Bhopal
[LinkedIn](https://www.linkedin.com/in/poojasri30/) · [GitHub](https://github.com/PoojaSri-30)
