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
This folder contains scripts for demonstrating how an attacker can remotely obtain **target BSSIDs** surrounding a victim’s actual location.  
It includes two techniques:
- **Hop-by-Hop Expansion** – gradually expanding outward from a known BSSID.  
- **Last-Hex Enumeration** – brute-force style enumeration of nearby BSSIDs by varying MAC address suffixes.

These tools illustrate the feasibility of discovering nearby access points (APs) without physical presence at the target site.

---

## Usage Notes

- Each subfolder contains scripts and helper files (`.py`) used in the experiments.  
- Please see the comments inside each script for detailed usage.  
- For reproducibility, ensure Python ≥3.8 and install required dependencies:
  ```bash
  pip install -r requirements.txt
