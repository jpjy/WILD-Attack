# WiFi-Localization — Open Science Artifacts

This repository contains the artifacts supporting our USENIX paper.  
It provides code and scripts to **reproduce key components of our experiments** on Wi-Fi Positioning Systems (WPS), specifically targeting the **Location Lookup Table (LLT)** update process and methods for **BSSID discovery**.

---

## Repository Structure

### 📂 `LLT Probe`
This folder contains scripts for probing the **LLT behavior** of the investigated WPS providers:
- **Google WPS**
- **Apple WPS**
- **A-Map**
- **WiGLE**

These scripts allow researchers to confirm whether and how LLT entries are updated during experiments.  
They form the basis for validating the persistence, update latency, and conflict resolution policies of different WPS providers.

---

### 📂 `BSSID-Discovery`
This folder contains scripts for demonstrating how an attacker can remotely obtain **target BSSIDs** surrounding the victim’s actual location.  
It includes two techniques:
- **Hop-by-Hop Expansion** – gradually expanding outward from a known BSSID.  
- **Last-Hex Enumeration** – enumeration of nearby BSSIDs by varying MAC address last Hex digit.


---

