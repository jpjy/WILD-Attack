# Overview

This artifact contains the code, scripts, and datasets used to reproduce the experimental results in our paper, including **Location Lookup Table (LLT) probing**, **BSSID discovery**, and **BSSID–coordinate data** used in WILD Attack.

---

## LLT Probe

This directory contains scripts for probing and characterizing the Location Lookup Table (LLT) behavior across four major Wi-Fi Positioning System (WPS) providers:

- **Google WPS**  
- **Apple WPS**  
- **A-Map**  
- **WiGLE**

Each subfolder includes executable scripts that interact directly with the corresponding WPS provider’s API.

### Executable LLT Probe Scripts

| Provider | Script | Description |
|----------|--------|-------------|
| **Apple WPS** | `test_wloc.py` | Sends BSSID queries to Apple’s binary geolocation API and inspects LLT responses. |
| **A-Map WPS** | `test-api.py` | Queries A-Map’s official Wi-Fi geolocation API (HTTP JSON). |
| **Google WPS** | `test-all-pairs.py` | Probes Google’s WPS API with BSSIDs and optional signal strengths. |
| **WiGLE** | `test-all-pairs.py` | Queries WiGLE’s API for BSSID → coordinate mapping. |

---

## BSSID-Discovery

This directory contains the attack-side scripts demonstrating how an adversary can remotely discover target BSSIDs near the victim's real location.

It includes implementations of:

- **Hop-by-Hop Expansion** – progressively exploring BSSIDs returned by WPS providers.  
- **Last-Hex Enumeration** – enumerating BSSIDs by varying the last MAC address hex byte.

---

## Data-BSSID-Coordinates

This directory contains the experiment locations and counts of nearby BSSIDs categorized into:

- low-traffic density zones  
- medium-traffic density zones  
- high-traffic density zones  

(Used in Section 4 WILD Attack.)




